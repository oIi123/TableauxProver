from antlr4 import *
from antlr4.error.ErrorListener import *

from gen.FOPLLexer import FOPLLexer
from gen.FOPLParser import FOPLParser
from src.Model.FoplExpressionTree import FoplExpressionTree
from src.Parser.FoplValidator import FoplValidator


class FoplParser:
    def __init__(self, expr: str):
        """
        Initialises a Parser for FOPL with a FOPL Expression
        :param expr: Expression in FOPL
        """
        self.expr = expr

    def parse(self) -> FoplExpressionTree:
        lexer = FOPLLexer(InputStream(self.expr))
        stream = CommonTokenStream(lexer)
        parser = FOPLParser(stream)

        parser.removeErrorListeners()
        lexer.removeErrorListeners()
        error_listener = FoplParserErrorListener()
        parser.addErrorListener(error_listener)
        lexer.addErrorListener(error_listener)

        tree = parser.expr()

        if error_listener.handled_errors > 0:
            raise RecognitionException("The input was not correct.")

        expr_tree = FoplExpressionTree(tree)
        validator = FoplValidator()
        if not validator.validate(expr_tree.expr):
            raise RecognitionException("Some Predicates or Functions do not have the same arity.")

        return expr_tree


class FoplParserErrorListener(ErrorListener):
    handled_errors = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.handled_errors += 1
