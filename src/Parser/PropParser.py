from gen.PropositionalLexer import PropositionalLexer
from gen.PropositionalParser import PropositionalParser
from src.Model.PropositionalExpressionTree import PropositionalExpressionTree
from antlr4 import *
from src.Parser.ParseException import ParseException, ParserErrorListener

class PropParser:
    parse_idx = 0

    @staticmethod
    def parse(expr: str) -> PropositionalExpressionTree:
        lexer = PropositionalLexer(InputStream(expr))
        stream = CommonTokenStream(lexer)
        parser = PropositionalParser(stream)

        parser.removeErrorListeners()
        lexer.removeErrorListeners()
        error_listener = ParserErrorListener()
        parser.addErrorListener(error_listener)
        lexer.addErrorListener(error_listener)

        tree = parser.expr()

        if error_listener.error_msg is not None:
            raise ParseException(error_listener.error_msg, error_listener.column)
            
        expr_tree = PropositionalExpressionTree(tree, PropParser.parse_idx)
        PropParser.parse_idx += 1
        return expr_tree
