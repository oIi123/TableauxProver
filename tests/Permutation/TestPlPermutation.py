import unittest

from src.Parser.PropParser import PropParser
from src.Model.PropositionalExpressionTree import *


class TestPlPermutation(unittest.TestCase):
    

    def test_atom(self):
        # A = [A]
        expr = Atom("A")

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])

    def test_and_1(self):
        # A&B = [A&B]
        expr = And(Atom("A"), Atom("B"))

        expected_permutations = [
            "A&B",
            "B&A",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
    
    def test_and_2(self):
        expr = And(And(Atom("A"), Atom("B")), Atom("C"))

        expected_permutations = [
            "A&B&C",
            "A&C&B",
            "B&A&C",
            "B&C&A",
            "C&B&A",
            "C&A&B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
    
    def test_and_3(self):
        expr = And(Atom("A"), And(Atom("B"), Atom("C")))

        expected_permutations = [
            "A&B&C",
            "A&C&B",
            "B&A&C",
            "B&C&A",
            "C&B&A",
            "C&A&B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
    
    def test_and_4(self):
        expr = And(Atom("A"), And(Atom("B"), And(Atom("C"), Atom("D"))))

        expected_permutations = [
            "A&B&C&D",
            "A&C&B&D",
            "B&A&C&D",
            "B&C&A&D",
            "C&B&A&D",
            "C&A&B&D",

            "A&B&D&C",
            "A&C&D&B",
            "B&A&D&C",
            "B&C&D&A",
            "C&B&D&A",
            "C&A&D&B",

            "A&D&B&C",
            "A&D&C&B",
            "B&D&A&C",
            "B&D&C&A",
            "C&D&B&A",
            "C&D&A&B",

            "D&A&B&C",
            "D&A&C&B",
            "D&B&A&C",
            "D&B&C&A",
            "D&C&B&A",
            "D&C&A&B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
    
    def test_and_5(self):
        expr = And(Or(Atom("A"), Atom("B")), Atom("C"))

        expected_permutations = [
            "(A|B)&C",
            "C&(A|B)",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
    
    def test_and_6(self):
        expr = Or(And(Atom("A"), Atom("B")), Atom("C"))

        expected_permutations = [
            "A&B|C",
            "C|A&B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")

    def test_or_1(self):
        expr = Or(Atom("A"), Atom("B"))

        expected_permutations = [
            "A|B",
            "B|A",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")

    def test_or_2(self):
        expr = Or(Or(Atom("A"), Atom("B")), Atom("C"))

        expected_permutations = [
            "A|B|C",
            "A|C|B",
            "B|A|C",
            "B|C|A",
            "C|B|A",
            "C|A|B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
        
    def test_or_3(self):
        expr = Or(Atom("A"), Or(Atom("B"), Atom("C")))

        expected_permutations = [
            "A|B|C",
            "A|C|B",
            "B|A|C",
            "B|C|A",
            "C|B|A",
            "C|A|B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")
    
    def test_or_4(self):
        expr = Or(Or(Or(Atom("A"), Atom("B")), Atom("C")), Atom("D"))

        expected_permutations = [
            "A|B|C|D",
            "A|C|B|D",
            "B|A|C|D",
            "B|C|A|D",
            "C|B|A|D",
            "C|A|B|D",

            "A|B|D|C",
            "A|C|D|B",
            "B|A|D|C",
            "B|C|D|A",
            "C|B|D|A",
            "C|A|D|B",

            "A|D|B|C",
            "A|D|C|B",
            "B|D|A|C",
            "B|D|C|A",
            "C|D|B|A",
            "C|D|A|B",

            "D|A|B|C",
            "D|A|C|B",
            "D|B|A|C",
            "D|B|C|A",
            "D|C|B|A",
            "D|C|A|B",
        ]

        permutations = [str(x) for x in expr.permute()]

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            self.assertIn(expected_permutation, permutations, f"{expected_permutation} missing")

    def test_impl_1(self):
        expr = Impl(Atom("A"), Atom("B"))

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])
    
    def test_impl_2(self):
        expr = Impl(Impl(Atom("A"), Atom("B")), Atom("C"))

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])
    
    def test_eq_1(self):
        expr = Eq(Atom("A"), Atom("B"))

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])
    
    def test_eq_2(self):
        expr = Eq(Eq(Atom("A"), Atom("B")), Atom("C"))

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])

    def test_not_1(self):
        expr = Not(Atom("A"))

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])
    
    def test_not_2(self):
        expr = Not(Not(Atom("A")))

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])
