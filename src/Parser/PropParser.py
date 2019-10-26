from gen.PropositionalLexer import PropositionalLexer
from gen.PropositionalParser import PropositionalParser
from src.Model.PropositionalExpressionTree import PropositionalExpressionTree
from antlr4 import *


class PropParser:
    def __init__(self, expr: str):
        """
        Initialises a Parser for Propositional Logic with a Propositional Expression
        :param expr: Expression in Propositional Logic
        """
        self.expr = expr

    def parse(self) -> PropositionalExpressionTree:
        lexer = PropositionalLexer(InputStream(self.expr))
        stream = CommonTokenStream(lexer)
        parser = PropositionalParser(stream)
        tree = parser.expr()
        return PropositionalExpressionTree(tree)
