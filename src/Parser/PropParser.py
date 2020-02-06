from gen.PropositionalLexer import PropositionalLexer
from gen.PropositionalParser import PropositionalParser
from src.Model.PropositionalExpressionTree import PropositionalExpressionTree
from antlr4 import *
from antlr4.error.ErrorListener import *


class PropParser:
    parse_idx = 0

    @staticmethod
    def parse(expr: str) -> PropositionalExpressionTree:
        lexer = PropositionalLexer(InputStream(expr))
        stream = CommonTokenStream(lexer)
        parser = PropositionalParser(stream)

        parser.removeErrorListeners()
        lexer.removeErrorListeners()
        error_listener = PropParserErrorListener()
        parser.addErrorListener(error_listener)
        lexer.addErrorListener(error_listener)

        tree = parser.expr()

        if error_listener.handled_errors > 0:
            raise RecognitionException("The input was not correct")
            
        expr_tree = PropositionalExpressionTree(tree, PropParser.parse_idx)
        PropParser.parse_idx += 1
        return expr_tree


class PropParserErrorListener(ErrorListener):
    handled_errors = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.handled_errors += 1
