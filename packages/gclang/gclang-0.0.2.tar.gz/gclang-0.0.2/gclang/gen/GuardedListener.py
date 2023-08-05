# Generated from Guarded.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GuardedParser import GuardedParser
else:
    from GuardedParser import GuardedParser

# This class defines a complete listener for a parse tree produced by GuardedParser.
class GuardedListener(ParseTreeListener):

    # Enter a parse tree produced by GuardedParser#Impl.
    def enterImpl(self, ctx:GuardedParser.ImplContext):
        pass

    # Exit a parse tree produced by GuardedParser#Impl.
    def exitImpl(self, ctx:GuardedParser.ImplContext):
        pass


    # Enter a parse tree produced by GuardedParser#Or.
    def enterOr(self, ctx:GuardedParser.OrContext):
        pass

    # Exit a parse tree produced by GuardedParser#Or.
    def exitOr(self, ctx:GuardedParser.OrContext):
        pass


    # Enter a parse tree produced by GuardedParser#MulDiv.
    def enterMulDiv(self, ctx:GuardedParser.MulDivContext):
        pass

    # Exit a parse tree produced by GuardedParser#MulDiv.
    def exitMulDiv(self, ctx:GuardedParser.MulDivContext):
        pass


    # Enter a parse tree produced by GuardedParser#AddSub.
    def enterAddSub(self, ctx:GuardedParser.AddSubContext):
        pass

    # Exit a parse tree produced by GuardedParser#AddSub.
    def exitAddSub(self, ctx:GuardedParser.AddSubContext):
        pass


    # Enter a parse tree produced by GuardedParser#UnarySub.
    def enterUnarySub(self, ctx:GuardedParser.UnarySubContext):
        pass

    # Exit a parse tree produced by GuardedParser#UnarySub.
    def exitUnarySub(self, ctx:GuardedParser.UnarySubContext):
        pass


    # Enter a parse tree produced by GuardedParser#True.
    def enterTrue(self, ctx:GuardedParser.TrueContext):
        pass

    # Exit a parse tree produced by GuardedParser#True.
    def exitTrue(self, ctx:GuardedParser.TrueContext):
        pass


    # Enter a parse tree produced by GuardedParser#False.
    def enterFalse(self, ctx:GuardedParser.FalseContext):
        pass

    # Exit a parse tree produced by GuardedParser#False.
    def exitFalse(self, ctx:GuardedParser.FalseContext):
        pass


    # Enter a parse tree produced by GuardedParser#ExprFnCall.
    def enterExprFnCall(self, ctx:GuardedParser.ExprFnCallContext):
        pass

    # Exit a parse tree produced by GuardedParser#ExprFnCall.
    def exitExprFnCall(self, ctx:GuardedParser.ExprFnCallContext):
        pass


    # Enter a parse tree produced by GuardedParser#Identifier.
    def enterIdentifier(self, ctx:GuardedParser.IdentifierContext):
        pass

    # Exit a parse tree produced by GuardedParser#Identifier.
    def exitIdentifier(self, ctx:GuardedParser.IdentifierContext):
        pass


    # Enter a parse tree produced by GuardedParser#Brackets.
    def enterBrackets(self, ctx:GuardedParser.BracketsContext):
        pass

    # Exit a parse tree produced by GuardedParser#Brackets.
    def exitBrackets(self, ctx:GuardedParser.BracketsContext):
        pass


    # Enter a parse tree produced by GuardedParser#Number.
    def enterNumber(self, ctx:GuardedParser.NumberContext):
        pass

    # Exit a parse tree produced by GuardedParser#Number.
    def exitNumber(self, ctx:GuardedParser.NumberContext):
        pass


    # Enter a parse tree produced by GuardedParser#And.
    def enterAnd(self, ctx:GuardedParser.AndContext):
        pass

    # Exit a parse tree produced by GuardedParser#And.
    def exitAnd(self, ctx:GuardedParser.AndContext):
        pass


    # Enter a parse tree produced by GuardedParser#Equiv.
    def enterEquiv(self, ctx:GuardedParser.EquivContext):
        pass

    # Exit a parse tree produced by GuardedParser#Equiv.
    def exitEquiv(self, ctx:GuardedParser.EquivContext):
        pass


    # Enter a parse tree produced by GuardedParser#Negate.
    def enterNegate(self, ctx:GuardedParser.NegateContext):
        pass

    # Exit a parse tree produced by GuardedParser#Negate.
    def exitNegate(self, ctx:GuardedParser.NegateContext):
        pass


    # Enter a parse tree produced by GuardedParser#Logic.
    def enterLogic(self, ctx:GuardedParser.LogicContext):
        pass

    # Exit a parse tree produced by GuardedParser#Logic.
    def exitLogic(self, ctx:GuardedParser.LogicContext):
        pass


    # Enter a parse tree produced by GuardedParser#start.
    def enterStart(self, ctx:GuardedParser.StartContext):
        pass

    # Exit a parse tree produced by GuardedParser#start.
    def exitStart(self, ctx:GuardedParser.StartContext):
        pass


    # Enter a parse tree produced by GuardedParser#operatorList.
    def enterOperatorList(self, ctx:GuardedParser.OperatorListContext):
        pass

    # Exit a parse tree produced by GuardedParser#operatorList.
    def exitOperatorList(self, ctx:GuardedParser.OperatorListContext):
        pass


    # Enter a parse tree produced by GuardedParser#operator.
    def enterOperator(self, ctx:GuardedParser.OperatorContext):
        pass

    # Exit a parse tree produced by GuardedParser#operator.
    def exitOperator(self, ctx:GuardedParser.OperatorContext):
        pass


    # Enter a parse tree produced by GuardedParser#assignOperator.
    def enterAssignOperator(self, ctx:GuardedParser.AssignOperatorContext):
        pass

    # Exit a parse tree produced by GuardedParser#assignOperator.
    def exitAssignOperator(self, ctx:GuardedParser.AssignOperatorContext):
        pass


    # Enter a parse tree produced by GuardedParser#commandList.
    def enterCommandList(self, ctx:GuardedParser.CommandListContext):
        pass

    # Exit a parse tree produced by GuardedParser#commandList.
    def exitCommandList(self, ctx:GuardedParser.CommandListContext):
        pass


    # Enter a parse tree produced by GuardedParser#command.
    def enterCommand(self, ctx:GuardedParser.CommandContext):
        pass

    # Exit a parse tree produced by GuardedParser#command.
    def exitCommand(self, ctx:GuardedParser.CommandContext):
        pass


    # Enter a parse tree produced by GuardedParser#ifOperator.
    def enterIfOperator(self, ctx:GuardedParser.IfOperatorContext):
        pass

    # Exit a parse tree produced by GuardedParser#ifOperator.
    def exitIfOperator(self, ctx:GuardedParser.IfOperatorContext):
        pass


    # Enter a parse tree produced by GuardedParser#doOperator.
    def enterDoOperator(self, ctx:GuardedParser.DoOperatorContext):
        pass

    # Exit a parse tree produced by GuardedParser#doOperator.
    def exitDoOperator(self, ctx:GuardedParser.DoOperatorContext):
        pass


    # Enter a parse tree produced by GuardedParser#condition.
    def enterCondition(self, ctx:GuardedParser.ConditionContext):
        pass

    # Exit a parse tree produced by GuardedParser#condition.
    def exitCondition(self, ctx:GuardedParser.ConditionContext):
        pass


    # Enter a parse tree produced by GuardedParser#functionCall.
    def enterFunctionCall(self, ctx:GuardedParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by GuardedParser#functionCall.
    def exitFunctionCall(self, ctx:GuardedParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by GuardedParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:GuardedParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by GuardedParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:GuardedParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by GuardedParser#formalParameters.
    def enterFormalParameters(self, ctx:GuardedParser.FormalParametersContext):
        pass

    # Exit a parse tree produced by GuardedParser#formalParameters.
    def exitFormalParameters(self, ctx:GuardedParser.FormalParametersContext):
        pass


    # Enter a parse tree produced by GuardedParser#actualParameters.
    def enterActualParameters(self, ctx:GuardedParser.ActualParametersContext):
        pass

    # Exit a parse tree produced by GuardedParser#actualParameters.
    def exitActualParameters(self, ctx:GuardedParser.ActualParametersContext):
        pass


    # Enter a parse tree produced by GuardedParser#initialAssignments.
    def enterInitialAssignments(self, ctx:GuardedParser.InitialAssignmentsContext):
        pass

    # Exit a parse tree produced by GuardedParser#initialAssignments.
    def exitInitialAssignments(self, ctx:GuardedParser.InitialAssignmentsContext):
        pass



del GuardedParser