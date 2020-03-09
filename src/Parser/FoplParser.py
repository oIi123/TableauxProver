from antlr4 import *

from gen.FOPLLexer import FOPLLexer
from gen.FOPLParser import FOPLParser
from src.Model.FoplExpressionTree import FoplExpressionTree
from src.Parser.ParseException import ParseException, ParserErrorListener


class FoplParser:
    parse_idx = 0

    @staticmethod
    def parse(expr: str) -> FoplExpressionTree:
        lexer = FOPLLexer(InputStream(expr))
        stream = CommonTokenStream(lexer)
        parser = FOPLParser(stream)

        parser.removeErrorListeners()
        lexer.removeErrorListeners()
        error_listener = ParserErrorListener()
        parser.addErrorListener(error_listener)
        lexer.addErrorListener(error_listener)

        tree = parser.expr()

        if error_listener.error_msg is not None:
            raise ParseException(error_listener.error_msg, error_listener.column)

        expr_tree = FoplExpressionTree(tree, visit_idx=FoplParser.parse_idx)
        FoplParser.parse_idx += 1
        return expr_tree
