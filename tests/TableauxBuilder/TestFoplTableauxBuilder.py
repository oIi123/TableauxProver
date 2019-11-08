import unittest

from src.Model.FoplExpressionTree import *
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder


class TestFoplTableauxBuilder(unittest.TestCase):
    def run_builder(self, builder: FoplTableauxBuilder):
        while not builder.is_done():
            builder.visit()

    def test_not_closing_1(self):
        # P()
        tree = FoplExpressionTree(expr=Predicate("P", []))

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_2(self):
        # P()&P()
        expr = And(Predicate("P", []), Predicate("P", []))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_3(self):
        # (A)x P(x)&P(x)
        expr = AllQuantor(Var("x"), And(Predicate("P", [Var("x")]), Predicate("P", [Var("x")])))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_4(self):
        # P()|P()
        expr = Or(Predicate("P", []), Predicate("P", []))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_5(self):
        # (A)x P(x)|P(x)
        expr = AllQuantor(Var("x"), Or(Predicate("P", [Var("x")]), Predicate("P", [Var("x")])))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_6(self):
        # P()&K() | !P()&K()
        expr = Or(And(Predicate("P", []), Predicate("K", [])), And(Not(Predicate("P", [])), Predicate("K", [])))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_7(self):
        # (A)x P(x)&K(x) | !P(x)&K(x)
        expr = AllQuantor(Var("x"), Or(And(Predicate("P", [Var("x")]), Predicate("K", [Var("x")])), And(Not(Predicate("P", [Var("x")])), Predicate("K", [Var("x")]))))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_8(self):
        # (A)x !(P(x)<->P(x,x))
        expr = AllQuantor(Var("x"), Not(Eq(Predicate("P", [Var("x")]), Predicate("P", [Var("x"), Var("x")]))))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_closing_1(self):
        # !((E)x A(x)) -> (A)x !A(x)
        expr = Impl(Not(ExistentialQuantor(Var("x"), Predicate("A", [Var("x")]))), AllQuantor(Var("x"), Not(Predicate("A", [Var("x")]))))
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_2(self):
        # ((A)x (A(x) -> B(x))) -> (((A)x A(x)) -> ((A)x B(x)))
        expr = Impl(
            AllQuantor(Var("x"), Impl(Predicate("A", [Var("x")]), Predicate("B", [Var("x")]))),
            Impl(AllQuantor(Var("x"), Predicate("A", [Var("x")])), AllQuantor(Var("x"), Predicate("B", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_3(self):
        # ((A)x F(x)) -> ((A)y F(y))
        expr = Impl(
            AllQuantor(Var("x"), Predicate("F", [Var("x")])),
            AllQuantor(Var("y"), Predicate("F", [Var("y")]))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_7(self):
        # !((A)x F(x)) <-> ((E)x !F(x))
        expr = Eq(
            Not(AllQuantor(Var("x"), Predicate("F", [Var("x")]))),
            ExistentialQuantor(Var("x"), Not(Predicate("F", [Var("x")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    # Not yet terminating Tests:
    # TODO: Change FoplTreeBuilder to perform a breadth search instead of depth search
    """
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

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())
    """

    """
    def test_closing_13(self):
        # ((A)x (E)y F(x,y)) -> ((E)y (A)x F(x,y))
        expr = Impl(
            AllQuantor(Var("x"), ExistentialQuantor(Var("y"), Predicate("F", [Var("x"), Var("y")]))),
            ExistentialQuantor(Var("y"), AllQuantor(Var("x"), Predicate("F", [Var("x"), Var("y")])))
        )
        tree = FoplExpressionTree(expr=expr)

        builder = FoplTableauxBuilder(tree)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())
    """


if __name__ == '__main__':
    unittest.main()
