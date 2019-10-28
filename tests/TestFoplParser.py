import unittest

from antlr4 import RecognitionException

from src.Model.FoplExpressionTree import Predicate, Var, Func, Not, And, Or, Impl, Eq, AllQuantor, ExistentialQuantor
from src.Parser.FoplParser import FoplParser


class TestCorrectFoplParser(unittest.TestCase):
    def test_atom_1(self):
        wff = "P()"
        expr = Predicate("P", [])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_2(self):
        wff = "Person(x)"
        expr = Predicate("Person", [Var("x")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_3(self):
        wff = "Person(x,y,z)"
        expr = Predicate("Person", [Var("x"), Var("y"), Var("z")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_4(self):
        wff = "Person( x, y, z)"
        expr = Predicate("Person", [Var("x"), Var("y"), Var("z")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_5(self):
        wff = "Person(f())"
        expr = Predicate("Person", [Func("f", [])])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_6(self):
        wff = "Person(f(x,y,z))"
        expr = Predicate("Person", [Func("f", [Var("x"), Var("y"), Var("z")])])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_7(self):
        wff = "Person(a,f(x,g(y,z)),b)"
        expr = Predicate("Person", [Var("a"), Func("f", [Var("x"), Func("g", [Var("y"), Var("z")])]), Var("b")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_not_1(self):
        wff = "!Person(a)"
        expr = Not(Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_not_2(self):
        wff = "! Person(a)"
        expr = Not(Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_not_3(self):
        wff = "!!Person(a)"
        expr = Not(Not(Predicate("Person", [Var("a")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_and_1(self):
        wff = "Person(a)&Person(b)"
        expr = And(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_and_2(self):
        wff = "Person(a) &Person(b)"
        expr = And(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_and_3(self):
        wff = "Person(a) & Person(b)"
        expr = And(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_or_1(self):
        wff = "Person(a)|Person(b)"
        expr = Or(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_or_2(self):
        wff = "Person(a) |Person(b)"
        expr = Or(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_or_3(self):
        wff = "Person(a) | Person(b)"
        expr = Or(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_impl_1(self):
        wff = "Person(a)->Person(b)"
        expr = Impl(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_impl_2(self):
        wff = "Person(a) ->Person(b)"
        expr = Impl(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_impl_3(self):
        wff = "Person(a) -> Person(b)"
        expr = Impl(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_eq_1(self):
        wff = "Person(a)<->Person(b)"
        expr = Eq(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_eq_2(self):
        wff = "Person(a) <->Person(b)"
        expr = Eq(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_eq_3(self):
        wff = "Person(a) <-> Person(b)"
        expr = Eq(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_all_quant_1(self):
        wff = "(A)a Person(a)"
        expr = AllQuantor([Var("a")], Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_all_quant_2(self):
        wff = "(A)a,b Person(a)"
        expr = AllQuantor([Var("a"), Var("b")], Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_all_quant_3(self):
        wff = "(A)a , b Person(a)"
        expr = AllQuantor([Var("a"), Var("b")], Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_ex_quant_1(self):
        wff = "(E)a Person(a)"
        expr = ExistentialQuantor([Var("a")], Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_ex_quant_2(self):
        wff = "(E)a,b Person(a)"
        expr = ExistentialQuantor([Var("a"), Var("b")], Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_ex_quant_3(self):
        wff = "(E)a , b Person(a)"
        expr = ExistentialQuantor([Var("a"), Var("b")], Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_clamp_1(self):
        wff = "(Person(a))"
        expr = Predicate("Person", [Var("a")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_clamp_2(self):
        wff = "( Person(a) )"
        expr = Predicate("Person", [Var("a")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_complex_1(self):
        wff = "(A)a (E)b Person(a)&Person(b)->Parent(a,b)"
        expr = AllQuantor(
            [Var("a")],
            ExistentialQuantor(
                [Var("b")],
                Impl(
                    And(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")])),
                    Predicate("Parent", [Var("a"), Var("b")])
                )
            )
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_complex_2(self):
        wff = "(A)a,b (E)c Person(a)&Person(b)&Person(c)&Parent(a,b)&Parent(b,c)->Grandparent(a,c)"
        expr = AllQuantor(
            [Var("a"), Var("b")],
            ExistentialQuantor(
                [Var("c")],
                Impl(
                    And(
                        And(
                            And(
                                And(
                                    Predicate("Person", [Var("a")]),
                                    Predicate("Person", [Var("b")])
                                ),
                                Predicate("Person", [Var("c")])
                            ),
                            Predicate("Parent", [Var("a"), Var("b")])
                        ),
                        Predicate("Parent", [Var("b"), Var("c")])
                    ),
                    Predicate("Grandparent", [Var("a"), Var("c")])
                )
            )
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_complex_3(self):
        wff = "(P(a)->K(f(a,b))&P(c))<->!(E(c,d)|K(a))"
        expr = Eq(
            Impl(
                Predicate("P", [Var("a")]),
                And(
                    Predicate("K", [Func("f", [Var("a"), Var("b")])]),
                    Predicate("P", [Var("c")])
                )
            ),
            Not(
                Or(
                    Predicate("E", [Var("c"), Var("d")]),
                    Predicate("K", [Var("a")])
                )
            )
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_complex_4(self):
        wff = "P(a)|P(b)&P(c)|P(d)"
        expr = Or(
            Or(
                Predicate("P", [Var("a")]),
                And(
                    Predicate("P", [Var("b")]),
                    Predicate("P", [Var("c")])
                )
            ),
            Predicate("P", [Var("d")])
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)


class TestIncorrectFoplParser(unittest.TestCase):
    def test_atom_1(self):
        nwff = "P("
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_2(self):
        nwff = "P)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_3(self):
        nwff = "P(x,)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_4(self):
        nwff = "P(x,f()"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_5(self):
        nwff = "P(x,f(x,))"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)


if __name__ == '__main__':
    unittest.main()
