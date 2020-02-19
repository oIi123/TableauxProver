import unittest

from unittest.mock import MagicMock

from src.Model.PropositionalExpressionTree import *
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from src.view.DrawingCalculator import DrawingCalculator


def parse(expr):
    return PropParser.parse(expr).expr



class TestPlView(unittest.TestCase):
    def setUp(self):
        PropParser.parse_idx = 0

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
            
            self.assertEqual(expr, expr_positions[i][1], f'{pos}:{i}')

    def get_drawing_calculator(self, true_exprs, false_exprs):
        painter_mock = MagicMock()
        tableaux_builder = PropositionalTableauxBuilder(
            true_exprs=true_exprs,
            false_exprs=false_exprs,
            visit_idx= len(true_exprs) + len(false_exprs)
        )
        tableaux_builder.auto_resolve()

        return DrawingCalculator(tableaux_builder, painter_mock,
                                 False, False, 10)

    def test_closing_impls_1(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[
                parse('p->q'),
                parse('q->r'),
                parse('r->s'),
            ],
            false_exprs=[
                parse('!s->!p'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('p->q'),
            parse('q->r'),
            parse('r->s'),
            parse('!s->!p'),
            parse('!s'),
            parse('!p'),
            parse('p'),
            parse('s'),
            [
                [
                    parse('p'),
                ],
                [
                    parse('q'),
                    [
                        [
                            parse('q'),
                        ],
                        [
                            parse('r'),
                            [
                                [
                                    parse('r'),
                                ],
                                [
                                    parse('s'),
                                ],
                            ]
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_impls_2(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('(a->b)&(b->c)->(a->c)'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('(a->b)&(b->c)->(a->c)'),
            parse('(a->b)&(b->c)'),
            parse('a->c'),
            parse('a'),
            parse('c'),
            parse('a->b'),
            parse('b->c'),
            [
                [
                    parse('a'),
                ],
                [
                    parse('b'),
                    [
                        [
                            parse('b'),
                        ],
                        [
                            parse('c'),
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_impls_3(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('!!a->a'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('!!a->a'),
            parse('!!a'),
            parse('a'),
            parse('!a'),
            parse('a'),
        ])
    
    def test_closing_impls_4(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('a->!!a'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('a->!!a'),
            parse('a'),
            parse('!!a'),
            parse('!a'),
            parse('a'),
        ])
    
    def test_closing_impls_5(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('a->(b->a)'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('a->(b->a)'),
            parse('a'),
            parse('b->a'),
            parse('a'),
        ])
    
    def test_closing_impls_6(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('!a->(a->b)'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('!a->(a->b)'),
            parse('!a'),
            parse('a->b'),
            parse('a'),
        ])
    
    def test_closing_impls_7(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('(a->b)->(!b->!a)'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('(a->b)->(!b->!a)'),
            parse('a->b'),
            parse('!b->!a'),
            parse('!b'),
            parse('!a'),
            parse('a'),
            parse('b'),
            [
                [
                    parse('a'),
                ],
                [
                    parse('b'),
                ],
            ],
        ])
    
    def test_closing_impls_8(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('(!a->!b)->(b->a)'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('(!a->!b)->(b->a)'),
            parse('!a->!b'),
            parse('b->a'),
            parse('b'),
            parse('a'),
            [
                [
                    parse('!a'),
                    parse('a'),
                ],
                [
                    parse('!b'),
                    parse('b'),
                ],
            ],
        ])

    def test_closing_eq_1(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('a->(b->c)<->a&b->c'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('a->(b->c)<->a&b->c'),
            [
                [
                    parse('a->(b->c)'),
                    parse('a&b->c'),
                    parse('b->c'),
                    parse('a'),
                    parse('b'),
                    parse('c'),
                    [
                        [
                            parse('a&b'),
                            [
                                [
                                    parse('a'),
                                ],
                                [
                                    parse('b'),
                                ],
                            ],
                        ],
                        [
                            parse('c'),
                        ],
                    ],
                ],
                [
                    parse('a->(b->c)'),
                    parse('a&b->c'),
                    parse('a&b'),
                    parse('c'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('a'),
                        ],
                        [
                            parse('b->c'),
                            [
                                [
                                    parse('b'),
                                ],
                                [
                                    parse('c'),
                                ]
                            ]
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_eq_2(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('!(a&b)<->!a|!b'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('!(a&b)<->!a|!b'),
            [
                [
                    parse('!(a&b)'),
                    parse('!a|!b'),
                    parse('a&b'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('!a'),
                            parse('a'),
                        ],
                        [
                            parse('!b'),
                            parse('b'),
                        ],
                    ],
                ],
                [
                    parse('!(a&b)'),
                    parse('!a|!b'),
                    parse('!a'),
                    parse('!b'),
                    parse('a'),
                    parse('b'),
                    parse('a&b'),
                    [
                        [
                            parse('a'),
                        ],
                        [
                            parse('b'),
                        ],
                    ],
                ],
            ],
        ])
    
    def test_closing_eq_3(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('!(a|b)<->!a&!b'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('!(a|b)<->!a&!b'),
            [
                [
                    parse('!(a|b)'),
                    parse('!a&!b'),
                    parse('a|b'),
                    parse('!a'),
                    parse('!b'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('a'),
                        ],
                        [
                            parse('b'),
                        ],
                    ],
                ],
                [
                    parse('!(a|b)'),
                    parse('!a&!b'),
                    parse('a|b'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('!a'),
                            parse('a'),
                        ],
                        [
                            parse('!b'),
                            parse('b'),
                        ],
                    ],
                ],
            ],
        ])
    
    def test_closing_eq_4(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('!(!a|!b)<->a&b'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('!(!a|!b)<->a&b'),
            [
                [
                    parse('!(!a|!b)'),
                    parse('a&b'),
                    parse('!a|!b'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('!a'),
                            parse('a'),
                        ],
                        [
                            parse('!b'),
                            parse('b'),
                        ],
                    ],
                ],
                [
                    parse('!(!a|!b)'),
                    parse('a&b'),
                    parse('!a|!b'),
                    parse('!a'),
                    parse('!b'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('a'),
                        ],
                        [
                            parse('b'),
                        ],
                    ],
                ],
            ],
        ])
    
    def test_closing_eq_5(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('!(!a&!b)<->a|b'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('!(!a&!b)<->a|b'),
            [
                [
                    parse('!(!a&!b)'),
                    parse('a|b'),
                    parse('!a&!b'),
                    parse('!a'),
                    parse('!b'),
                    parse('a'),
                    parse('b'),
                    [
                        [
                            parse('a'),
                        ],
                        [
                            parse('b'),
                        ],
                    ],
                ],
                [
                    parse('!(!a&!b)'),
                    parse('a|b'),
                    parse('a'),
                    parse('b'),
                    parse('!a&!b'),
                    [
                        [
                            parse('!a'),
                            parse('a'),
                        ],
                        [
                            parse('!b'),
                            parse('b'),
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_or_1(self):
        drawing_calculator = self.get_drawing_calculator(
            true_exprs=[],
            false_exprs=[
                parse('a|!a'),
            ],
        )

        self.traverse_tree(drawing_calculator, [
            parse('a|!a'),
            parse('a'),
            parse('!a'),
            parse('a')
        ])
