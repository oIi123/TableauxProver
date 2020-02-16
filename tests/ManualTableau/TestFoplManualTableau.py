import unittest

from src.builder_factory import LogicType
from src.Parser.FoplParser import FoplParser
from src.TableauxBuilder.BaseManualTableau import BaseManualTableau, BaseTableauxBuilder
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder


def parse(expr: str):
    return FoplParser.parse(expr).expr

class TestFoplManualTableau(unittest.TestCase):
    def test_incorrect_1(self):
        expr = parse('(P()->T())&(T()->Q())->(P()->Q())')

        l_expr = [
            parse('(P()->T())&(T()->Q())'),
            parse('(P()->Q())'),
        ]

        tableau = FoplTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [[]], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_2(self):
        expr = parse('(P()->T())&(T()->Q())->(P()->Q())')

        l_expr = [
            parse('(P()->T())&(T()->Q())'),
            parse('(P()->Q())'),
        ]

        r_expr = [
            parse('(P()->Q())'),
        ]

        tableau = FoplTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_3(self):
        expr = parse('(P()->T())&(T()->Q())->(P()->Q())')

        l_expr = [
            parse('(P()->T())&(T()->Q())'),
        ]

        r_expr = [
            parse('(T()->Q())'),
        ]

        tableau = FoplTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)

    def test_incorrect_4(self):
        expr_t = parse('(P()->T())&(T()->Q())->(P()->Q())')
        expr_f = parse('(P()->T())&(T()->Q())->(P()->Q())')

        l_expr = [
            parse('(P()->T())&(T()->Q())'),
        ]

        r_expr = [
            parse('(P()->Q())'),
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_5(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = []

        r_expr = [
            parse('P()'),
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_6(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = [
            parse('P()'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_7(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(C)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertFalse(success)
    
    def test_incorrect_8(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(C)|T(C)')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertFalse(success)
    
    def test_incorrect_9(self):
        expr_t = parse('P(A)|T(B)')
        expr_f = parse('(A)x P(x)')

        l_expr = []

        r_expr = [
            parse('P(A)'),
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertFalse(success)
    
    def test_incorrect_10(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(A)|T(A)')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertFalse(success)
    
    def test_incorrect_11(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(C)|T(D)')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C', 'D'])

        self.assertFalse(success)
    
    def test_incorrect_12(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(B)')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertFalse(success)

    def test_incorrect_13(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(A)&T(B)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertFalse(success)

    def test_incorrect_14(self):
        expr_t = parse('(A)x,y M(x,l(x,y))')
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('(A)y M(A,l(B,y))')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t],
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertFalse(success)

    def test_correct_1(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = []

        r_expr = [
            parse('!P()')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_correct_2(self):
        expr_t = parse('!!P()')
        expr_f = parse('P()|T()')

        l_expr = []

        r_expr = [
            parse('P()'),
            parse('T()')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_3(self):
        expr_t = parse('!!P()')
        expr_f = parse('(P()->T())&(T()->Q())->(P()->Q())')

        l_expr = [
            parse('(P()->T())&(T()->Q())')
        ]

        r_expr = [
            parse('(P()->Q())')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_4(self):
        expr_t = [
            parse('F()->K()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            parse('!S()')
        ]

        r_expr = [
            parse('!F()')
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f[0], None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_correct_5(self):
        expr_t = [
            parse('F()->K()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            [parse('K()')], []
        ]

        r_expr = [
            [], [parse('F()')]
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_6(self):
        expr_t = [
            parse('F()->K()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            [], [parse('K()')]
        ]

        r_expr = [
            [parse('F()')], []
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_7(self):
        expr_t = [
            parse('P()|T()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            [parse('T()')], [parse('P()')]
        ]

        r_expr = [
            [], []
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_8(self):
        expr_t = [
            parse('P()|T()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            [parse('P()')], [parse('T()')]
        ]

        r_expr = [
            [], []
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)

    def test_correct_9(self):
        expr_t = [
            parse('P()&T()&Q()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            parse('P()'),
            parse('T()&Q()')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_10(self):
        expr_t = [
            parse('P()&T()&Q()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            parse('P()&T()'),
            parse('Q()')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_correct_11(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(A)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertTrue(success)
    
    def test_correct_12(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(B)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['B'])

        self.assertTrue(success)
    
    def test_correct_13(self):
        expr_t = parse('(A)x P(x)')
        expr_f = parse('P(A)|T(B)')

        l_expr = [
            parse('P(A)'),
            parse('P(B)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertTrue(success)

    def test_correct_14(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(A)')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertTrue(success)
    
    def test_correct_15(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(B)|T(B)')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['B'])

        self.assertTrue(success)
    
    def test_correct_16(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(A)'),
            parse('P(B)|T(B)'),
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        self.assertTrue(success)

    def test_correct_17(self):
        expr_t = parse('P(A)|T(B)')
        expr_f = parse('(A)x P(x)')

        l_expr = []

        r_expr = [
            parse('P(C)'),
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertTrue(success)
    
    def test_correct_18(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(C)|T(C)')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C'])

        self.assertTrue(success)
    
    def test_correct_19(self):
        expr_t = parse('(A)x,y M(x,l(x,y))')
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('(A)y M(A,l(A, y))')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t],
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        self.assertTrue(success)
    
    def test_correct_20(self):
        expr_t = [
            parse('(A)x,y M(x,l(x,y))'),
            parse('(A)y M(A,l(A,y))'),
        ]
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('M(A,l(A,l(B,NIL)))')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=expr_t,
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[1], None, None), [l_expr], [r_expr], [[]], ['A', 'B', 'NIL'])

        self.assertTrue(success)
    
    def test_correct_21(self):
        expr_t = [
            parse('(A)x,y M(x,l(x,y))'),
            parse('(A)y M(A,l(A,y))'),
        ]
        expr_f = parse('M(A,l(A,l(B,NIL)))')

        l_expr = [
            parse('M(A,l(A,l(A,l(B,NIL))))')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=expr_t,
                                      false_exprs=[expr_f],
                                      constants=['A', 'B', 'NIL'],
                                      functions=[('l', 2)])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        success = manual_tableau.merge((expr_t[1], None, None), [l_expr], [r_expr], [[]], ['A', 'B', 'NIL'])

        self.assertTrue(success)

    def test_merge_1(self):
        expr_t = [
            parse('P()&T()&Q()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            parse('P()&T()'),
            parse('Q()')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('Q()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!F()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('P()&T()&Q()'), sequent[BaseTableauxBuilder.true_processed])

        self.assertEqual(0, len(tableau.children))

    def test_merge_2(self):
        expr_t = [
            parse('P()&T()&Q()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            parse('T()&Q()'),
            parse('P()')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('T()&Q()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!S()->!F()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('P()&T()&Q()'), sequent[BaseTableauxBuilder.true_processed])

        self.assertEqual(0, len(tableau.children))


    def test_merge_3(self):
        expr_t = [
            parse('P()&T()&Q()'),
            parse('K()->R()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            parse('!S()')
        ]

        r_expr = [
            parse('!F()')
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((None, expr_f[0], None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('!S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&Q()'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!F()'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertIn(parse('!S()->!F()'), sequent[BaseTableauxBuilder.false_processed])

        self.assertEqual(0, len(tableau.children))

    def test_merge_4(self):
        expr_t = [
            parse('K()->R()'),
            parse('P()&T()&Q()'),
            parse('R()->S()'),
        ]
        expr_f = [
            parse('!S()->!F()')
        ]

        l_expr = [
            [], [parse('R()')],
        ]

        r_expr = [
            [parse('K()')], [],
        ]

        tableau = FoplTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        sequent = tableau.sequent

        self.assertEqual(2, len(tableau.children))

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('R()->S()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&Q()'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('K()->R()'), sequent[BaseTableauxBuilder.true_processed])

        c_s_1 = tableau.children[0].sequent
        c_s_2 = tableau.children[1].sequent

        self.assertEqual(2, len(c_s_1[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('R()->S()'), c_s_1[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&Q()'), c_s_1[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(c_s_1[BaseTableauxBuilder.false_atoms]))
        self.assertIn(parse('K()'), c_s_1[BaseTableauxBuilder.false_atoms])
        self.assertEqual(0, len(c_s_1[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(c_s_1[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(c_s_1[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('K()->R()'), c_s_1[BaseTableauxBuilder.true_processed])

        self.assertEqual(2, len(c_s_2[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('R()->S()'), c_s_2[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P()&T()&Q()'), c_s_2[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(c_s_2[BaseTableauxBuilder.true_atoms]))
        self.assertIn(parse('R()'), c_s_2[BaseTableauxBuilder.true_atoms])
        self.assertEqual(0, len(c_s_2[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(c_s_2[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(c_s_2[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('K()->R()'), c_s_2[BaseTableauxBuilder.true_processed])

    def test_merge_5(self):
        expr_t = parse('(E)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(C)|T(C)')
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['C'])

        sequent = tableau.sequent

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('P(C)|T(C)'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('P(A)&F(B)'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('(E)x (P(x)|T(x))'), sequent[BaseTableauxBuilder.true_processed])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions]))

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.established_constants]))
        self.assertIn('A', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('B', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('C', sequent[BaseTableauxBuilder.established_constants])

        self.assertEqual(0, len(tableau.children))
    
    def test_merge_6(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(A)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(C)|T(C)')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['C'])

        sequent = tableau.sequent

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('P(C)|T(C)'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('P(A)&F(B)'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertIn(parse('(A)x (P(x)|T(x))'), sequent[BaseTableauxBuilder.false_processed])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions]))

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.established_constants]))
        self.assertIn('A', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('B', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('C', sequent[BaseTableauxBuilder.established_constants])

        self.assertEqual(0, len(tableau.children))

    def test_merge_7(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(A)')
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A'])

        sequent = tableau.sequent

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('P(A)&F(B)'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('P(A)|T(A)'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions]))
        self.assertIn(parse('(E)x (P(x)|T(x))'), sequent[BaseTableauxBuilder.processed_false_quantor_expressions])
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions][parse('(E)x (P(x)|T(x))')]))
        self.assertIn('A', sequent[BaseTableauxBuilder.processed_false_quantor_expressions][parse('(E)x (P(x)|T(x))')])

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.established_constants]))
        self.assertIn('A', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('B', sequent[BaseTableauxBuilder.established_constants])

        self.assertEqual(0, len(tableau.children))

    def test_merge_8(self):
        expr_t = parse('P(A)&F(B)')
        expr_f = parse('(E)x (P(x)|T(x))')

        l_expr = []

        r_expr = [
            parse('P(A)|T(A)'),
            parse('P(B)|T(B)'),
        ]

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        sequent = tableau.sequent

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('P(A)&F(B)'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('P(A)|T(A)'), sequent[BaseTableauxBuilder.false_exprs])
        self.assertIn(parse('P(B)|T(B)'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions]))
        self.assertIn(parse('(E)x (P(x)|T(x))'), sequent[BaseTableauxBuilder.processed_false_quantor_expressions])
        self.assertEqual(2, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions][parse('(E)x (P(x)|T(x))')]))
        self.assertIn('A', sequent[BaseTableauxBuilder.processed_false_quantor_expressions][parse('(E)x (P(x)|T(x))')])
        self.assertIn('B', sequent[BaseTableauxBuilder.processed_false_quantor_expressions][parse('(E)x (P(x)|T(x))')])

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.established_constants]))
        self.assertIn('A', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('B', sequent[BaseTableauxBuilder.established_constants])

        self.assertEqual(0, len(tableau.children))

    def test_merge_9(self):
        expr_t = parse('(A)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(A)|T(A)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A'])

        sequent = tableau.sequent

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('P(A)|T(A)'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('P(A)&F(B)'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions]))
        self.assertIn(parse('(A)x (P(x)|T(x))'), sequent[BaseTableauxBuilder.processed_true_quantor_expressions])
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions][parse('(A)x (P(x)|T(x))')]))
        self.assertIn('A', sequent[BaseTableauxBuilder.processed_true_quantor_expressions][parse('(A)x (P(x)|T(x))')])

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.established_constants]))
        self.assertIn('A', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('B', sequent[BaseTableauxBuilder.established_constants])

        self.assertEqual(0, len(tableau.children))
    
    def test_merge_10(self):
        expr_t = parse('(A)x (P(x)|T(x))')
        expr_f = parse('P(A)&F(B)')

        l_expr = [
            parse('P(A)|T(A)'),
            parse('P(B)|T(B)'),
        ]

        r_expr = []

        tableau = FoplTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f], constants=['A', 'B'])
        manual_tableau = BaseManualTableau(LogicType.FOPL, tableau)

        manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], ['A', 'B'])

        sequent = tableau.sequent

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('P(A)|T(A)'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('P(B)|T(B)'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('P(A)&F(B)'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.processed_false_quantor_expressions]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions]))
        self.assertIn(parse('(A)x (P(x)|T(x))'), sequent[BaseTableauxBuilder.processed_true_quantor_expressions])
        self.assertEqual(2, len(sequent[BaseTableauxBuilder.processed_true_quantor_expressions][parse('(A)x (P(x)|T(x))')]))
        self.assertIn('A', sequent[BaseTableauxBuilder.processed_true_quantor_expressions][parse('(A)x (P(x)|T(x))')])
        self.assertIn('B', sequent[BaseTableauxBuilder.processed_true_quantor_expressions][parse('(A)x (P(x)|T(x))')])

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.established_constants]))
        self.assertIn('A', sequent[BaseTableauxBuilder.established_constants])
        self.assertIn('B', sequent[BaseTableauxBuilder.established_constants])

        self.assertEqual(0, len(tableau.children))
