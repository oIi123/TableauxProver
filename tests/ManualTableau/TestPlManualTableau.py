import unittest

from src.builder_factory import LogicType
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.BaseManualTableau import BaseManualTableau, BaseTableauxBuilder
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder


def parse(expr: str):
    return PropParser.parse(expr).expr

class TestPlManualTableau(unittest.TestCase):
    def test_incorrect_1(self):
        expr = parse('(a->b)&(b->c)->(a->c)')

        l_expr = [
            parse('(a->b)&(b->c)'),
            parse('(a->c)'),
        ]

        tableau = IpcTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [[]], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_2(self):
        expr = parse('(a->b)&(b->c)->(a->c)')

        l_expr = [
            parse('(a->b)&(b->c)'),
            parse('(a->c)'),
        ]

        r_expr = [
            parse('(a->c)'),
        ]

        tableau = IpcTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_3(self):
        expr = parse('(a->b)&(b->c)->(a->c)')

        l_expr = [
            parse('(a->b)&(b->c)'),
        ]

        r_expr = [
            parse('(b->c)'),
        ]

        tableau = IpcTableauxBuilder(false_exprs=[expr])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)

    def test_incorrect_4(self):
        expr_t = parse('(a->b)&(b->c)->(a->c)')
        expr_f = parse('(a->b)&(b->c)->(a->c)')

        l_expr = [
            parse('(a->b)&(b->c)'),
        ]

        r_expr = [
            parse('(a->c)'),
        ]

        tableau = IpcTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_5(self):
        expr_t = parse('!!a')
        expr_f = parse('a|b')

        l_expr = []

        r_expr = [
            parse('a'),
        ]

        tableau = IpcTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_incorrect_6(self):
        expr_t = parse('!!a')
        expr_f = parse('a|b')

        l_expr = [
            parse('a'),
        ]

        r_expr = []

        tableau = IpcTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertFalse(success)
    
    def test_correct_1(self):
        expr_t = parse('!!a')
        expr_f = parse('a|b')

        l_expr = []

        r_expr = [
            parse('!a')
        ]

        tableau = IpcTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t, None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_correct_2(self):
        expr_t = parse('!!a')
        expr_f = parse('a|b')

        l_expr = []

        r_expr = [
            parse('a'),
            parse('b')
        ]

        tableau = IpcTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_3(self):
        expr_t = parse('!!a')
        expr_f = parse('(a->b)&(b->c)->(a->c)')

        l_expr = [
            parse('(a->b)&(b->c)')
        ]

        r_expr = [
            parse('(a->c)')
        ]

        tableau = IpcTableauxBuilder(true_exprs=[expr_t], false_exprs=[expr_f])
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr_f, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_4(self):
        expr_t = [
            parse('p->q'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            parse('!s')
        ]

        r_expr = [
            parse('!p')
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((None, expr_f[0], None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_correct_5(self):
        expr_t = [
            parse('p->q'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            [parse('q')], []
        ]

        r_expr = [
            [], [parse('p')]
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_6(self):
        expr_t = [
            parse('p->q'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            [], [parse('q')]
        ]

        r_expr = [
            [parse('p')], []
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_7(self):
        expr_t = [
            parse('a|b'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            [parse('b')], [parse('a')]
        ]

        r_expr = [
            [], []
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)
    
    def test_correct_8(self):
        expr_t = [
            parse('a|b'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            [parse('a')], [parse('b')]
        ]

        r_expr = [
            [], []
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        self.assertTrue(success)

    def test_correct_9(self):
        expr_t = [
            parse('a&b&c'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            parse('a'),
            parse('b&c')
        ]

        r_expr = []

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)
    
    def test_correct_10(self):
        expr_t = [
            parse('a&b&c'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            parse('a&b'),
            parse('c')
        ]

        r_expr = []

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        success = manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        self.assertTrue(success)

    def test_merge_1(self):
        expr_t = [
            parse('a&b&c'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            parse('a&b'),
            parse('c')
        ]

        r_expr = []

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('q->r'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('r->s'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('a&b'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('c'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!s->!p'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('a&b&c'), sequent[BaseTableauxBuilder.true_processed])

        self.assertEqual(0, len(tableau.children))

    def test_merge_2(self):
        expr_t = [
            parse('a&b&c'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            parse('b&c'),
            parse('a')
        ]

        r_expr = []

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        manual_tableau.merge((expr_t[0], None, None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(3, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('q->r'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('r->s'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('b&c'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('a'), sequent[BaseTableauxBuilder.true_atoms])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!s->!p'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('a&b&c'), sequent[BaseTableauxBuilder.true_processed])

        self.assertEqual(0, len(tableau.children))


    def test_merge_3(self):
        expr_t = [
            parse('a&b&c'),
            parse('q->r'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            parse('!s')
        ]

        r_expr = [
            parse('!p')
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        manual_tableau.merge((None, expr_f[0], None), [l_expr], [r_expr], [[]], [])

        sequent = tableau.sequent

        self.assertEqual(4, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('q->r'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('r->s'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('!s'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('a&b&c'), sequent[BaseTableauxBuilder.true_exprs])

        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_exprs]))
        self.assertIn(parse('!p'), sequent[BaseTableauxBuilder.false_exprs])

        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertIn(parse('!s->!p'), sequent[BaseTableauxBuilder.false_processed])

        self.assertEqual(0, len(tableau.children))

    def test_merge_4(self):
        expr_t = [
            parse('q->r'),
            parse('a&b&c'),
            parse('r->s'),
        ]
        expr_f = [
            parse('!s->!p')
        ]

        l_expr = [
            [], [parse('r')],
        ]

        r_expr = [
            [parse('q')], [],
        ]

        tableau = IpcTableauxBuilder(true_exprs=expr_t, false_exprs=expr_f)
        manual_tableau = BaseManualTableau(LogicType.PROPOSITIONAL, tableau)

        manual_tableau.merge((expr_t[0], None, None), l_expr, r_expr, [[],[]], [])

        sequent = tableau.sequent

        self.assertEqual(2, len(tableau.children))

        self.assertEqual(2, len(sequent[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('r->s'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('a&b&c'), sequent[BaseTableauxBuilder.true_exprs])
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(sequent[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(sequent[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('q->r'), sequent[BaseTableauxBuilder.true_processed])

        c_s_1 = tableau.children[0].sequent
        c_s_2 = tableau.children[1].sequent

        self.assertEqual(2, len(c_s_1[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('r->s'), c_s_1[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('a&b&c'), c_s_1[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(c_s_1[BaseTableauxBuilder.false_atoms]))
        self.assertIn(parse('q'), c_s_1[BaseTableauxBuilder.false_atoms])
        self.assertEqual(0, len(c_s_1[BaseTableauxBuilder.true_atoms]))
        self.assertEqual(0, len(c_s_1[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(c_s_1[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('q->r'), c_s_1[BaseTableauxBuilder.true_processed])

        self.assertEqual(2, len(c_s_2[BaseTableauxBuilder.true_exprs]))
        self.assertIn(parse('r->s'), c_s_2[BaseTableauxBuilder.true_exprs])
        self.assertIn(parse('a&b&c'), c_s_2[BaseTableauxBuilder.true_exprs])
        self.assertEqual(1, len(c_s_2[BaseTableauxBuilder.true_atoms]))
        self.assertIn(parse('r'), c_s_2[BaseTableauxBuilder.true_atoms])
        self.assertEqual(0, len(c_s_2[BaseTableauxBuilder.false_atoms]))
        self.assertEqual(0, len(c_s_2[BaseTableauxBuilder.false_processed]))
        self.assertEqual(1, len(c_s_2[BaseTableauxBuilder.true_processed]))
        self.assertIn(parse('q->r'), c_s_2[BaseTableauxBuilder.true_processed])
