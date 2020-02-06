import unittest

from antlr4 import RecognitionException

from src.Model.PropositionalExpressionTree import Atom, And, Or, Impl, Eq, Not
from src.Parser.PropParser import PropParser


class TestCorrectPropParser(unittest.TestCase):
    def test_atom_1(self):
        wff = "A"
        expr = Atom("A")

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_atom_2(self):
        wff = "abc"
        expr = Atom("abc")

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_atom_3(self):
        wff = "9af3b"
        expr = Atom("9af3b")

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_and_1(self):
        wff = "a&b"
        expr = And(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_and_2(self):
        wff = "a &b"
        expr = And(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_and_3(self):
        wff = "a & b"
        expr = And(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_and_4(self):
        wff = "a2df1&bash3"
        expr = And(Atom("a2df1"), Atom("bash3"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_or_1(self):
        wff = "a|b"
        expr = Or(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_or_2(self):
        wff = "a |b"
        expr = Or(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_or_3(self):
        wff = "a | b"
        expr = Or(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_or_4(self):
        wff = "a2df1|bash3"
        expr = Or(Atom("a2df1"), Atom("bash3"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_impl_1(self):
        wff = "a->b"
        expr = Impl(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_impl_2(self):
        wff = "a ->b"
        expr = Impl(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_impl_3(self):
        wff = "a -> b"
        expr = Impl(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_impl_4(self):
        wff = "a2df1->bash3"
        expr = Impl(Atom("a2df1"), Atom("bash3"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_eq_1(self):
        wff = "a<->b"
        expr = Eq(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_eq_2(self):
        wff = "a <->b"
        expr = Eq(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_eq_3(self):
        wff = "a <-> b"
        expr = Eq(Atom("a"), Atom("b"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_eq_4(self):
        wff = "a2df1<->bash3"
        expr = Eq(Atom("a2df1"), Atom("bash3"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_not_1(self):
        wff = "!a"
        expr = Not(Atom("a"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_not_2(self):
        wff = "! a"
        expr = Not(Atom("a"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_not_3(self):
        wff = "!a2df1"
        expr = Not(Atom("a2df1"))

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_clamp_1(self):
        wff = "(a)"
        expr = Atom("a")

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_clamp_2(self):
        wff = "( ads )"
        expr = Atom("ads")

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_complex_1(self):
        wff = "(a->b&c)<->!(d|a)"
        expr = Eq(
            Impl(
                Atom("a"),
                And(Atom("b"), Atom("c"))
            ),
            Not(
                Or(
                    Atom("d"),
                    Atom("a")
                )
            )
        )

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)

    def test_complex_2(self):
        wff = "a|b&c|d&e&f"
        expr = Or(
            Or(
                Atom("a"),
                And(Atom("b"), Atom("c"))
            ),
            And(
                And(Atom("d"), Atom("e")),
                Atom("f")
            )
        )

        tree = PropParser.parse(wff)

        self.assertEqual(expr, tree.expr)


class TestIncorrectPropParser(unittest.TestCase):
    def test_invalid_chars_1(self):
        nwff = "a?+ffs"
        self.assertRaises(RecognitionException, PropParser.parse, nwff)

    def test_invalid_chars_2(self):
        nwff = "a{ffs"
        self.assertRaises(RecognitionException, PropParser.parse, nwff)

    def test_invalid_chars_3(self):
        nwff = "a|?b"
        self.assertRaises(RecognitionException, PropParser.parse, nwff)

    def test_invalid_construct_1(self):
        nwff = "(a&b"
        self.assertRaises(RecognitionException, PropParser.parse, nwff)

    def test_invalid_construct_2(self):
        nwff = "(a&b)&->c"
        self.assertRaises(RecognitionException, PropParser.parse, nwff)


if __name__ == '__main__':
    unittest.main()
