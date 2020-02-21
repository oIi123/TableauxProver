import unittest

from unittest.mock import MagicMock

from src.Model.FoplExpressionTree import *
from src.Parser.FoplParser import FoplParser
from src.TableauxBuilder.IfoplTableauxBuilder import IfoplTableauxBuilder
from src.view.DrawingCalculator import DrawingCalculator


class ConstConverter:
    def __init__(self, expr):
        expr.visit(self)
    
    def __getattribute__(self, name):
        if name.startswith('visited_') and name != 'visited_Const':
            def visited_any(expr):
                for attr in ['lhs', 'rhs', 'expr']:
                    if hasattr(expr, attr):
                        getattr(expr, attr).visit(self)
                if hasattr(expr, 'terms'):
                    for term in expr.terms:
                        term.visit(self)
            return visited_any
        return super().__getattribute__(name)         

    def visited_Const(self, const):
        idx = const.name[1:]
        const.name = f'X_{idx}'


def parse(expr):
    if expr.startswith('[') and expr.endswith(']'):
        expr = expr[1:-1]
    expr = FoplParser.parse(expr).expr
    ConstConverter(expr)
    return expr


class TestIfoplView(unittest.TestCase):
    def setUp(self):
        FoplParser.parse_idx = 0

    def traverse_tree(self, drawing_calculator, exprs, pos=''):
        btn_fun_mock = MagicMock()
        expr_positions = drawing_calculator.calc_expr_positions(btn_fun_mock)

        for i, expr in enumerate(exprs):
            if type(expr) == list:
                if len(expr) == 2 and type(expr[0]) == type(expr[1]) == list:
                    left = drawing_calculator.get_child(0, 375)
                    right = drawing_calculator.get_child(1, 375)

                    self.traverse_tree(left, expr[0], pos + 'l')
                    self.traverse_tree(right, expr[1], pos + 'r')
                    continue

                child = drawing_calculator.get_child(0, 375)
                self.traverse_tree(child, expr, pos + 'c')
                continue

            self.assertEqual(parse(expr), expr_positions[i][1], f'{pos}:{i}')

    def get_drawing_calculator(self, true_exprs, false_exprs):
        painter_mock = MagicMock()
        tableaux_builder = IfoplTableauxBuilder(
            true_exprs=[parse(e) for e in true_exprs],
            false_exprs=[parse(e) for e in false_exprs],
            visit_idx= len(true_exprs) + len(false_exprs)
        )
        tableaux_builder.auto_resolve()

        return DrawingCalculator(tableaux_builder, painter_mock,
                                 False, True, 10)

    def test_closing_1(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x P(x)->!(E)x !P(x)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x P(x)->!(E)x !P(x)',
            [
                '(A)x P(x)',
                '!(E)x !P(x)',
                [
                    '(A)x P(x)',
                    '(E)x !P(x)',
                    '!P(X0)',
                    'P(X0)',
                    '[P(X0)]',
                ],
            ],
        ])
    
    def test_closing_2(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(E)x P(x)->!(A)x !P(x)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(E)x P(x)->!(A)x !P(x)',
            [
                '(E)x P(x)',
                '!(A)x !P(x)',
                [
                    '(E)x P(x)',
                    '(A)x !P(x)',
                    'P(X0)',
                    '!P(X0)',
                    '[P(X0)]',
                ],
            ],
        ])

    def test_closing_3(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x !P(x)<->!(E)x P(x)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x !P(x)<->!(E)x P(x)',
            '((A)x !P(x)->!(E)x P(x))&(!(E)x P(x)->(A)x !P(x))',
            [
                [
                    '(A)x !P(x)->!(E)x P(x)',
                    [
                        '!(E)x P(x)',
                        '(A)x !P(x)',
                        [
                            '(A)x !P(x)',
                            '(E)x P(x)',
                            'P(X0)',
                            '!P(X0)',
                            '[P(X0)]',
                        ],
                    ],
                ],
                [
                    '!(E)x P(x)->(A)x !P(x)',
                    [
                        '!(E)x P(x)',
                        '(A)x !P(x)',
                        '[(E)x P(x)]',
                        [
                            '[(E)x P(x)]',
                            '!P(X0)',
                            [
                                '[(E)x P(x)]',
                                'P(X0)',
                                'P(X0)',
                            ],
                        ],
                    ],
                ],
            ],
        ])
