import unittest

from src.Model.FoplExpressionTree import *
from src.TableauxBuilder.IfoplTableauxBuilder import IfoplTableauxBuilder


class TestIfoplTableauxBuilder(unittest.TestCase):
    def test_not_closing_1(self):
        # P()
        expr = Predicate("P", [])

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_2(self):
        # P()&P()
        expr = And(
            Predicate("P", []),
            Predicate("P", []),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_3(self):
        # P()|P()
        expr = Or(
            Predicate("P", []),
            Predicate("P", []),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_4(self):
        # P()&T() | !P()&T()
        expr = Or(
            And(
                Predicate("P", []),
                Predicate("T", []),
            ),
            And(
                Not(Predicate("P", [])),
                Predicate("T", [])
            )
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_5(self):
        # P()|!P()
        expr = Or(
            Predicate("P", []),
            Not(Predicate("P", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_6(self):
        # !!P()->P()
        expr = Impl(
            Not(Not(Predicate("P", []))),
            Predicate("P", []),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_7(self):
        # !(!P()|!T())->P()&T()
        expr = Impl(
            Not(Or(Not(Predicate("P", [])), Predicate("T", []))),
            And(Predicate("P", []), Predicate("T", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_8(self):
        # !(!P()&!T())->P()|T()
        expr = Impl(
            Not(And(Not(Predicate("P", [])), Predicate("T", []))),
            Or(Predicate("P", []), Predicate("T", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_9(self):
        # !(P()&T())->(!P()|!T())
        expr = Impl(
            Not(And(Predicate("P", []), Predicate("T", []))),
            Or(Not(Predicate("P", [])), Not(Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_10(self):
        # !(P()->!T())->P()&T()
        expr = Impl(
            Not(Impl(Predicate("P", []), Not(Predicate("T", [])))),
            And(Predicate("P", []), Not(Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_11(self):
        # !(P()&!T())->(P()->T())
        expr = Impl(
            Not(And(Predicate("P", []), Not(Predicate("T", [])))),
            Impl(Predicate("P", []), Predicate("T", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_12(self):
        # !(P()->T())->(P()&!T())
        expr = Impl(
            Not(Impl(Predicate("P", []), Predicate("T", []))),
            And(Predicate("P", []), Not(Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_13(self):
        # (P()->T())->(!P()|T())
        expr = Impl(
            Impl(Predicate("P", []), Predicate("T", [])),
            Or(Not(Predicate("P", [])), Predicate("T", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_14(self):
        # (A)x P(x)&P(x)
        expr = AllQuantor(Var("x"),
            And(Predicate("P", []), Predicate("P", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_15(self):
        # (E)x P(x)&P(x)
        expr = ExistentialQuantor(Var("x"),
            And(Predicate("P", []), Predicate("P", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_closing_1(self):
        # T P()     F P()
        expr_1 = Predicate("P", [])
        expr_2 = Predicate("P", [])

        builder = IfoplTableauxBuilder(true_exprs=[expr_1], false_exprs=[expr_2])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_2(self):
        # T P()     F P()|T()
        expr_1 = Predicate("P", [])
        expr_2 = Or(Predicate("P", []), Predicate("T", []))

        builder = IfoplTableauxBuilder(true_exprs=[expr_1], false_exprs=[expr_2])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_3(self):
        # T P()&T()     F P()
        expr_1 = And(Predicate("P", []), Predicate("T", []))
        expr_2 = Predicate("P", [])

        builder = IfoplTableauxBuilder(true_exprs=[expr_1], false_exprs=[expr_2])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_4(self):
        # P()&T()->!(!P()|!T())
        expr = Impl(
            And(Predicate("P", []), Predicate("T", [])),
            Not(Or(Not(Predicate("P", [])), Not(Predicate("T", [])))),
        )
        print(expr)

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_5(self):
        # P()|T()->!(!P()&!T())
        expr = Impl(
            Or(Predicate("P", []), Predicate("T", [])),
            Not(And(Not(Predicate("P", [])), Not(Predicate("T", [])))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_6(self):
        # !P()|!T()->!(P()&T())
        expr = Impl(
            Or(Not(Predicate("P", [])), Not(Predicate("T", []))),
            Not(And(Predicate("P", []), Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_7(self):
        # !P()&!T()->!(P()|T())
        expr = Impl(
            And(Not(Predicate("P", [])), Not(Predicate("T", []))),
            Not(Or(Predicate("P", []), Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_8(self):
        # !(P()|T())->!P()&!T()
        expr = Impl(
            Not(Or(Predicate("P", []), Predicate("T", []))),
            And(Not(Predicate("P", [])), Not(Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_9(self):
        # P()&T()->!(P()->!T())
        expr = Impl(
            And(Predicate("P", []), Predicate("T", [])),
            Not(Impl(Predicate("P", []), Not(Predicate("T", [])))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_10(self):
        # P()&!T()->!(P()->T())
        expr = Impl(
            And(Predicate("P", []), Not(Predicate("T", []))),
            Not(Impl(Predicate("P", []), Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_11(self):
        # (P()->!T())->!(P()&T())
        expr = Impl(
            Impl(Predicate("P", []), Not(Predicate("T", []))),
            Not(And(Predicate("P", []), Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_12(self):
        # !(P()&T())->(P()->!T())
        expr = Impl(
            Not(And(Predicate("P", []), Predicate("T", []))),
            Impl(Predicate("P", []), Not(Predicate("T", []))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_13(self):
        # P()|T()->(!P()->T())
        expr = Impl(
            Or(Predicate("P", []), Predicate("T", [])),
            Impl(Not(Predicate("P", [])), Predicate("T", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_14(self):
        # (!P()|T())->(P()->T())
        expr = Impl(
            Or(Not(Predicate("P", [])), Predicate("T", [])),
            Impl(Predicate("P", []), Predicate("T", [])),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_15(self):
        # (P()<->T())<->(((P()->T())&(T()->P()))
        expr = Eq(
            Eq(Predicate("P", []), Predicate("T", [])),
            And(
                Impl(Predicate("P", []), Predicate("T", [])),
                Impl(Predicate("T", []), Predicate("P", [])),
            ),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_16(self):
        # (P()->T())<->(((P()|T())<->T())
        expr = Eq(
            Impl(Predicate("P", []), Predicate("T", [])),
            Eq(
                Or(Predicate("P", []), Predicate("T", [])),
                Predicate("T", []),
            ),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_17(self):
        # (P()->T())<->(((P()&T())<->P())
        expr = Eq(
            Impl(Predicate("P", []), Predicate("T", [])),
            Eq(
                And(Predicate("P", []), Predicate("T", [])),
                Predicate("P", []),
            ),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_18(self):
        # (P()&T())<->(((P()->T())<->P())
        expr = Eq(
            And(Predicate("P", []), Predicate("T", [])),
            Eq(
                Impl(Predicate("P", []), Predicate("T", [])),
                Predicate("P", []),
            ),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_19(self):
        # (P()&T())<->((((P()|T())<->T())<->P())
        expr = Eq(
            And(Predicate("P", []), Predicate("T", [])),
            Eq(
                Eq(
                    Or(Predicate("P", []), Predicate("T", [])),
                    Predicate("T", []),
                ),
                Predicate("P", []),
            ),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_20(self):
        # (A)x P(x)->!(E)x !P(x)
        expr = Impl(
            AllQuantor(Var("x"), Predicate("P", [Var("x")])),
            Not(ExistentialQuantor(Var("x"), Not(Predicate("P", [Var("x")])))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_21(self):
        # (E)x P(x)->!(A)x !P(x)
        expr = Impl(
            ExistentialQuantor(Var("x"), Predicate("P", [Var("x")])),
            Not(AllQuantor(Var("x"), Not(Predicate("P", [Var("x")])))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_22(self):
        # (A)x !P(x)<->!(E)x P(x)
        expr = Eq(
            AllQuantor(Var("x"), Not(Predicate("P", [Var("x")]))),
            Not(ExistentialQuantor(Var("x"), Predicate("P", [Var("x")]))),
        )

        builder = IfoplTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
