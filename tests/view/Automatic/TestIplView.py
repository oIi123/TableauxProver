import unittest

from unittest.mock import MagicMock

from src.Model.PropositionalExpressionTree import *
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder
from src.view.DrawingCalculator import DrawingCalculator


def parse(expr):
    if expr.startswith('[') and expr.endswith(']'):
        expr = expr[1:-1]
    return PropParser.parse(expr).expr


class TestIplView(unittest.TestCase):
    def setUp(self):
        PropParser.parse_idx = 0

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
        tableaux_builder = IpcTableauxBuilder(
            true_exprs=[parse(e) for e in true_exprs],
            false_exprs=[parse(e) for e in false_exprs],
            visit_idx= len(true_exprs) + len(false_exprs)
        )
        tableaux_builder.auto_resolve()

        return DrawingCalculator(tableaux_builder, painter_mock,
                                 False, True, 10)

    def test_closing_1(self):
        drawing_calculator = self.get_drawing_calculator(
            [
                'a',
            ],
            [
                'a|b'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a',
            'a|b',
            'a',
        ])

    def test_closing_2(self):
        drawing_calculator = self.get_drawing_calculator(
            [
                'a&b',
            ],
            [
                'a'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a&b',
            'a',
            'a',
        ])
    
    def test_closing_3(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                'a&b->!(!a|!b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a&b->!(!a|!b)',
            [
                'a&b',
                '!(!a|!b)',
                [
                    'a&b',
                    '!a|!b',
                    'a',
                    'b',
                    [
                        [
                            '!a',
                            '[a]',
                        ],
                        [
                            '!b',
                            '[b]'
                        ]
                    ]
                ]
            ]
        ])

    def test_closing_4(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                'a|b->!(!a&!b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a|b->!(!a&!b)',
            [
                'a|b',
                '!(!a&!b)',
                [
                    'a|b',
                    '!a&!b',
                    '!a',
                    '!b',
                    [
                        [
                            'a',
                            '[a]',
                        ],
                        [
                            'b',
                            '[a]',
                            '[b]',
                        ]
                    ]
                ]
            ]
        ])

    def test_closing_5(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '!a|!b->!(a&b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '!a|!b->!(a&b)',
            [
                '!a|!b',
                '!(a&b)',
                [
                    '!a|!b',
                    'a&b',
                    'a',
                    'b',
                    [
                        [
                            '!a',
                            '[a]',
                        ],
                        [
                            '!b',
                            '[b]',
                        ]
                    ]
                ]
            ]
        ])
    
    def test_closing_6(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '!a&!b->!(a|b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '!a&!b->!(a|b)',
            [
                '!a&!b',
                '!(a|b)',
                [
                    '!a&!b',
                    'a|b',
                    '!a',
                    '!b',
                    [
                        [
                            'a',
                            '[a]',
                        ],
                        [
                            'b',
                            '[a]',
                            '[b]',
                        ]
                    ]
                ]
            ]
        ])
    
    def test_closing_7(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '!(a|b)->!a&!b'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '!(a|b)->!a&!b',
            [
                '!(a|b)',
                '!a&!b',
                [
                    [
                        '!a',
                        [
                            '[a|b]',
                            'a',
                            '[a]',
                        ]
                    ],
                    [
                        '!b',
                        [
                            '[a|b]',
                            'b',
                            '[a]',
                            '[b]',
                        ]
                    ]
                ]
            ]
        ])

    def test_closing_8(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                'a&b->!(a->!b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a&b->!(a->!b)',
            [
                'a&b',
                '!(a->!b)',
                [
                    'a&b',
                    'a->!b',
                    'a',
                    'b',
                    [
                        [
                            'a->!b',
                            'a',
                        ],
                        [
                            '!b',
                            '[b]',
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_9(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                'a&!b->!(a->b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a&!b->!(a->b)',
            [
                'a&!b',
                '!(a->b)',
                [
                    'a&!b',
                    'a->b',
                    'a',
                    '!b',
                    [
                        [
                            'a->b',
                            'a',
                        ],
                        [
                            'b',
                            '[b]',
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_10(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '(a->!b)->!(a&b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '(a->!b)->!(a&b)',
            [
                'a->!b',
                '!(a&b)',
                [
                    'a->!b',
                    'a&b',
                    'a',
                    'b',
                    [
                        [
                            'a->!b',
                            'a',
                        ],
                        [
                            '!b',
                            '[b]',
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_11(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '!(a&b)->(a->!b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '!(a&b)->(a->!b)',
            [
                '!(a&b)',
                'a->!b',
                [
                    '!(a&b)',
                    'a',
                    '!b',
                    [
                        '!(a&b)',
                        'a',
                        'b',
                        '[a&b]',
                        [
                            [
                                'a',
                                'b',
                                '[a]',
                            ],
                            [
                                'a',
                                'b',
                                '[b]',
                            ],
                        ],
                    ],
                ]
            ],
        ])

    def test_closing_12(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                'a|b->(!a->b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            'a|b->(!a->b)',
            [
                'a|b',
                '!a->b',
                [
                    'a|b',
                    '!a',
                    'b',
                    [
                        [
                            'a',
                            '[a]',
                        ],
                        [
                            'b',
                        ],
                    ],
                ]
            ],
        ])
    
    def test_closing_13(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '(!a|b)->(a->b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '(!a|b)->(a->b)',
            [
                '!a|b',
                'a->b',
                [
                    '!a|b',
                    'a',
                    'b',
                    [
                        [
                            '!a',
                            '[a]',
                        ],
                        [
                            'b',
                        ],
                    ],
                ]
            ],
        ])

    def test_closing_14(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '(a<->b)<->((a->b)&(b->a))'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '(a<->b)<->((a->b)&(b->a))',
            '((a<->b)->((a->b)&(b->a)))&(((a->b)&(b->a))->(a<->b))',
            [
                [
                    '((a<->b)->((a->b)&(b->a)))',
                    [
                        '(a->b)&(b->a)',
                        'a<->b',
                        [
                            [
                                'a->b',
                                [
                                    'a<->b',
                                    'a',
                                    'b',
                                    '(a->b)&(b->a)',
                                    'a->b',
                                    [
                                        [
                                            'a->b',
                                            'a',
                                        ],
                                        [
                                            'b',
                                        ],
                                    ],
                                ],
                            ],
                            [
                                'b->a',
                                [
                                    'a<->b',
                                    'b',
                                    'a',
                                    '(a->b)&(b->a)',
                                    'a->b',
                                    'b->a',
                                    [
                                        [
                                            'a->b',
                                            'a',
                                            [
                                                [
                                                    'b->a',
                                                    'b',
                                                ],
                                                [
                                                    'a',
                                                ],
                                            ],
                                        ],
                                        [
                                            'b',
                                            [
                                                [
                                                    'b->a',
                                                    'b',
                                                ],
                                                [
                                                    'a',
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ]
                ],
                [
                    '(((a->b)&(b->a))->(a<->b))',
                    [
                        '(a->b)&(b->a)',
                        'a<->b',
                        'a->b',
                        'b->a',
                        '(a->b)&(b->a)',
                        [
                            [
                                'a->b',
                                [
                                    'a->b',
                                    'b',
                                    'a',
                                    [
                                        [
                                            'a->b',
                                            'a',
                                        ],
                                        [
                                            'b',
                                        ],
                                    ],
                                ]
                            ],
                            [
                                'b->a',
                                [
                                    'a->b',
                                    'b->a',
                                    'b',
                                    'a',
                                    [
                                        [
                                            'a->b',
                                            'a',
                                            [
                                                [
                                                    'b->a',
                                                    'b',
                                                ],
                                                [
                                                    'a',
                                                ],
                                            ],
                                        ],
                                        [
                                            'b',
                                            [
                                                [
                                                    'b->a',
                                                    'b',
                                                ],
                                                [
                                                    'a',
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_15(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '(a->b)<->((a|b)<->b)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '(a->b)<->((a|b)<->b)',
            '((a->b)->((a|b)<->b))&(((a|b)<->b)->(a->b))',
            [
                [
                    '(a->b)->((a|b)<->b)',
                    [
                        '(a|b)<->b',
                        'a->b',
                        '((a|b)->b)&(b->(a|b))',
                        [
                            [
                                '(a|b)->b',
                                [
                                    'a->b',
                                    'a|b',
                                    'b',
                                    [
                                        [
                                            'a->b',
                                            'a',
                                            [
                                                [
                                                    'a',
                                                ],
                                                [
                                                    'b',
                                                ],
                                            ],
                                        ],
                                        [
                                            'b',
                                        ],
                                    ],
                                ],
                            ],
                            [
                                'b->(a|b)',
                                [
                                    'b',
                                    'a|b',
                                    'a',
                                    'b',
                                ],
                            ],
                        ],
                    ],
                ],
                [
                    '((a|b)<->b)->(a->b)',
                    [
                        'a|b<->b',
                        'a->b',
                        [
                            'a|b<->b',
                            'a',
                            'b',
                            '(a|b->b)&(b->a|b)',
                            'a|b->b',
                            [
                                [
                                    'a|b->b',
                                    'a|b',
                                    'a',
                                ],
                                [
                                    'b',
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_16(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '(a->b)<->((a&b)<->a)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '(a->b)<->((a&b)<->a)',
            '((a->b)->((a&b)<->a))&(((a&b)<->a)->(a->b))',
            [
                [
                    '(a->b)->((a&b)<->a)',
                    [
                        '(a&b)<->a',
                        'a->b',
                        '((a&b)->a)&(a->(a&b))',
                        [
                            [
                                '(a&b)->a',
                                [
                                    'a',
                                    'a&b',
                                    'a',
                                ]
                            ],
                            [
                                'a->(a&b)',
                                [
                                    'a->b',
                                    'a',
                                    'a&b',
                                    [
                                        [
                                            'a',
                                        ],
                                        [
                                            'b',
                                            [
                                                [
                                                    'a->b',
                                                    'a',
                                                ],
                                                [
                                                    'b'
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
                [
                    '((a&b)<->a)->(a->b)',
                    [
                        '(a&b)<->a',
                        'a->b',
                        [
                            '(a&b)<->a',
                            'a',
                            'b',
                            '((a&b)->a)&(a->(a&b))',
                            'a&b->a',
                            'a->a&b',
                            [
                                [
                                    'a&b->a',
                                    'a&b',
                                    [
                                        [
                                            'a',
                                        ],
                                        [
                                            'b',
                                            [
                                                [
                                                    'a->a&b',
                                                    'a'
                                                ],
                                                [
                                                    'a&b',
                                                    'a',
                                                    'b',
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                                [
                                    'a',
                                    [
                                        [
                                            'a->a&b',
                                            'a',
                                        ],
                                        [
                                            'a&b',
                                            'a',
                                            'b',
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ])

    def test_closing_17(self):
        drawing_calculator = self.get_drawing_calculator(
            [],
            [
                '(a&b)<->((a->b)<->a)'
            ]
        )
        self.traverse_tree(drawing_calculator, [
            '(a&b)<->((a->b)<->a)',
            '((a&b)->((a->b)<->a))&(((a->b)<->a)->(a&b))',
            [
                [
                    '(a&b)->((a->b)<->a)',
                    [
                        'a->b<->a',
                        'a&b',
                        'a',
                        'b',
                        '((a->b)->a)&(a->(a->b))',
                        [
                            [
                                '(a->b)->a',
                                [
                                    'a',
                                    'b',
                                    'a',
                                ],
                            ],
                            [
                                'a->(a->b)',
                                [
                                    'a',
                                    'b',
                                    'a',
                                    'a->b',
                                    [
                                        'a',
                                        'b',
                                        'b',
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
                [
                    '((a->b)<->a)->(a&b)',
                    [
                        'a->b<->a',
                        'a&b',
                        [
                            [
                                'a',
                                '((a->b)->a)&(a->(a->b))',
                                '(a->b)->a',
                                'a->(a->b)',
                                [
                                    [
                                        '(a->b)->a',
                                        'a->b',
                                        [
                                            '(a->b)->a',
                                            'a->(a->b)',
                                            'a',
                                            'b',
                                            [
                                                [
                                                    'a->(a->b)',
                                                    'a',
                                                ],
                                                [
                                                    'a->b',
                                                    [
                                                        [
                                                            'a->b',
                                                            'a',
                                                        ],
                                                        [
                                                            'b',
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                    [
                                        'a',
                                    ],
                                ],
                            ],
                            [
                                'b',
                                '((a->b)->a)&(a->(a->b))',
                                '(a->b)->a',
                                'a->(a->b)',
                                [
                                    [
                                        '(a->b)->a',
                                        'a->(a->b)',
                                        'a->b',
                                        [
                                            '(a->b)->a',
                                            'a',
                                            'b',
                                            [
                                                [
                                                    'a->(a->b)',
                                                    'a',
                                                ],
                                                [
                                                    'a->b',
                                                    [
                                                        [
                                                            'a->b',
                                                            'a',
                                                        ],
                                                        [
                                                            'b',
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                    [
                                        'a',
                                        [
                                            [
                                                'a->(a->b)',
                                                'a'
                                            ],
                                            [
                                                'a->b',
                                                [
                                                    [
                                                        'a->b',
                                                        'a',
                                                    ],
                                                    [
                                                        'b',
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ])
