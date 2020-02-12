import unittest

from src.Parser.PropParser import PropParser as Parser
from src.Model.PropositionalExpressionTree import *


class TestPlPermutation(unittest.TestCase):
    

    def test_atom(self):
        # A = [A]
        expr = Atom("A")

        permutations = expr.permute()

        self.assertEqual(len(permutations), 1)
        self.assertEqual(expr, permutations[0])

    def test_and_1(self):
        expected_permutations = [
            "A&B",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_and_2(self):
        expected_permutations = [
            "A&(B&C)",
            "(A&B)&C",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_and_3(self):
        expected_permutations = [
            "A&(B&C)",
            "(A&B)&C",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_and_4(self):
        expected_permutations = [
            "A&(B&(C&D))",
            "A&((B&C)&D)",
            "((A&B)&C)&D",
            "(A&(B&C))&D",
            "(A&B)&(C&D)",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_and_5(self):
        expr = And(Or(Atom("A"), Atom("B")), Atom("C"))

        expected_permutations = [
            "(A|B)&C",
        ]

        permutations = expr.permute()

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            expr = Parser.parse(expected_permutation).expr
            self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_and_6(self):
        expr = Or(And(Atom("A"), Atom("B")), Atom("C"))

        expected_permutations = [
            "A&B|C",
        ]

        permutations = expr.permute()

        self.assertEqual(len(permutations), len(expected_permutations))
        for expected_permutation in expected_permutations:
            expr = Parser.parse(expected_permutation).expr
            self.assertIn(expr, permutations, f"{expected_permutation} missing")

    def test_or_1(self):
        expected_permutations = [
            "A|B",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")

    def test_or_2(self):
        expected_permutations = [
            "(A|B)|C",
            "A|(B|C)",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
        
    def test_or_3(self):
        expected_permutations = [
            "(A|B)|C",
            "A|(B|C)",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_or_4(self):
        expected_permutations = [
            "A|((B|C)|D)",
            "A|(B|(C|D))",
            "((A|B)|C)|D",
            "(A|(B|C))|D",
            "(A|B)|(C|D)",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")

    def test_impl_1(self):
        expected_permutations = [
            "A->B",
        ]

        for expr_str in expected_permutations:
            expr = Parser.parse(expr_str).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), 1)
            expr = Parser.parse(expr_str).expr
            self.assertIn(expr, permutations, f"{expr_str} not in perms")
    
    def test_impl_2(self):
        expected_permutations = [
            "(A->B)->C",
            "A->(B->C)",
        ]

        for expr_str in expected_permutations:
            expr = Parser.parse(expr_str).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), 1)
            expr = Parser.parse(expr_str).expr
            self.assertIn(expr, permutations, f"{expr_str} not in perms")
    
    def test_impl_3(self):
        expected_permutations = [
            "A->((B->C)->D)",
            "A->(B->(C->D))",
            "((A->B)->C)->D",
            "(A->(B->C))->D",
            "(A->B)->(C->D)",
        ]

        for expr_str in expected_permutations:
            expr = Parser.parse(expr_str).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), 1)
            expr = Parser.parse(expr_str).expr
            self.assertIn(expr, permutations, f"{expr_str} not in perms")
    
    def test_eq_1(self):
        expected_permutations = [
            "A<->B",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_eq_2(self):
        expected_permutations = [
            "A<->(B<->C)",
            "(A<->B)<->C",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")
    
    def test_eq_3(self):
        expected_permutations = [
            "A<->((B<->C)<->D)",
            "A<->(B<->(C<->D))",
            "((A<->B)<->C)<->D",
            "(A<->(B<->C))<->D",
            "(A<->B)<->(C<->D)",
        ]

        for expr in expected_permutations:
            expr = Parser.parse(expr).expr
            permutations = expr.permute()

            self.assertEqual(len(permutations), len(expected_permutations))
            for expected_permutation in expected_permutations:
                expr = Parser.parse(expected_permutation).expr
                self.assertIn(expr, permutations, f"{expected_permutation} missing")

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
