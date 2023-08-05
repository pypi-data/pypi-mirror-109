from random import randint
from pprint import pprint

import antlr4
import itertools
from .gen.GuardedVisitor import GuardedVisitor
from .gen.GuardedParser import GuardedParser
from .macro_visitor import MacroVisitor


class ExecutingVisitor(MacroVisitor):
    def __init__(self):
        super(ExecutingVisitor, self).__init__()
        self._stack = []
        self.vars = {} # name -> value mapping of all variables

    def visitNumber(self, ctx: GuardedParser.NumberContext):
        num = float(ctx.getText())
        self._stack.append(num)

    def visitIdentifier(self, ctx: GuardedParser.IdentifierContext):
        identifier = ctx.getText()

        if identifier in self.vars:
            self._stack.append(self.vars[identifier])
            return

        if self.replacementStack:
            replacement = self.replacementStack[-1]
            if identifier in replacement:
                self._stack.append(replacement[identifier])
                return

        raise AssertionError("Undefined identifier " + identifier)  

    def visitTrue(self, ctx: GuardedParser.TrueContext):
        self._stack.append(True)

    def visitFalse(self, ctx: GuardedParser.FalseContext):
        self._stack.append(False)

    def visitUnarySub(self, ctx: GuardedParser.UnarySubContext):
        self.visitChildren(ctx)
        value = self._stack.pop()
        self._stack.append(-value)

    def visitNegate(self, ctx: GuardedParser.NegateContext):
        self.visitChildren(ctx)
        value = self._stack.pop()
        self._stack.append(not value)

    def visitAnd(self, ctx: GuardedParser.AndContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(left and right)

    def visitOr(self, ctx: GuardedParser.OrContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(left or right)

    def visitImpl(self, ctx: GuardedParser.ImplContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(right or not left)

    def visitEquiv(self, ctx: GuardedParser.EquivContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(bool(left) == bool(right))

    def visitAddSub(self, ctx: GuardedParser.AddSubContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._stack.pop(), self._stack.pop()
        op = children[1]
        if op == ctx.ADD():
            self._stack.append(left + right)
        elif op == ctx.SUB():
            self._stack.append(left - right)
        else:
            raise Exception(f"Unexpected operation: {ctx.op}")

    def visitMulDiv(self, ctx: GuardedParser.MulDivContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._stack.pop(), self._stack.pop()
        op = children[1]
        if op == ctx.MUL():
            self._stack.append(left * right)
        elif op == ctx.DIV():
            self._stack.append(left / right)
        else:
            raise Exception(f"Unexpected operation: {ctx.getText()}")

    def visitLogic(self, ctx: GuardedParser.LogicContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._stack.pop(), self._stack.pop()
        op = children[1]
        if op == ctx.LT():
            self._stack.append(left < right)
        elif op == ctx.LE():
            self._stack.append(left <= right)
        elif op == ctx.GT():
            self._stack.append(left > right)
        elif op == ctx.GE():
            self._stack.append(left >= right)
        elif op == ctx.EQ():
            self._stack.append(left == right)
        elif op == ctx.NEQ():
            self._stack.append(left != right)
        else:
            raise Exception(f"Unexpected logical operation: {op}")

    def visitAssignOperator(self, ctx: GuardedParser.AssignOperatorContext):
        children_iter = ctx.getChildren()
        var_names = list(map(
            lambda c: c.getText(),
            filter(lambda c: c.getText() != ',',
                itertools.takewhile(lambda c: c.getText() != ':=', children_iter))
            ) 
        )
        assert len(var_names) == len(set(var_names)), "Multi assignment with same variables in left-hand side"

        expressions = list(filter(lambda c: c.getText() != ',', children_iter))
        assert len(var_names) == len(expressions), "Multi assignment with different number of variables and values"

        self.visitChildren(ctx)
        values = list(reversed(
            list(self._stack.pop() for i in range(len(expressions)))
        ))
        self.vars |= dict(zip(var_names, values))

    def visitExprFnCall(self, ctx: GuardedParser.ExprFnCallContext):
        raise Exception("Macro function call in expression")

    def visitCommand(self, ctx: GuardedParser.CommandContext):
        children = list(ctx.getChildren())
        if isinstance(children[0], GuardedParser.LogicContext):
            self.visitLogic(children[0])
        elif isinstance(children[0], GuardedParser.TrueContext):
            self.visitTrue(children[0])
        elif isinstance(children[0], GuardedParser.FalseContext):
            self.visitFalse(children[0])
        elif isinstance(children[0], GuardedParser.AndContext):
            self.visitAnd(children[0])
        elif isinstance(children[0], GuardedParser.OrContext):
            self.visitOr(children[0])
        elif isinstance(children[0], GuardedParser.NegateContext):
            self.visitNegate(children[0])
        else:
            raise Exception(f"Fuse of Guarded command must be valid logical expression")

        ctx.fuse = self._stack.pop()
        ctx.command = children[2]

    def visitCommandList(self, ctx: GuardedParser.CommandListContext):
        self.visitChildren(ctx)

        ctx.true_commands = []
        for child in ctx.getChildren():
            if isinstance(child, GuardedParser.CommandContext) and child.fuse:
                ctx.true_commands.append(child.command)

    def visitIfOperator(self, ctx: GuardedParser.IfOperatorContext):
        self.visitChildren(ctx)

        command_list = list(ctx.getChildren())[1]
        if len(command_list.true_commands) != 0:
            rand = randint(0, len(command_list.true_commands) - 1)
            self.visitOperatorList(command_list.true_commands[rand])

    def visitDoOperator(self, ctx: GuardedParser.DoOperatorContext):
        while True:
            # recalc all fuses on each iteration
            self.visitChildren(ctx)

            command_list = next(c for c in ctx.getChildren() if isinstance(c, GuardedParser.CommandListContext))
            if len(command_list.true_commands) != 0:
                rand = randint(0, len(command_list.true_commands) - 1)
                self.visitOperatorList(command_list.true_commands[rand])
            else:
                break

    def visitCondition(self, ctx: GuardedParser.ConditionContext):
        pass

    def visitInitialAssignments(self, ctx: GuardedParser.InitialAssignmentsContext):
        self.visitChildren(ctx)

    def visitStart(self, ctx: GuardedParser.StartContext):
        # macro layer
        children = list(ctx.getChildren())
        [self.visitFunctionDefinition(f) for f in children if isinstance(f, GuardedParser.FunctionDefinitionContext)]

        # execute
        self.visitChildren(ctx)

        for key, val in self.vars.items():
            print(f"{key} = {val}")

    def visitFunctionCall(self, ctx: GuardedParser.FunctionCallContext):
        children = list(ctx.getChildren())
        function_name = children[0].getText()
        function = self.functions[function_name]

        params_ctx = children[2]
        self.visitChildren(params_ctx)
        params = reversed([self._stack.pop() for p in function.parameters])
        replacement = dict(zip(function.parameters, params))
        print('replacement: ', replacement)

        self.replacementStack.append(replacement)
        old_vars = self.vars
        self.vars = {}
        self.visitOperatorList(function.body)
        self.vars = old_vars | self.vars
        self.replacementStack.pop()