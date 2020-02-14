import unittest

from src.Model.FoplExpressionTree import *
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder


class TestFoplTableauxBuilder(unittest.TestCase):
    def test_not_closing_1(self):
        # P()
        tree = FoplExpressionTree(expr=Predicate("P", []))

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_2(self):
        # P()&P()
        expr = And(Predicate("P", []), Predicate("P", []))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_3(self):
        # (A)x P(x)&P(x)
        expr = AllQuantor(Var("x"), And(Predicate("P", [Var("x")]), Predicate("P", [Var("x")])))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_4(self):
        # P()|P()
        expr = Or(Predicate("P", []), Predicate("P", []))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_5(self):
        # (A)x P(x)|P(x)
        expr = AllQuantor(Var("x"), Or(Predicate("P", [Var("x")]), Predicate("P", [Var("x")])))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_6(self):
        # P()&K() | !P()&K()
        expr = Or(And(Predicate("P", []), Predicate("K", [])), And(Not(Predicate("P", [])), Predicate("K", [])))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_7(self):
        # (A)x P(x)&K(x) | !P(x)&K(x)
        expr = AllQuantor(Var("x"), Or(And(Predicate("P", [Var("x")]), Predicate("K", [Var("x")])), And(Not(Predicate("P", [Var("x")])), Predicate("K", [Var("x")]))))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_8(self):
        # (A)x !(P(x)<->P(x,x))
        expr = AllQuantor(Var("x"), Not(Eq(Predicate("P", [Var("x")]), Predicate("P", [Var("x"), Var("x")]))))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_closing_1(self):
        # !((E)x A(x)) -> (A)x !A(x)
        expr = Impl(Not(ExistentialQuantor(Var("x"), Predicate("A", [Var("x")]))), AllQuantor(Var("x"), Not(Predicate("A", [Var("x")]))))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_2(self):
        # ((A)x (A(x) -> B(x))) -> (((A)x A(x)) -> ((A)x B(x)))
        expr = Impl(
            AllQuantor(Var("x"), Impl(Predicate("A", [Var("x")]), Predicate("B", [Var("x")]))),
            Impl(AllQuantor(Var("x"), Predicate("A", [Var("x")])), AllQuantor(Var("x"), Predicate("B", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_3(self):
        # ((A)x F(x)) -> ((A)y F(y))
        expr = Impl(
            AllQuantor(Var("x"), Predicate("F", [Var("x")])),
            AllQuantor(Var("y"), Predicate("F", [Var("y")]))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_4(self):
        # ((A)x M(x) -> P(x))&((A)x S(x) -> M(x)) -> ((A)x S(x) -> P(x))
        expr = Impl(
            And(
                AllQuantor(Var("x"), Impl(Predicate("M", [Var("x")]), Predicate("P", [Var("x")]))),
                AllQuantor(Var("x"), Impl(Predicate("S", [Var("x")]), Predicate("M", [Var("x")])))
            ),
            AllQuantor(Var("x"), Impl(Predicate("S", [Var("x")]), Predicate("P", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_5(self):
        # ((A)x P(x)->!M(x))&((E)x (S(x)&M(x))) -> ((E)x S(x)&!P(x))
        expr = Impl(
            And(
                AllQuantor(Var("x"), Impl(Predicate("P", [Var("x")]), Not(Predicate("M", [Var("x")])))),
                ExistentialQuantor(Var("x"), And(Predicate("S", [Var("x")]), Predicate("M", [Var("x")])))
            ),
            ExistentialQuantor(Var("x"), And(Predicate("S", [Var("x")]), Not(Predicate("P", [Var("x")]))))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_6(self):
        # ((A)x P(x)->!M(x))&((E)x (S(x)&M(x))) -> ((E)x S(x)&!P(x))
        expr = Impl(
            And(
                AllQuantor(Var("x"), Impl(Predicate("P", [Var("x")]), Not(Predicate("M", [Var("x")])))),
                ExistentialQuantor(Var("x"), And(Predicate("S", [Var("x")]), Predicate("M", [Var("x")])))
            ),
            ExistentialQuantor(Var("x"), And(Predicate("S", [Var("x")]), Not(Predicate("P", [Var("x")]))))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_7(self):
        # !((A)x F(x)) <-> ((E)x !F(x))
        expr = Eq(
            Not(AllQuantor(Var("x"), Predicate("F", [Var("x")]))),
            ExistentialQuantor(Var("x"), Not(Predicate("F", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_8(self):
        # (((E)x F(x)) -> ((A)x G(x))) -> ((A)x F(x) -> G(x))
        expr = Impl(
            Impl(
                ExistentialQuantor(Var("x"), Predicate("F", [Var("x")])),
                AllQuantor(Var("x"), Predicate("G", [Var("x")]))
            ),
            AllQuantor(Var("x"), Impl(Predicate("F", [Var("x")]), Predicate("G", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_9(self):
        # ((A)x F(x)&G(x)) <-> (((A)x F(x))&((A)x G(x)))
        expr = Eq(
            AllQuantor(Var("x"), And(Predicate("F", [Var("x")]), Predicate("G", [Var("x")]))),
            And(
                AllQuantor(Var("x"), Predicate("F", [Var("x")])),
                AllQuantor(Var("x"), Predicate("G", [Var("x")]))
            )
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_10(self):
        # (((A)x F(x))|((A)x G(x))) -> ((A)x F(x)|G(x))
        expr = Impl(
            Or(
                AllQuantor(Var("x"), Predicate("F", [Var("x")])),
                AllQuantor(Var("x"), Predicate("G", [Var("x")]))
            ),
            AllQuantor(Var("x"), Or(Predicate("F", [Var("x")]), Predicate("G", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_11(self):
        # ((E)x F(x)&G(x)) -> (((E)x F(x))&((E)x G(x)))
        expr = Impl(
            ExistentialQuantor(Var("x"), And(Predicate("F", [Var("x")]), Predicate("G", [Var("x")]))),
            And(
                ExistentialQuantor(Var("x"), Predicate("F", [Var("x")])),
                ExistentialQuantor(Var("x"), Predicate("G", [Var("x")]))
            )
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_12(self):
        # ((E)x F(x)|G(x)) <-> (((E)x F(x))|((E)x G(x)))
        expr = Eq(
            ExistentialQuantor(Var("x"), Or(Predicate("F", [Var("x")]), Predicate("G", [Var("x")]))),
            Or(
                ExistentialQuantor(Var("x"), Predicate("F", [Var("x")])),
                ExistentialQuantor(Var("x"), Predicate("G", [Var("x")]))
            )
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_exprs=[tree.expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_13(self):
        # T (A)x,y M(x, l(x,y))     F M(A,l(A,l(B,NIL)))
        true_expr = AllQuantor(Var("x"),
            AllQuantor(Var("y"),
                Predicate("M",[
                    Var("x"),
                    Func("l", [Var("x"), Var("y")])
                ])
            )
        )

        false_expr = Predicate("M",[
            Const("A"),
            Func("l", [
                Const("A"),
                Func("l", [
                    Const("B"),
                    Const("NIL")
                ])
            ])
        ])

        constants = ["A", "B", "NIL"]
        functions = [("l", 2)]

        builder = FoplTableauxBuilder(true_exprs=[true_expr],
                                      false_exprs=[false_expr],
                                      constants=constants,
                                      functions=functions)
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_permute_functions_1(self):
        consts = ["X", "Y"]
        funs = [("l", 2)]

        expected = [
            Func("l", [Const("X"), Const("X")]),
            Func("l", [Const("X"), Const("Y")]),
            Func("l", [Const("Y"), Const("X")]),
            Func("l", [Const("Y"), Const("Y")]),
            Const("X"),
            Const("Y"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_2(self):
        consts = ["X"]
        funs = [("l", 2)]

        expected = [
            Func("l", [Const("X"), Const("X")]),
            Const("X"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_3(self):
        consts = ["X"]
        funs = [("l", 1)]

        expected = [
            Func("l", [Const("X")]),
            Const("X"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_4(self):
        consts = ["X"]
        funs = [("l", 1)]

        expected = [
            Func("l", [Const("X")]),
            Func("l", [Func("l", [Const("X")])]),
            Const("X"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 1
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_5(self):
        consts = ["X", "Y"]
        funs = [("l", 1)]

        expected = [
            Func("l", [Const("X")]),
            Func("l", [Const("Y")]),
            Func("l", [Func("l", [Const("X")])]),
            Func("l", [Func("l", [Const("Y")])]),
            Const("X"),
            Const("Y"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 1
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_6(self):
        consts = ["X", "Y"]
        funs = [("l", 2)]

        expected = [
            Const("X"),
            Const("Y"),
            Func("l", [Const("X"), Const("X")]),
            Func("l", [Const("X"), Const("Y")]),
            Func("l", [Const("Y"), Const("X")]),
            Func("l", [Const("Y"), Const("Y")]),

            Func("l", [Func("l", [Const("X"), Const("X")]), Const("X")]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Const("X")]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Const("X")]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Const("X")]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Const("Y")]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Const("Y")]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Const("Y")]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Const("Y")]),

            Func("l", [Const("X"), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Const("X"), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Const("X"), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Const("X"), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Const("Y"), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Const("Y"), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Const("Y"), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Const("Y"), Func("l", [Const("Y"), Const("Y")])]),

            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("Y"), Const("Y")])]),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 1
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)

    def test_permute_functions_7(self):
        consts = ["X"]
        funs = [("l", 1), ("j", 1)]

        expected = [
            Func("l", [Const("X")]),
            Func("j", [Const("X")]),
            Const("X"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_8(self):
        consts = ["X", "Y"]
        funs = [("l", 1), ("j", 1)]

        expected = [
            Func("l", [Const("X")]),
            Func("l", [Const("Y")]),
            Func("j", [Const("X")]),
            Func("j", [Const("Y")]),
            Const("X"),
            Const("Y"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_9(self):
        consts = ["X", "Y"]
        funs = [("l", 2), ("j", 1)]

        expected = [
            Func("l", [Const("X"), Const("X")]),
            Func("l", [Const("X"), Const("Y")]),
            Func("l", [Const("Y"), Const("X")]),
            Func("l", [Const("Y"), Const("Y")]),
            Func("j", [Const("X")]),
            Func("j", [Const("Y")]),
            Const("X"),
            Const("Y"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_10(self):
        consts = ["X", "Y"]
        funs = [("l", 2), ("j", 2)]

        expected = [
            Func("l", [Const("X"), Const("X")]),
            Func("l", [Const("X"), Const("Y")]),
            Func("l", [Const("Y"), Const("X")]),
            Func("l", [Const("Y"), Const("Y")]),
            Func("j", [Const("X"), Const("X")]),
            Func("j", [Const("X"), Const("Y")]),
            Func("j", [Const("Y"), Const("X")]),
            Func("j", [Const("Y"), Const("Y")]),
            Const("X"),
            Const("Y"),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)

    def test_permute_functions_11(self):
        consts = ["X", "Y"]
        funs = [("l", 2), ("j", 1)]

        expected = [
            Const("X"),
            Const("Y"),
            Func("j", [Const("X")]),
            Func("j", [Const("Y")]),
            Func("l", [Const("X"), Const("X")]),
            Func("l", [Const("X"), Const("Y")]),
            Func("l", [Const("Y"), Const("X")]),
            Func("l", [Const("Y"), Const("Y")]),

            Func("j", [Func("j", [Const("X")])]),
            Func("j", [Func("j", [Const("Y")])]),
            Func("j", [Func("l", [Const("X"), Const("X")])]),
            Func("j", [Func("l", [Const("X"), Const("Y")])]),
            Func("j", [Func("l", [Const("Y"), Const("X")])]),
            Func("j", [Func("l", [Const("Y"), Const("Y")])]),

            Func("l", [Const("X"), Func("j", [Const("X")])]),
            Func("l", [Const("X"), Func("j", [Const("Y")])]),
            Func("l", [Const("Y"), Func("j", [Const("X")])]),
            Func("l", [Const("Y"), Func("j", [Const("Y")])]),
            Func("l", [Func("j", [Const("X")]), Const("X")]),
            Func("l", [Func("j", [Const("X")]), Const("Y")]),
            Func("l", [Func("j", [Const("Y")]), Const("X")]),
            Func("l", [Func("j", [Const("Y")]), Const("Y")]),

            Func("l", [Func("j", [Const("X")]), Func("j", [Const("X")])]),
            Func("l", [Func("j", [Const("X")]), Func("j", [Const("Y")])]),
            Func("l", [Func("j", [Const("Y")]), Func("j", [Const("X")])]),
            Func("l", [Func("j", [Const("Y")]), Func("j", [Const("Y")])]),

            Func("l", [Const("X"), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Const("X"), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Const("X"), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Const("X"), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Const("Y"), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Const("Y"), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Const("Y"), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Const("Y"), Func("l", [Const("Y"), Const("Y")])]),

            Func("l", [Func("l", [Const("X"), Const("X")]), Const("X")]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Const("X")]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Const("X")]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Const("X")]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Const("Y")]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Const("Y")]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Const("Y")]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Const("Y")]),

            Func("l", [Func("j", [Const("X")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("j", [Const("X")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("j", [Const("X")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("j", [Const("X")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("j", [Const("Y")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("j", [Const("Y")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("j", [Const("Y")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("j", [Const("Y")]), Func("l", [Const("Y"), Const("Y")])]),

            Func("l", [Func("l", [Const("X"), Const("X")]), Func("j", [Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("j", [Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("j", [Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("j", [Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("j", [Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("j", [Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("j", [Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("j", [Const("Y")])]),

            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("X")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("X"), Const("Y")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("X")]), Func("l", [Const("Y"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("X"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("X"), Const("Y")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("Y"), Const("X")])]),
            Func("l", [Func("l", [Const("Y"), Const("Y")]), Func("l", [Const("Y"), Const("Y")])]),
        ]

        builder = FoplTableauxBuilder(constants=consts,
                                      functions=funs)
        builder.function_depth = 1
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)

    def test_permute_functions_12(self):
        consts = ["X", "Y"]

        expected = [
            Const("X"),
            Const("Y"),
        ]

        builder = FoplTableauxBuilder(constants=consts)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_13(self):
        consts = ["X"]

        expected = [
            Const("X"),
        ]

        builder = FoplTableauxBuilder(constants=consts)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)
    
    def test_permute_functions_14(self):
        consts = ["X", "Y", "Z"]

        expected = [
            Const("X"),
            Const("Y"),
            Const("Z"),
        ]

        builder = FoplTableauxBuilder(constants=consts)
        builder.function_depth = 0
        perms = builder.calculate_functions()

        self.assertEqual(len(expected), len(perms))
        for exp in expected:
            self.assertIn(exp, perms)

# This test does not terminate
"""
    def test_not_closing_9(self):
        # ((A)x (E)y F(x,y)) -> ((E)y (A)x F(x,y))
        expr = Impl(
            AllQuantor(Var("x"), ExistentialQuantor(Var("y"), Predicate("F", [Var("x"), Var("y")]))),
            ExistentialQuantor(Var("y"), AllQuantor(Var("x"), Predicate("F", [Var("x"), Var("y")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(false_expr=[tree.expr])
        builder.auto_resolve(True)

        self.assertTrue(builder.is_closed())
"""

if __name__ == '__main__':
    unittest.main()
