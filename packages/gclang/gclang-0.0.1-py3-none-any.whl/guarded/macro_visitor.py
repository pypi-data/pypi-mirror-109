import dataclasses

from .gen.GuardedVisitor import GuardedVisitor
from .gen.GuardedParser import GuardedParser


@dataclasses.dataclass
class Function:
    parameters: list[str]
    body: GuardedParser.OperatorListContext


class MacroVisitor(GuardedVisitor):

    def __init__(self):
        self.functions = {}
        self.replacementStack = []

    def visitFunctionDefinition(self, ctx: GuardedParser.FunctionDefinitionContext):
        children = list(ctx.getChildren())

        function_name = children[0].getText()
        function_params = children[2]
        
        params = list(filter(lambda t: t != ',', map(lambda c: c.getText(), function_params.getChildren())))
        body = children[5]

        self.functions[function_name] = Function(params, body)