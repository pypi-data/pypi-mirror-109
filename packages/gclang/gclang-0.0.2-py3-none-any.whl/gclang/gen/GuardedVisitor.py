# Generated from Guarded.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GuardedParser import GuardedParser
else:
    from GuardedParser import GuardedParser

# This class defines a complete generic visitor for a parse tree produced by GuardedParser.

class GuardedVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GuardedParser#Impl.
    def visitImpl(self, ctx:GuardedParser.ImplContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Or.
    def visitOr(self, ctx:GuardedParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#MulDiv.
    def visitMulDiv(self, ctx:GuardedParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#AddSub.
    def visitAddSub(self, ctx:GuardedParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#UnarySub.
    def visitUnarySub(self, ctx:GuardedParser.UnarySubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#True.
    def visitTrue(self, ctx:GuardedParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#False.
    def visitFalse(self, ctx:GuardedParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#ExprFnCall.
    def visitExprFnCall(self, ctx:GuardedParser.ExprFnCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Identifier.
    def visitIdentifier(self, ctx:GuardedParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Brackets.
    def visitBrackets(self, ctx:GuardedParser.BracketsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Number.
    def visitNumber(self, ctx:GuardedParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#And.
    def visitAnd(self, ctx:GuardedParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Equiv.
    def visitEquiv(self, ctx:GuardedParser.EquivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Negate.
    def visitNegate(self, ctx:GuardedParser.NegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#Logic.
    def visitLogic(self, ctx:GuardedParser.LogicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#start.
    def visitStart(self, ctx:GuardedParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#operatorList.
    def visitOperatorList(self, ctx:GuardedParser.OperatorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#operator.
    def visitOperator(self, ctx:GuardedParser.OperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#assignOperator.
    def visitAssignOperator(self, ctx:GuardedParser.AssignOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#commandList.
    def visitCommandList(self, ctx:GuardedParser.CommandListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#command.
    def visitCommand(self, ctx:GuardedParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#ifOperator.
    def visitIfOperator(self, ctx:GuardedParser.IfOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#doOperator.
    def visitDoOperator(self, ctx:GuardedParser.DoOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#condition.
    def visitCondition(self, ctx:GuardedParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#functionCall.
    def visitFunctionCall(self, ctx:GuardedParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:GuardedParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#formalParameters.
    def visitFormalParameters(self, ctx:GuardedParser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#actualParameters.
    def visitActualParameters(self, ctx:GuardedParser.ActualParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuardedParser#initialAssignments.
    def visitInitialAssignments(self, ctx:GuardedParser.InitialAssignmentsContext):
        return self.visitChildren(ctx)



del GuardedParser