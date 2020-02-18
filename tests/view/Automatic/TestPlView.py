import unittest

from unittest.mock import MagicMock

from src.Model.PropositionalExpressionTree import *
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from src.view.DrawingCalculator import DrawingCalculator


def parse(expr):
    return PropParser.parse(expr).expr



class TestPlView(unittest.TestCase):
    def test_not_closing_impls_1(self):
        painter_mock = MagicMock()
        tableaux_builder = PropositionalTableauxBuilder(
            true_exprs=[
                parse('q->p'),
                parse('q->r'),
                parse('r->s'),
            ],
            false_exprs=[
                parse('!s->!p'),
            ]
        )
        tableaux_builder.auto_resolve()

        drawing_calculator = DrawingCalculator(tableaux_builder, painter_mock,
                                               False, False, 10)
