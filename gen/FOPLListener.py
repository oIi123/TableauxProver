# Generated from D:/Studium/7_Studienarbeit/Impl/src/Parser\FOPL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FOPLParser import FOPLParser
else:
    from FOPLParser import FOPLParser

# This class defines a complete listener for a parse tree produced by FOPLParser.
class FOPLListener(ParseTreeListener):

    # Enter a parse tree produced by FOPLParser#expr.
    def enterExpr(self, ctx:FOPLParser.ExprContext):
        pass

    # Exit a parse tree produced by FOPLParser#expr.
    def exitExpr(self, ctx:FOPLParser.ExprContext):
        pass


    # Enter a parse tree produced by FOPLParser#predicate.
    def enterPredicate(self, ctx:FOPLParser.PredicateContext):
        pass

    # Exit a parse tree produced by FOPLParser#predicate.
    def exitPredicate(self, ctx:FOPLParser.PredicateContext):
        pass


    # Enter a parse tree produced by FOPLParser#quantor.
    def enterQuantor(self, ctx:FOPLParser.QuantorContext):
        pass

    # Exit a parse tree produced by FOPLParser#quantor.
    def exitQuantor(self, ctx:FOPLParser.QuantorContext):
        pass


    # Enter a parse tree produced by FOPLParser#terms.
    def enterTerms(self, ctx:FOPLParser.TermsContext):
        pass

    # Exit a parse tree produced by FOPLParser#terms.
    def exitTerms(self, ctx:FOPLParser.TermsContext):
        pass


    # Enter a parse tree produced by FOPLParser#termlist.
    def enterTermlist(self, ctx:FOPLParser.TermlistContext):
        pass

    # Exit a parse tree produced by FOPLParser#termlist.
    def exitTermlist(self, ctx:FOPLParser.TermlistContext):
        pass


    # Enter a parse tree produced by FOPLParser#term.
    def enterTerm(self, ctx:FOPLParser.TermContext):
        pass

    # Exit a parse tree produced by FOPLParser#term.
    def exitTerm(self, ctx:FOPLParser.TermContext):
        pass


    # Enter a parse tree produced by FOPLParser#var.
    def enterVar(self, ctx:FOPLParser.VarContext):
        pass

    # Exit a parse tree produced by FOPLParser#var.
    def exitVar(self, ctx:FOPLParser.VarContext):
        pass


    # Enter a parse tree produced by FOPLParser#varlist.
    def enterVarlist(self, ctx:FOPLParser.VarlistContext):
        pass

    # Exit a parse tree produced by FOPLParser#varlist.
    def exitVarlist(self, ctx:FOPLParser.VarlistContext):
        pass


    # Enter a parse tree produced by FOPLParser#func.
    def enterFunc(self, ctx:FOPLParser.FuncContext):
        pass

    # Exit a parse tree produced by FOPLParser#func.
    def exitFunc(self, ctx:FOPLParser.FuncContext):
        pass


