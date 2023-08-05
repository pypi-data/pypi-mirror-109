from ..gen.GuardedVisitor import GuardedVisitor
from ..gen.GuardedParser import GuardedParser


class PythonVisitor(GuardedVisitor):
    def __init__(self):
        self.lines = []  # lines of python code
        self._stack = []

    def visitIdentifier(self, ctx: GuardedParser.IdentifierContext):
        self._stack.append(ctx.getText())

    def visitNumber(self, ctx: GuardedParser.NumberContext):
        self._stack.append(ctx.getText())

    def visitTrue(self, ctx: GuardedParser.TrueContext):
        self._stack.append('True')

    def visitFalse(self, ctx: GuardedParser.FalseContext):
        self._stack.append('False')

    def visitUnarySub(self, ctx: GuardedParser.UnarySubContext):
        self.visitChildren(ctx)
        self._stack.append(f'-{self._stack.pop()}')

    def visitNegate(self, ctx: GuardedParser.NegateContext):
        self.visitChildren(ctx)
        self._stack.append(f'not {self._stack.pop()}')

    def visitAnd(self, ctx: GuardedParser.AndContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(f'{left} and {right}')

    def visitOr(self, ctx: GuardedParser.OrContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(f'{left} or {right}')

    def visitImpl(self, ctx: GuardedParser.ImplContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(f'{right} or not {left}')

    def visitEquiv(self, ctx: GuardedParser.EquivContext):
        self.visitChildren(ctx)
        right, left = self._stack.pop(), self._stack.pop()
        self._stack.append(f'{left} == {right}')

    def visitAddSub(self, ctx: GuardedParser.AddSubContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._stack.pop(), self._stack.pop()
        op = children[1]
        if op == ctx.ADD():
            self._stack.append(f'{left} + {right}')
        elif op == ctx.SUB():
            self._stack.append(f'{left} - {right}')
        else:
            raise Exception(f"Unexpected operation: {ctx.op}")

    def visitMulDiv(self, ctx: GuardedParser.MulDivContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._stack.pop(), self._stack.pop()
        op = children[1]
        if op == ctx.MUL():
            self._stack.append(f'{left} * {right}')
        elif op == ctx.DIV():
            self._stack.append(f'{left} / {right}')
        else:
            raise Exception(f"Unexpected operation: {ctx.getText()}")

    def visitAssignOperator(self, ctx: GuardedParser.AssignOperatorContext):
        self.visitChildren(ctx)

        var_name = next(ctx.getChildren()).getText()
        self.lines.append(f"{var_name} = {self._stack.pop()}")

    def visitLogic(self, ctx: GuardedParser.LogicContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        right, left = self._stack.pop(), self._stack.pop()
        op = children[1]
        if op == ctx.LT():
            self._stack.append(f'{left} < {right}')
        elif op == ctx.LE():
            self._stack.append(f'{left} <= {right}')
        elif op == ctx.GT():
            self._stack.append(f'{left} > {right}')
        elif op == ctx.GE():
            self._stack.append(f'{left} >= {right}')
        elif op == ctx.EQ():
            self._stack.append(f'{left} == {right}')
        elif op == ctx.NEQ():
            self._stack.append(f'{left} != {right}')
        else:
            raise Exception(f"Unexpected logical operation: {op}")

    def visitIfOperator(self, ctx: GuardedParser.IfOperatorContext):
        ...

    def visitDoOperator(self, ctx: GuardedParser.DoOperatorContext):
        ...

    def visitCondition(self, ctx: GuardedParser.ConditionContext):
        self.visitChildren(ctx)
        children = list(ctx.getChildren())

        self._stack.append(f'assert {self._stack.pop()}')

    def visitStart(self, ctx: GuardedParser.StartContext):
        self.visitChildren(ctx)
        print('\n'.join(self.lines))
