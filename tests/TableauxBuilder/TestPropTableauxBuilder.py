import unittest

from src.Model.PropositionalExpressionTree import *
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder


class TestPropTableauxBuilder(unittest.TestCase):
    def run_builder(self, builder: PropositionalTableauxBuilder):
        while not builder.is_done():
            builder.visit()

    def test_not_closing_1(self):
        # A
        expr = Atom("A")

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_2(self):
        # A&A
        expr = And(Atom("A"), Atom("A"))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_3(self):
        # A | A
        expr = Or(Atom("A"), Atom("A"))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_not_closing_4(self):
        # A&B | !A&B
        expr = Or(And(Atom("A"), Atom("B")), And(Not(Atom("A")), Atom("B")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertFalse(builder.is_closed())

    def test_closing_1(self):
        # A | !A
        expr = Or(Atom("A"), Not(Atom("A")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_2(self):
        # A -> (B -> A)
        expr = Impl(Atom("A"), Impl(Atom("B"), Atom("A")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_3(self):
        # !A -> (A -> B)
        expr = Impl(Not(Atom("A")), Impl(Atom("A"), Atom("B")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_4(self):
        # A -> (B -> C) <-> A&B -> C
        expr = Eq(Impl(Atom("A"), Impl(Atom("B"), Atom("C"))), Impl(And(Atom("A"), Atom("B")), Atom("C")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_5(self):
        # (A -> B) -> (!B -> !A)
        expr = Impl(Impl(Atom("A"), Atom("B")), Impl(Not(Atom("B")), Not(Atom("A"))))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_6(self):
        # (!A -> !B) -> (B -> A)
        expr = Impl(Impl(Not(Atom("A")), Not(Atom("B"))), Impl(Atom("B"), Atom("A")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_7(self):
        # !!A <-> A
        expr = Eq(Not(Not(Atom("A"))), Atom("A"))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_8(self):
        # !(A&B) <-> !A|!B
        expr = Eq(Not(And(Atom("A"), Atom("B"))), Or(Not(Atom("A")), Not(Atom("B"))))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_9(self):
        # !(A|B) <-> !A&!B
        expr = Eq(Not(Or(Atom("A"), Atom("B"))), And(Not(Atom("A")), Not(Atom("B"))))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_10(self):
        # !(!A|!B) <-> A&B
        expr = Eq(Not(Or(Not(Atom("A")), Not(Atom("B")))), And(Atom("A"), Atom("B")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())

    def test_closing_11(self):
        # !(!A&!B) <-> A|B
        expr = Eq(Not(And(Not(Atom("A")), Not(Atom("B")))), Or(Atom("A"), Atom("B")))

        builder = PropositionalTableauxBuilder(expr=expr)
        self.run_builder(builder)

        self.assertTrue(builder.is_closed())


if __name__ == '__main__':
    unittest.main()
