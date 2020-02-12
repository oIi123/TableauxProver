from antlr4 import *
from antlr4.error.ErrorListener import *

from gen.FOPLLexer import FOPLLexer
from gen.FOPLParser import FOPLParser
from src.Model.FoplExpressionTree import FoplExpressionTree


class FoplParser:
    parse_idx = 0

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

        if error_listener.error_msg is not None:
            raise RecognitionException(error_listener.error_msg)

        expr_tree = FoplExpressionTree(tree, visit_idx=FoplParser.parse_idx)
        FoplParser.parse_idx += 1
        return expr_tree


class FoplParserErrorListener(ErrorListener):
    error_msg = None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if self.error_msg is None:
            self.error_msg = f"The input was incorrect."
        self.error_msg += f"<br/>Column {column}: {msg}"
