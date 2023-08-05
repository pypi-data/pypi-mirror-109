from .gen.GuardedVisitor import GuardedVisitor
from .gen.GuardedParser import GuardedParser
from pprint import pprint
import sympy as sp
import itertools
sp.Eq

# todo: assert using fucntion call in expressions not in condition

class DerivingVisitor(GuardedVisitor):
    def __init__(self):
        self._expr_stack = []
        self._predicate_stack = []

        self._depth = 1
        self._claims = []

    def visitExpression(self, ctx):
        if isinstance(ctx, GuardedParser.TrueContext):
            self.visitTrue(ctx)
        elif isinstance(ctx, GuardedParser.FalseContext):
            self.visitFalse(ctx)
        elif isinstance(ctx, GuardedParser.AndContext):
            self.visitAnd(ctx)
        elif isinstance(ctx, GuardedParser.OrContext):
            self.visitOr(ctx)
        elif isinstance(ctx, GuardedParser.ImplContext):
            self.visitImpl(ctx)
        elif isinstance(ctx, GuardedParser.IdentifierContext):
            self.visitIdentifier(ctx)
        elif isinstance(ctx, GuardedParser.LogicContext):
            self.visitLogic(ctx)
        elif isinstance(ctx, GuardedParser.MulDivContext):
            self.visitMulDiv(ctx)
        elif isinstance(ctx, GuardedParser.AddSubContext):
            self.visitAddSub(ctx)
        elif isinstance(ctx, GuardedParser.BracketsContext):
            self.visitBrackets(ctx)
        elif isinstance(ctx, GuardedParser.NegateContext):
            self.visitNegate(ctx)
        elif isinstance(ctx, GuardedParser.NumberContext):
            self.visitNumber(ctx)
        elif isinstance(ctx, GuardedParser.UnarySubContext):
            self.visitUnarySub(ctx)
        elif isinstance(ctx, GuardedParser.ExprFnCallContext):
            self.visitExprFnCall(ctx)
    
    def visitTrue(self, ctx):
        self._expr_stack.append(sp.true)

    def visitFalse(self, ctx):
        self._expr_stack.append(sp.false)

    def visitIdentifier(self, ctx: GuardedParser.IdentifierContext):
        var_name = ctx.getText()
        self._expr_stack.append(sp.Symbol(var_name))

    def visitNumber(self, ctx: GuardedParser.NumberContext):
        num = float(ctx.getText())
        self._expr_stack.append(num)

    def visitUnarySub(self, ctx: GuardedParser.UnarySubContext):
        self.visitChildren(ctx)
        value = self._expr_stack.pop()
        self._expr_stack.append(-value)

    def visitNegate(self, ctx: GuardedParser.NegateContext):
        self.visitChildren(ctx)
        value = self._expr_stack.pop()
        self._expr_stack.append(sp.Not(value))

    def visitAnd(self, ctx: GuardedParser.AndContext):
        self.visitChildren(ctx)
        right, left = self._expr_stack.pop(), self._expr_stack.pop()
        self._expr_stack.append(sp.And(left, right))

    def visitOr(self, ctx: GuardedParser.OrContext):
        self.visitChildren(ctx)
        right, left = self._expr_stack.pop(), self._expr_stack.pop()
        self._expr_stack.append(sp.Or(left, right))

    def visitImpl(self, ctx: GuardedParser.ImplContext):
        self.visitChildren(ctx)
        right, left = self._expr_stack.pop(), self._expr_stack.pop()
        self._expr_stack.append(sp.Implies(left, right))

    def visitExprFnCall(self, ctx: GuardedParser.ExprFnCallContext):
        children = list(next(ctx.getChildren()).getChildren())
        function_name = children[0].getText()
        parameters_ctx = children[2]

        parameters = []
        for parameter in parameters_ctx.getChildren():
            if parameter.getText() == ',':
                continue
            self.visitExpression(parameter)
            parameters.append(self._expr_stack.pop())

        function = sp.Function(function_name)

        self._expr_stack.append(function(*parameters))

    def visitLogic(self, ctx: GuardedParser.LogicContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._expr_stack.pop(), self._expr_stack.pop()
        op = children[1]
        if op == ctx.LT():
            self._expr_stack.append(sp.Lt(left, right))
        elif op == ctx.LE():
            self._expr_stack.append(sp.Le(left, right))
        elif op == ctx.GT():
            self._expr_stack.append(sp.Gt(left, right))
        elif op == ctx.GE():
            self._expr_stack.append(sp.Ge(left, right))
        elif op == ctx.EQ():
            self._expr_stack.append(sp.Eq(left, right))
        elif op == ctx.NEQ():
            self._expr_stack.append(sp.Not(sp.Eq(left, right)))
        else:
            raise Exception(f"Unexpected logical operation: {op}")
    def visitAddSub(self, ctx: GuardedParser.AddSubContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._expr_stack.pop(), self._expr_stack.pop()
        op = children[1]
        if op == ctx.ADD():
            self._expr_stack.append(sp.Add(left, right))
        elif op == ctx.SUB():
            self._expr_stack.append(sp.Add(left, sp.Mul(-1, right)))
        else:
            raise Exception(f"Unexpected operation: {ctx.op}")
    def visitMulDiv(self, ctx: GuardedParser.MulDivContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._expr_stack.pop(), self._expr_stack.pop()
        op = children[1]
        if op == ctx.MUL():
            self._expr_stack.append(sp.Mul(left, right))
        elif op == ctx.DIV():
            self._expr_stack.append(sp.Mul(left, sp.Pow(right, -1)))
        else:
            raise Exception(f"Unexpected operation: {ctx.getText()}")

    def visitAssignOperator(self, ctx: GuardedParser.AssignOperatorContext):
        children_iter = ctx.getChildren()
        var_names = list(map(
            lambda c: sp.Symbol(c.getText()),
            filter(lambda c: c.getText() != ',',
                itertools.takewhile(lambda c: c.getText() != ':=', children_iter))
            ) 
        )
        expressions = list(filter(lambda c: c.getText() != ',', children_iter))
        assert len(var_names) == len(expressions), "Multi assignment with different number of variables and values"

        self.visitChildren(ctx)
        values = list(reversed(
            list(self._expr_stack.pop() for i in range(len(expressions)))
        ))

        old_condition = self._predicate_stack.pop()
        new_condition = old_condition.xreplace(dict(zip(var_names, values)))

        print('    ' * self._depth + f'{old_condition} --[assign {var_names}:={values}]--> {new_condition}')
        
        self._predicate_stack.append(new_condition)

    def visitIfOperator(self, ctx: GuardedParser.AssignOperatorContext):
        children = list(ctx.getChildren())
        commandList = filter(lambda c: isinstance(c, GuardedParser.CommandContext),
            children[1].getChildren())
        current_predicate = self._predicate_stack.pop()

        operator_list_predicates = []
        for command in commandList:
            command_children = list(command.getChildren())
            self.visitExpression(command_children[0])
            fuse = self._expr_stack.pop() # take fuse predicate

            operator_list: GuardedParser.OperatorListContext = command_children[2]
            self._predicate_stack.append(current_predicate)
            self._depth += 1
            self.visitOperatorList(operator_list)
            self._depth -= 1
            predicate = self._predicate_stack.pop()

            operator_list_predicates.append((fuse, predicate))
        
        fuse_predicate = sp.false
        operator_list_predicate = sp.true
        for fuse, operator_list in operator_list_predicates:
            fuse_predicate = sp.Or(fuse_predicate, fuse)
            operator_list_predicate = sp.And(operator_list_predicate, sp.Implies(fuse, operator_list))
        
        new_predicate = sp.And(fuse_predicate, operator_list_predicate)
        print('    ' * self._depth + f'{str(current_predicate)} --[if]--> {str(new_predicate)}')
        self._predicate_stack.append(new_predicate)

    def visitDoOperator(self, ctx: GuardedParser.DoOperatorContext):
        children = list(ctx.getChildren())
        assert isinstance(children[0], GuardedParser.ConditionContext), "do..od operator without invariant in deriving mode"

        self.visitCondition(children[0])
        invariant = self._expr_stack.pop()
        old_predicate = self._predicate_stack.pop()

        # check if (invariant and non bb => old_predicate)
        invariant_and_non_bb = invariant
        for command in children[2].getChildren():
            if not isinstance(command, GuardedParser.CommandContext):
                continue
            fuse = next(command.getChildren())
            self.visitExpression(fuse)
            fuse_predicate = self._expr_stack.pop()
            invariant_and_non_bb = sp.And(invariant_and_non_bb, sp.Not(fuse_predicate))
        
        self._claims.append(f"{invariant_and_non_bb.simplify()} >> {old_predicate}")
        self._predicate_stack.append(invariant)

    def visitOperatorList(self, ctx: GuardedParser.OperatorListContext):
        for operator in reversed(list(ctx.getChildren())):
            self.visitOperator(operator)
    
    def visitInitialAssignments(self, ctx: GuardedParser.InitialAssignmentsContext):
        pass

    def visitStart(self, ctx: GuardedParser.StartContext):
        try:
            post_condition_ctx: GuardedParser.ConditionContext = next(c for c in ctx.getChildren()
                if isinstance(c, GuardedParser.ConditionContext))
        except StopIteration:
            raise Exception('Post-condition not found')

        self.visitCondition(post_condition_ctx)
        post_condition = self._expr_stack.pop()

        # post_condition_str = list(post_condition_ctx.getChildren())[1].getText()
        # post_condition = sp.parse_expr(post_condition_str)
        self._predicate_stack.append(post_condition)

        print('Post-condition:', str(post_condition))
        self.visitChildren(ctx)
        pre_condition = sp.simplify(self._predicate_stack.pop())
        print('Pre-condition:', str(pre_condition.simplify()))

        self._claims and print('\nPROVE manually, that following formulas are tauthologies:')        
        for i in range(len(self._claims)):
            print(f'{i + 1}. {self._claims[i]}')