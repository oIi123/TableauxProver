import unittest

from src.TableauxBuilder.BaseManualTableau import NestLevelCalculator
from src.Model.FoplExpressionTree import *


class TestNestLevelCalculator(unittest.TestCase):
    def test_no_nesting_1(self):
        expr = Predicate("P", [])

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(0, nest_level)
    
    def test_no_nesting_2(self):
        expr = Predicate("P", [Var("x"), Const("Y")])

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(0, nest_level)
    
    def test_no_nesting_3(self):
        expr = And(Predicate("P", []), Predicate("T", []))

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(0, nest_level)
    
    def test_no_nesting_4(self):
        expr = Or(
            Predicate("P", [Const("X"), Var("y")]),
            Predicate("T", [Const("Z")]))

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(0, nest_level)

    def test_nesting_1(self):
        expr = Predicate("P", [Func("f", [])])

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(1, nest_level)
    
    def test_nesting_2(self):
        expr = Predicate("P", [Func("f", [Const("X"), Var("x")])])

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(1, nest_level)

    def test_nesting_3(self):
        expr = AllQuantor(Var("x"),
                    Predicate("P", [Func("f", [Const("X"), Var("x")])]))

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(1, nest_level)
    
    def test_nesting_4(self):
        expr = And(
                Predicate("P", [Func("f", [Const("X"), Var("x")])]),
                Predicate("T", [Const("X"), Var("x")]))

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(1, nest_level)
    
    def test_nesting_5(self):
        expr = Predicate("P", [Func("f", [Func("f", [Func("t", [Const("X")])])])])

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(3, nest_level)
    
    def test_nesting_6(self):
        expr = AllQuantor(Var("x"),
                And(
                    Predicate("P", [Func("f", [Func("f", [Func("t", [Const("X")])])])]),
                    Predicate("T", [Func("z", [Var("x"), Const("X")])])
                )
        )

        calculator = NestLevelCalculator()
        nest_level = calculator.calculate(expr)

        self.assertEqual(3, nest_level)
