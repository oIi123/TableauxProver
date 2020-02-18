import unittest

from src.builder_factory import LogicType
from src.Parser.FoplParser import FoplParser
from src.TableauxBuilder.BaseManualTableau import BaseManualTableau, BaseTableauxBuilder
from src.TableauxBuilder.IfoplTableauxBuilder import IfoplTableauxBuilder


def parse(expr: str):
    return FoplParser.parse(expr).expr

class TestIfoplManualTableau(unittest.TestCase):
    def test_incorrect_1(self):
        expr = parse('(P()->T())&(T()->F())->(P()->F())')

        l_expr = [
            parse('(P()->T())&(T()->F())'),
            parse('(P()->F())'),
        ]

        tableau = IfoplTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [[]], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_2(self):
        expr = parse('(P()->T())&(T()->F())->(P()->F())')

        l_expr = [
            parse('(P()->T())&(T()->F())'),
            parse('(P()->F())'),
        ]

        r_expr = [
            parse('(P()->F())'),
        ]

        tableau = IfoplTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_3(self):
        expr = parse('(P()->T())&(T()->F())->(P()->F())')

        l_expr = [
            parse('(P()->T())&(T()->F())'),
        ]

        r_expr = [
            parse('(T()->F())'),
        ]

        tableau = IfoplTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)

    def test_incorrect_4(self):
        expr_t = parse('(P()->T())&(T()->F())->(P()->F())')
        expr_f = parse('(P()->T())&(T()->F())->(P()->F())')

        l_expr = [
            parse('(P()->T())&(T()->F())'),
        ]

        r_expr = [
            parse('(P()->F())'),
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_5(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = []

        r_expr = [
            parse('P()'),
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_6(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = [
            parse('P()'),
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_7(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(C)'),
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertFalse(success)
    
    def test_incorrect_8(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(C)|T(C)')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertFalse(success)
    
    def test_incorrect_9(self):
        expr_t = parse('P(A)|T(B)')
        expr_f = parse('(A)x P(x)')

        l_expr = []

        r_expr = [
            parse('P(A)'),
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertFalse(success)
    
    def test_incorrect_10(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(A)|T(A)')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertFalse(success)
    
    def test_incorrect_11(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(C)|T(D)')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C', 'D'])

        self.assertFalse(success)
    
    def test_incorrect_12(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(B)')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertFalse(success)

    def test_incorrect_13(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(A)&T(B)'),
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertFalse(success)

    def test_incorrect_14(self):
        expr_t = parse('(A)x,y M(x,l(x,y))')
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('(A)y M(A,l(B,y))')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t],
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertFalse(success)

    def test_correct_1(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = []

        r_expr = []

        cf_expr = [
            parse('!P()')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [cf_expr], [])

        self.assertTrue(success)

    def test_correct_2(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = []

        r_expr = [
            parse('P()'),
            parse('T()')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_3(self):
        expr_t = parse('!!P()')
        expr_f = parse('(P()->T())&(T()->F())->(P()->F())')

        l_expr = [
            parse('(P()->T())&(T()->F())')
        ]

        r_expr = [
            parse('(P()->F())')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_4(self):
        expr_t = [
            parse('Q()->K()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            parse('!S()')
        ]

        r_expr = [
            parse('!Q()')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f[0], None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_correct_5(self):
        expr_t = [
            parse('Q()->K()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            [parse('K()')], []
        ]

        r_expr = [
            [], [parse('Q()')]
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_6(self):
        expr_t = [
            parse('Q()->K()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            [], [parse('K()')]
        ]

        r_expr = [
            [parse('Q()')], []
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_7(self):
        expr_t = [
            parse('P()|T()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            [parse('T()')], [parse('P()')]
        ]

        r_expr = [
            [], []
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_8(self):
        expr_t = [
            parse('P()|T()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            [parse('P()')], [parse('T()')]
        ]

        r_expr = [
            [], []
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)

    def test_correct_9(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            parse('P()'),
            parse('T()&F()')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_10(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            parse('P()&T()'),
            parse('F()')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_11(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]
        expr_cf = [
            parse('!P()')
        ]

        l_expr = [
            parse('P()')
        ]
        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs=expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_12(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]
        expr_cf = [
            parse('P()&T()')
        ]

        l_expr = [[],[]]
        r_expr = [[],[]]
        cf_expr = [
            [parse('P()')],
            [parse('T()')]
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs=expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertTrue(success)
    
    def test_correct_13(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]
        expr_cf = [
            parse('P()|T()')
        ]

        l_expr = [[]]
        r_expr = [[]]
        cf_expr = [[
            parse('P()'),
            parse('T()')
        ]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs=expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertTrue(success)
    
    def test_correct_14(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]
        expr_cf = [
            parse('P()->T()')
        ]

        l_expr = [[
            parse('P()')
        ]]
        r_expr = [[
            parse('T()')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs=expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertTrue(success)
    
    def test_correct_15(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]
        expr_cf = [
            parse('P()<->T()')
        ]

        l_expr = [[]]
        r_expr = [[]]
        cf_expr = [[
            parse('(P()->T())&(T()->P())')
        ]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs=expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertTrue(success)

    def test_correct_16(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(A)'),
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertTrue(success)
    
    def test_correct_17(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(B)'),
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['B'])

        self.assertTrue(success)
    
    def test_correct_18(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(A)'),
            parse('P(B)'),
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertTrue(success)

    def test_correct_19(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(A)')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertTrue(success)
    
    def test_correct_20(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(B)|T(B)')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['B'])

        self.assertTrue(success)
    
    def test_correct_21(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(A)'),
            parse('P(B)|T(B)'),
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertTrue(success)

    def test_correct_22(self):
        expr_t = parse('P(A)|T(B)')
        expr_f = parse('(A)x P(x)')

        l_expr = []

        r_expr = [
            parse('P(C)'),
        ]

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertTrue(success)
    
    def test_correct_23(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(C)|T(C)')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertTrue(success)
    
    def test_correct_24(self):
        expr_t = parse('(A)x,y M(x,l(x,y))')
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('(A)y M(A,l(A, y))')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=[expr_t],
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertTrue(success)
    
    def test_correct_25(self):
        expr_t = [
            parse('(A)x,y M(x,l(x,y))'),
            parse('(A)y M(A,l(A,y))'),
        ]
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('M(A,l(A,l(B,NIL)))')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[1], None, None), [l_expr], [r_expr], [[]], ['A', 'B', 'NIL'])

        self.assertTrue(success)
    
    def test_correct_26(self):
        expr_t = [
            parse('(A)x,y M(x,l(x,y))'),
            parse('(A)y M(A,l(A,y))'),
        ]
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('M(A,l(A,l(A,l(B,NIL))))')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[1], None, None), [l_expr], [r_expr], [[]], ['A', 'B', 'NIL'])

        self.assertTrue(success)

    def test_merge_true_and_perm_1(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            parse('P()&T()'),
            parse('F()')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!Q()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_processed])

        self.assertEqual(0, len(tableau.children))

    def test_merge_true_and_perm_2(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            parse('T()&F()'),
            parse('P()')
        ]

        r_expr = []

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!Q()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_processed])

        self.assertEqual(0, len(tableau.children))


    def test_merge_false_impl(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]

        l_expr = [
            parse('!S()')
        ]

        r_expr = [
            parse('!Q()')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), [l_expr], [r_expr], [[]], [])

        self.assertEqual(1, len(tableau.children))
        sequent = tableau.children[0].sequent

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('!S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!Q()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))

    def test_merge_true_impl(self):
        expr_t = [
            parse('K()->R()'),
            parse('P()&T()&F()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()')
        ]

        l_expr = [
            [], [parse('R()')],
        ]

        r_expr = [
            [parse('K()')], [],
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        sequent = tableau.sequent

        self.assertEqual(2, len(tableau.children))

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_processed])

        c_s_1 = tableau.children[0].sequent
        c_s_2 = tableau.children[1].sequent

        self.assertEqual(2, len(c_s_1[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('R()->S()'), c_s_1[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), c_s_1[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(c_s_1[BaseTableauxBuilder.false_atoms]))
        self.assertIn(parse('K()'), c_s_1[BaseTableauxBuilder.false_atoms])
        self.assertEqual(0, len(c_s_1[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(c_s_1[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(c_s_1[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('K()->R()'), c_s_1[BaseTableauxBuilder.true_processed])

        self.assertEqual(2, len(c_s_2[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('R()->S()'), c_s_2[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), c_s_2[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(c_s_2[BaseTableauxBuilder.true_atoms]))
        self.assertIn(parse('R()'), c_s_2[BaseTableauxBuilder.true_atoms])
        self.assertEqual(0, len(c_s_2[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(c_s_2[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(c_s_2[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('K()->R()'), c_s_2[BaseTableauxBuilder.true_processed])

    def test_merge_cf_or(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]
        expr_cf = [
            parse('S()|K()')
        ]

        l_expr = []
        r_expr = []
        cf_expr = [
            parse('S()'),
            parse('K()')
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, None, expr_cf[0]), [l_expr], [r_expr], [cf_expr], [])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!Q()'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L()&M()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertEqual(2, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))
        self.assertIn(parse('S()'), sequent[BaseTableauxBuilder.certain_falsehood_atoms])
        self.assertIn(parse('K()'), sequent[BaseTableauxBuilder.certain_falsehood_atoms])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))

    def test_merge_cf_and(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]
        expr_cf = [
            parse('S()&K()')
        ]

        l_expr = [[],[]]
        r_expr = [[],[]]
        cf_expr = [
            [parse('S()')],
            [parse('K()')]
        ]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertEqual(2, len(tableau.children))
        sequent_1 = tableau.children[0].sequent
        sequent_2 = tableau.children[1].sequent

        self.assertEqual(3, len(sequent_1[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent_1[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent_1[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent_1[BaseTableauxBuilder.true_exprs])

        self.assertEqual(0, len(sequent_1[BaseTableauxBuilder.false_exprs]))

        self.assertEqual(0, len(sequent_1[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertEqual(1, len(sequent_1[BaseTableauxBuilder.certain_falsehood_atoms]))
        self.assertIn(parse('S()'), sequent_1[BaseTableauxBuilder.certain_falsehood_atoms])

        self.assertEqual(0, len(sequent_1[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent_1[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent_1[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent_1[BaseTableauxBuilder.false_processed]))


        self.assertEqual(3, len(sequent_2[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent_2[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent_2[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent_2[BaseTableauxBuilder.true_exprs])

        self.assertEqual(0, len(sequent_2[BaseTableauxBuilder.false_exprs]))

        self.assertEqual(0, len(sequent_2[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertEqual(1, len(sequent_2[BaseTableauxBuilder.certain_falsehood_atoms]))
        self.assertIn(parse('K()'), sequent_2[BaseTableauxBuilder.certain_falsehood_atoms])

        self.assertEqual(0, len(sequent_2[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent_2[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent_2[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent_2[BaseTableauxBuilder.false_processed]))

    def test_merge_cf_impl(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]
        expr_cf = [
            parse('S()->K()')
        ]

        l_expr = [[
            parse('S()')
        ]]
        r_expr = [[
            parse('K()')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertEqual(1, len(tableau.children))
        sequent = tableau.children[0].sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertIn(parse('S()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertIn(parse('K()'), sequent[BaseTableauxBuilder.false_atoms])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))
        
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
    
    def test_merge_cf_eq(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]
        expr_cf = [
            parse('S()<->K()')
        ]

        l_expr = [[]]
        r_expr = [[]]
        cf_expr = [[
            parse('(S()->K())&(K()->S())')
        ]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!Q()'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L()&M()'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('(S()->K())&(K()->S())'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))
        
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
        self.assertIn(parse('S()<->K()'), sequent[BaseTableauxBuilder.certain_falsehood_processed])

    def test_merge_cf_not(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]
        expr_cf = [
            parse('!S()')
        ]

        l_expr = [[
            parse('S()')
        ]]
        r_expr = [[]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, [])

        self.assertEqual(1, len(tableau.children))
        sequent = tableau.children[0].sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertIn(parse('S()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))
        
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
        self.assertIn(parse('!S()'), sequent[BaseTableauxBuilder.certain_falsehood_processed])

    def test_merge_true_not(self):
        expr_t = [
            parse('!S()'),
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!Q()'),
            parse('L()&M()')
        ]
        expr_cf = [
            parse('!S()')
        ]

        l_expr = [[]]
        r_expr = [[]]
        cf_expr = [[
            parse('S()')
        ]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, cf_expr, [])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!Q()'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L()&M()'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S()'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))
        self.assertIn(parse('S()'), sequent[BaseTableauxBuilder.certain_falsehood_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('!S()'), sequent[BaseTableauxBuilder.true_processed])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
    
    def test_merge_false_not(self):
        expr_t = [
            parse('P()&T()&F()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()'),
            parse('!S()->!Q()'),
            parse('L()&M()'),
        ]
        expr_cf = [
            parse('!S()')
        ]

        l_expr = [[
            parse('S()')
        ]]
        r_expr = [[]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf)
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, [])

        self.assertEqual(1, len(tableau.children))
        sequent = tableau.children[0].sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&F()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertIn(parse('S()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S()'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
    
    def test_merge_false_univq(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(A)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(D)->P(D)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['D'])

        self.assertEqual(1, len(tableau.children))
        sequent = tableau.children[0].sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('F(D)->P(D)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
    
    def test_merge_cf_univq(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('(A)x (F(x)->P(x))'),
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(D)->P(D)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, ['D'])

        self.assertEqual(1, len(tableau.children))
        sequent = tableau.children[0].sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('F(D)->P(D)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_true_univq_1(self):
        expr_t = [
            parse('(A)x (F(x)->P(x))'),
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[
            parse('F(A)->P(A)')
        ]]
        r_expr = [[]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, cf_expr, ['A'])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
    
    def test_merge_true_univq_2(self):
        expr_t = [
            parse('(A)x (F(x)->P(x))'),
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[
            parse('F(B)->P(B)')
        ]]
        r_expr = [[]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, cf_expr, ['B'])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_true_univq_3(self):
        expr_t = [
            parse('(A)x (F(x)->P(x))'),
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[
            parse('F(A)->P(A)'),
            parse('F(B)->P(B)'),
            parse('F(C)->P(C)'),
        ]]
        r_expr = [[]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, cf_expr, ['A', 'B', 'C'])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(6, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F(C)->P(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_false_exq_1(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(A)->P(A)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['A'])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_false_exq_2(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(B)->P(B)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['B'])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_false_exq_3(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(A)->P(A)'),
            parse('F(B)->P(B)'),
            parse('F(C)->P(C)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['A', 'B', 'C'])

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(6, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(C)->P(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_cf_exq_1(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(A)->P(A)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, ['A'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_cf_exq_2(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(B)->P(B)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, ['B'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_cf_exq_3(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(A)->P(A)'),
            parse('F(B)->P(B)'),
            parse('F(C)->P(C)'),
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, None, expr_cf[0]), l_expr, r_expr, cf_expr, ['A', 'B', 'C'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(6, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(C)->P(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_false_exq_1(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(A)->P(A)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['A'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_false_exq_2(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(B)->P(B)')
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['B'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_false_exq_3(self):
        expr_t = [
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('(E)x (F(x)->P(x))'),
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[]]
        r_expr = [[
            parse('F(A)->P(A)'),
            parse('F(B)->P(B)'),
            parse('F(C)->P(C)'),
        ]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((None, expr_f[0], None), l_expr, r_expr, cf_expr, ['A', 'B', 'C'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(6, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(A)->P(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(B)->P(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('F(C)->P(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))

    def test_merge_true_exq(self):
        expr_t = [
            parse('(E)x (F(x)->P(x))'),
            parse('P(A)&T(B)&F(C)'),
            parse('K(A)->R(B)'),
            parse('R(C)->S(A)'),
        ]
        expr_f = [
            parse('!S(C)'),
            parse('!S(A)->!Q(B)'),
            parse('L(B)&M(A)'),
        ]
        expr_cf = [
            parse('!S(A)')
        ]

        l_expr = [[
            parse('F(D)->P(D)')
        ]]
        r_expr = [[]]
        cf_expr = [[]]

        tableau = IfoplTableauxBuilder(true_exprs=expr_t,
                                     false_exprs=expr_f,
                                     cf_exprs = expr_cf,
                                     constants=['A', 'B', 'C'])
        manual_tableau = BaseManualTableau(LogicType.IFOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, cf_expr, ['D'])
        self.assertTrue(success)

        self.assertEqual(0, len(tableau.children))
        sequent = tableau.sequent

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K(A)->R(B)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R(C)->S(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(A)&T(B)&F(C)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('F(D)->P(D)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S(C)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('!S(A)->!Q(B)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('L(B)&M(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.certain_falsehood_exprs]))
        self.assertIn(parse('!S(A)'), sequent[BaseTableauxBuilder.certain_falsehood_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_atoms]))

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('(E)x (F(x)->P(x))'), sequent[BaseTableauxBuilder.true_processed])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.certain_falsehood_processed]))
