from antlr4 import *
from antlr4.error.ErrorListener import *

from gen.FOPLLexer import FOPLLexer
from gen.FOPLParser import FOPLParser
from src.Model.FoplExpressionTree import FoplExpressionTree


class FoplParser:
    @staticmethod
    def parse(expr: str) -> FoplExpressionTree:
        lexer = FOPLLexer(InputStream(expr))
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
        return expr_tree


class FoplParserErrorListener(ErrorListener):
    handled_errors = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.handled_errors += 1
