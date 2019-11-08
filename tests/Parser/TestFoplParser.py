import unittest

from antlr4 import RecognitionException

from src.Model.FoplExpressionTree import Predicate, Var, Func, Not, And, Or, Impl, Eq, AllQuantor, ExistentialQuantor, \
    Const
from src.Parser.FoplParser import FoplParser


class TestCorrectFoplParser(unittest.TestCase):
    def test_atom_1(self):
        wff = "P()"
        expr = Predicate("P", [])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_2(self):
        wff = "Person(X)"
        expr = Predicate("Person", [Const("X")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["X"])

    def test_atom_3(self):
        wff = "Person(X,Y,Z)"
        expr = Predicate("Person", [Const("X"), Const("Y"), Const("Z")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["X", "Y", "Z"])

    def test_atom_4(self):
        wff = "Person( X, Y, Z)"
        expr = Predicate("Person", [Const("X"), Const("Y"), Const("Z")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["X", "Y", "Z"])

    def test_atom_5(self):
        wff = "Person(f())"
        expr = Predicate("Person", [Func("f", [])])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_atom_6(self):
        wff = "Person(f(X,Y,Z))"
        expr = Predicate("Person", [Func("f", [Const("X"), Const("Y"), Const("Z")])])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["X", "Y", "Z"])

    def test_atom_7(self):
        wff = "Person(A,f(X,g(Y,Z)),B)"
        expr = Predicate("Person", [Const("A"), Func("f", [Const("X"), Func("g", [Const("Y"), Const("Z")])]), Const("B")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "X", "Y", "Z", "B"])

    def test_atom_8(self):
        wff = "(A)a Person(a,B)"
        expr = AllQuantor(Var("a"), Predicate("Person", [Var("a"), Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["B"])

    def test_atom_9(self):
        wff = "(A)a,b Person(a,b)"
        expr = AllQuantor(Var("a"), AllQuantor(Var("b"), Predicate("Person", [Var("a"), Var("b")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, [])

    def test_atom_10(self):
        wff = "(E)a Person(a,B)"
        expr = ExistentialQuantor(Var("a"), Predicate("Person", [Var("a"), Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["B"])

    def test_atom_11(self):
        wff = "(E)a,b Person(a,b)"
        expr = ExistentialQuantor(Var("a"), ExistentialQuantor(Var("b"), Predicate("Person", [Var("a"), Var("b")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, [])

    def test_not_1(self):
        wff = "!Person(A)"
        expr = Not(Predicate("Person", [Const("A")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A"])

    def test_not_2(self):
        wff = "! Person(A)"
        expr = Not(Predicate("Person", [Const("A")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A"])

    def test_not_3(self):
        wff = "!!Person(A)"
        expr = Not(Not(Predicate("Person", [Const("A")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A"])

    def test_and_1(self):
        wff = "Person(A)&Person(B)"
        expr = And(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_and_2(self):
        wff = "Person(A) &Person(B)"
        expr = And(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_and_3(self):
        wff = "Person(A) & Person(B)"
        expr = And(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_or_1(self):
        wff = "Person(A)|Person(B)"
        expr = Or(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_or_2(self):
        wff = "Person(A) |Person(B)"
        expr = Or(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_or_3(self):
        wff = "Person(A) | Person(B)"
        expr = Or(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_impl_1(self):
        wff = "Person(A)->Person(B)"
        expr = Impl(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_impl_2(self):
        wff = "Person(A) ->Person(B)"
        expr = Impl(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_impl_3(self):
        wff = "Person(A) -> Person(B)"
        expr = Impl(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_eq_1(self):
        wff = "Person(A)<->Person(B)"
        expr = Eq(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_eq_2(self):
        wff = "Person(A) <->Person(B)"
        expr = Eq(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_eq_3(self):
        wff = "Person(A) <-> Person(B)"
        expr = Eq(Predicate("Person", [Const("A")]), Predicate("Person", [Const("B")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B"])

    def test_all_quant_1(self):
        wff = "(A)a Person(a)"
        expr = AllQuantor(Var("a"), Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_all_quant_2(self):
        wff = "(A)a,b Person(a)"
        expr = AllQuantor(Var("a"), AllQuantor(Var("b"), Predicate("Person", [Var("a")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_all_quant_3(self):
        wff = "(A)a , b Person(a)"
        expr = AllQuantor(Var("a"), AllQuantor(Var("b"), Predicate("Person", [Var("a")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_ex_quant_1(self):
        wff = "(E)a Person(a)"
        expr = ExistentialQuantor(Var("a"), Predicate("Person", [Var("a")]))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_ex_quant_2(self):
        wff = "(E)a,b Person(a)"
        expr = ExistentialQuantor(Var("a"), ExistentialQuantor(Var("b"), Predicate("Person", [Var("a")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_ex_quant_3(self):
        wff = "(E)a , b Person(a)"
        expr = ExistentialQuantor(Var("a"), ExistentialQuantor(Var("b"), Predicate("Person", [Var("a")])))

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_clamp_1(self):
        wff = "(Person(A))"
        expr = Predicate("Person", [Const("A")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A"])

    def test_clamp_2(self):
        wff = "( Person(A) )"
        expr = Predicate("Person", [Const("A")])

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A"])

    def test_complex_1(self):
        wff = "(A)a (E)b (Person(a)&Person(b)->Parent(a,b))"
        expr = AllQuantor(
            Var("a"),
            ExistentialQuantor(
                Var("b"),
                Impl(
                    And(Predicate("Person", [Var("a")]), Predicate("Person", [Var("b")])),
                    Predicate("Parent", [Var("a"), Var("b")])
                )
            )
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_complex_2(self):
        wff = "(A)a,b (E)c (Person(a)&Person(b)&Person(c)&Parent(a,b)&Parent(b,c)->Grandparent(a,c))"
        expr = AllQuantor(
            Var("a"),
            AllQuantor(
                Var("b"),
                ExistentialQuantor(
                    Var("c"),
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
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)

    def test_complex_3(self):
        wff = "(P(A)->K(f(A,B))&P(C))<->!(E(C,D)|K(A))"
        expr = Eq(
            Impl(
                Predicate("P", [Const("A")]),
                And(
                    Predicate("K", [Func("f", [Const("A"), Const("B")])]),
                    Predicate("P", [Const("C")])
                )
            ),
            Not(
                Or(
                    Predicate("E", [Const("C"), Const("D")]),
                    Predicate("K", [Const("A")])
                )
            )
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B", "C", "D"])

    def test_complex_4(self):
        wff = "P(A)|P(B)&P(C)|P(D)"
        expr = Or(
            Or(
                Predicate("P", [Const("A")]),
                And(
                    Predicate("P", [Const("B")]),
                    Predicate("P", [Const("C")])
                )
            ),
            Predicate("P", [Const("D")])
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["A", "B", "C", "D"])

    def test_complex_5(self):
        wff = "(A)a (P(a)->K(f(a,B))&P(C)<->!(E(C,D)|K(a)))"
        expr = AllQuantor(
            Var("a"),
            Eq(
                Impl(
                    Predicate("P", [Var("a")]),
                    And(
                        Predicate("K", [Func("f", [Var("a"), Const("B")])]),
                        Predicate("P", [Const("C")])
                    )
                ),
                Not(
                    Or(
                        Predicate("E", [Const("C"), Const("D")]),
                        Predicate("K", [Var("a")])
                    )
                )
            )
        )

        tree = FoplParser(wff).parse()

        self.assertEqual(tree.expr, expr)
        self.assertEqual(tree.constants, ["B", "C", "D"])


class TestIncorrectFoplParser(unittest.TestCase):
    def test_atom_1(self):
        nwff = "P("
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_2(self):
        nwff = "P)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_3(self):
        nwff = "P(X,)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_4(self):
        nwff = "P(X,f()"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_5(self):
        nwff = "P(X,f(X,))"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_atom_6(self):
        nwff = "P(X_123)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_invalid_variable_1(self):
        nwff = "P(x)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_invalid_variable_2(self):
        nwff = "(A)x P(x,y)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)

    def test_invalid_variable_3(self):
        nwff = "P(X,y)"
        self.assertRaises(RecognitionException, FoplParser(nwff).parse)


if __name__ == '__main__':
    unittest.main()
