import unittest

from unittest.mock import MagicMock

from src.Model.FoplExpressionTree import *
from src.Parser.FoplParser import FoplParser
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
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
    expr = FoplParser.parse(expr).expr
    ConstConverter(expr)
    return expr


class TestFoplView(unittest.TestCase):
    def setUp(self):
        FoplParser.parse_idx = 0

    def traverse_tree(self, drawing_calculator, exprs, pos=''):
        btn_fun_mock = MagicMock()
        expr_positions = drawing_calculator.calc_expr_positions(btn_fun_mock)

        for i, expr in enumerate(exprs):
            if type(expr) == list:
                left = drawing_calculator.get_child(0, 375)
                right = drawing_calculator.get_child(1, 375)

                self.traverse_tree(left, expr[0], pos + 'l')
                self.traverse_tree(right, expr[1], pos + 'r')
                continue
            
            self.assertEqual(parse(expr), expr_positions[i][1], f'{pos}:{i}')

    def get_drawing_calculator(self, true_exprs, false_exprs):
        painter_mock = MagicMock()
        tableaux_builder = FoplTableauxBuilder(
            true_exprs=[parse(e) for e in true_exprs],
            false_exprs=[parse(e) for e in false_exprs],
            visit_idx= len(true_exprs) + len(false_exprs)
        )
        tableaux_builder.auto_resolve()

        return DrawingCalculator(tableaux_builder, painter_mock,
                                 False, False, 10)

    def test_closing_1(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '!(E)x A(x)->(A)x !A(x)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '!(E)x A(x)->(A)x !A(x)',
            '!(E)x A(x)',
            '(A)x !A(x)',
            '(E)x A(x)',
            '!A(X0)',
            'A(X0)',
        ])
    
    def test_closing_2(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x (A(x)->B(x))->((A)x A(x)->(A)x B(x))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x (A(x)->B(x))->((A)x A(x)->(A)x B(x))',
            '(A)x (A(x)->B(x))',
            '(A)x A(x)->(A)x B(x)',
            '(A)x A(x)',
            '(A)x B(x)',
            'B(X0)',
            'A(X0)->B(X0)',
            [
                [
                    'A(X0)',
                    'A(X0)',
                ],
                [
                    'B(X0)',
                ]
            ]
        ])
    
    def test_closing_3(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x F(x)->(A)y F(y)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x F(x)->(A)y F(y)',
            '(A)x F(x)',
            '(A)y F(y)'
            'F(X0)',
            'F(X0)',
        ])

    def test_closing_4(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x (M(x)->P(x))&(A)x (S(x)->M(x))->(A)x (S(x)->P(x))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x (M(x)->P(x))&(A)x (S(x)->M(x))->(A)x (S(x)->P(x))',
            '(A)x (M(x)->P(x))&(A)x (S(x)->M(x))',
            '(A)x (S(x)->P(x))',
            '(A)x (M(x)->P(x))',
            '(A)x (S(x)->M(x))',
            'S(X0)->P(X0)',
            'S(X0)',
            'P(X0)',
            'M(X0)->P(X0)',
            [
                [
                    'M(X0)',
                    'S(X0)->M(X0)',
                    [
                        [
                            'S(X0)',
                        ],
                        [
                            'M(X0)',
                        ],
                    ],
                ],
                [
                    'P(X0)',
                ]
            ]
        ])
    
    def test_closing_5(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x (P(x)->!M(x))&(E)x (S(x)&M(x))->(E)x (S(x)&!P(x))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x (P(x)->!M(x))&(E)x (S(x)&M(x))->(E)x (S(x)&!P(x))',
            '(A)x (P(x)->!M(x))&(E)x (S(x)&M(x))',
            '(E)x (S(x)&!P(x))',
            '(A)x (P(x)->!M(x))',
            '(E)x (S(x)&M(x))',
            'S(X0)&M(X0)',
            'S(X0)',
            'M(X0)',
            'S(X0)&!P(X0)',
            [
                [
                    'S(X0)',
                ],
                [
                    '!P(X0)',
                    'P(X0)',
                    'P(X0)->!M(X0)',
                    [
                        [
                            'P(X0)',
                        ],
                        [
                            '!M(X0)',
                            'M(X0)',
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_6(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '!(A)x F(x)<->(E)x !F(x)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '!(A)x F(x)<->(E)x !F(x)',
            [
                [
                    '!(A)x F(x)',
                    '(E)x !F(x)',
                    '(A)x F(x)',
                    '!F(X0)',
                    'F(X0)',
                    'F(X0)',
                ],
                [
                    '!(A)x F(x)',
                    '(E)x !F(x)',
                    '(A)x F(x)',
                    'F(X0)',
                    '!F(X0)',
                    'F(X0)',
                ]
            ]
        ])

    def test_closing_7(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '((E)x F(x)->(A)x G(x))->((A)x (F(x)->G(x)))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '((E)x F(x)->(A)x G(x))->(A)x (F(x)->G(x))',
            '(E)x F(x)->(A)x G(x)',
            '(A)x (F(x)->G(x))',
            'F(X0)->G(X0)',
            'F(X0)',
            'G(X0)',
            [
                [
                    '(E)x F(x)',
                    'F(X0)',
                ],
                [
                    '(A)x G(x)',
                    'G(X0)',
                ],
            ],
        ])

    def test_closing_8(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(A)x (F(x)&G(x))<->(A)x F(x)&(A)x G(x)'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(A)x (F(x)&G(x))<->(A)x F(x)&(A)x G(x)',
            [
                [
                    '(A)x (F(x)&G(x))',
                    '(A)x F(x)&(A)x G(x)',
                    '(A)x F(x)',
                    '(A)x G(x)',
                    'F(X0)&G(X0)',
                    [
                        [
                            'F(X0)',
                            'F(X0)',
                        ],
                        [
                            'G(X0)',
                            'F(X0)',
                            'G(X0)',
                        ],
                    ],
                ],
                [
                    '(A)x (F(x)&G(x))',
                    '(A)x F(x)&(A)x G(x)',
                    [
                        [
                            '(A)x F(x)',
                            'F(X0)',
                            'F(X0)&G(X0)',
                            'F(X0)',
                        ],
                        [
                            '(A)x G(x)',
                            'G(X0)',
                            'F(X0)&G(X0)',
                            'F(X0)',
                            'G(X0)',
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_9(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '((A)x F(x)|(A)x G(x))->(A)x (F(x)|G(x))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '((A)x F(x)|(A)x G(x))->(A)x (F(x)|G(x))',
            '(A)x F(x)|(A)x G(x)',
            '(A)x (F(x)|G(x))',
            'F(X0)|G(X0)',
            'F(X0)',
            'G(X0)',
            [
                [
                    '(A)x F(x)',
                    'F(X0)'
                ],
                [
                    '(A)x G(x)',
                    'G(X0)'
                ],
            ],
        ])

    def test_closing_10(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(E)x (F(x)&G(x))->((E)x F(x)&(E)x G(x))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(E)x (F(x)&G(x))->((E)x F(x)&(E)x G(x))',
            '(E)x (F(x)&G(x))',
            '(E)x F(x)&(E)x G(x)',
            [
                [
                    '(E)x F(x)',
                    'F(X0)&G(X0)',
                    'F(X0)',
                    'G(X0)',
                    'F(X0)',
                ],
                [
                    '(E)x G(x)',
                    'F(X0)&G(X0)',
                    'F(X0)',
                    'G(X0)',
                    'G(X0)',
                ],
            ],
        ])

    def test_closing_11(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                '(E)x (F(x)|G(x))<->((E)x F(x)|(E)x G(x))'
            ]
        )

        self.traverse_tree(drawing_calculator, [
            '(E)x (F(x)|G(x))<->((E)x F(x)|(E)x G(x))',
            [
                [
                    '(E)x (F(x)|G(x))',
                    '(E)x F(x)|(E)x G(x)',
                    [
                        [
                            '(E)x F(x)',
                            'F(X0)',
                            'F(X0)|G(X0)',
                            'F(X0)',
                        ],
                        [
                            '(E)x G(x)',
                            'G(X0)',
                            'F(X0)|G(X0)',
                            'F(X0)',
                            'G(X0)',
                        ],
                    ],
                ],
                [
                    '(E)x (F(x)|G(x))',
                    '(E)x F(x)|(E)x G(x)',
                    '(E)x F(x)',
                    '(E)x G(x)',
                    'F(X0)|G(X0)',
                    [
                        [
                            'F(X0)',
                            'F(X0)',
                        ],
                        [
                            'G(X0)',
                            'F(X0)',
                            'G(X0)',
                        ],
                    ],
                ],
            ],
        ])
