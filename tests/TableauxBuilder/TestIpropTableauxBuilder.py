import unittest

from src.Model.PropositionalExpressionTree import *
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder


class TestIpropTableauxBuilder(unittest.TestCase):
    def test_not_closing_1(self):
        # A
        expr = Atom("A")

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_2(self):
        # A&A
        expr = And(Atom("A"), Atom("A"))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_3(self):
        # A | A
        expr = Or(Atom("A"), Atom("A"))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_4(self):
        # A&B | !A&B
        expr = Or(And(Atom("A"), Atom("B")), And(Not(Atom("A")), Atom("B")))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_5(self):
        # A|!A
        expr = Or(Atom("A"), Not(Atom("A")))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_6(self):
        # !!A->A
        expr = Impl(Not(Not(Atom("A"))), Atom("A"))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_7(self):
        # !(!A|!B)->A&B
        expr = Impl(
            Not(Or(Not(Atom("A")), Not(Atom("B")))),
            And(Atom("A"), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_8(self):
        # !(!A&!B)->A|B
        expr = Impl(
            Not(And(Not(Atom("A")), Not(Atom("B")))),
            Or(Atom("A"), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_9(self):
        # !(A&B)->(!A|!B)
        expr = Impl(
            Not(And(Atom("A"), Atom("B"))),
            Or(Not(Atom("A")), Not(Atom("B"))),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_10(self):
        # !(A->!B)->A&B
        expr = Impl(
            Not(Impl(Atom("A"), Not(Atom("B")))),
            And(Atom("A"), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_11(self):
        # !(A&!B)->(A->B)
        expr = Impl(
            Not(And(Atom("A"), Not(Atom("B")))),
            Impl(Atom("A"), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    
    def test_not_closing_12(self):
        # !(A->B)->(A&!B)
        expr = Impl(
            Not(Impl(Atom("A"), Atom("B"))),
            And(Atom("A"), Not(Atom("B"))),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_13(self):
        # (A->B)->(!A|B)
        expr = Impl(
            Impl(Atom("A"), Atom("B")),
            Or(Not(Atom("A")), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    def test_not_closing_14(self):
        # (A->B)->(!A|B)
        expr = Impl(
            Impl(Atom("A"), Atom("B")),
            Or(Not(Atom("A")), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())

    """
    Not Terminating:
    def test_not_closing_15(self):
        # (!A->B)->(A|B)
        expr = Impl(
            Impl(Not(Atom("A")), Atom("B")),
            Or(Atom("A"), Atom("B")),
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertFalse(builder.is_closed())
    """

    def test_closing_1(self):
        # T A     F A
        expr_1 = Atom("A")
        expr_2 = Atom("A")

        builder = IpcTableauxBuilder(true_exprs=[expr_1], false_exprs=[expr_2])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_2(self):
        # T A     F A|B
        expr_1 = Atom("A")
        expr_2 = Or(Atom("A"), Atom("B"))

        builder = IpcTableauxBuilder(true_exprs=[expr_1], false_exprs=[expr_2])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_3(self):
        # T A&B     F A
        expr_1 = And(Atom("A"), Atom("B"))
        expr_2 = Atom("A")

        builder = IpcTableauxBuilder(true_exprs=[expr_1], false_exprs=[expr_2])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_4(self):
        # A&B->!(!A|!B)
        expr = Impl(And(Atom("A"), Atom("B")), Not(Or(Not(Atom("A")), Not(Atom("B")))))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_5(self):
        # A|B->!(!A&!B)
        expr = Impl(Or(Atom("A"), Atom("B")), Not(And(Not(Atom("A")), Not(Atom("B")))))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_6(self):
        # !A|!B -> !(A&B)
        expr = Impl(Or(Not(Atom("A")), Not(Atom("B"))), Not(And(Atom("A"), Atom("B"))))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_7(self):
        # !A&!B -> !(A|B)
        expr = Impl(And(Not(Atom("A")), Not(Atom("B"))), Not(Or(Atom("A"), Atom("B"))))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_8(self):
        # !(A|B) -> !A&!B
        expr = Impl(Not(Or(Atom("A"), Atom("B"))), And(Not(Atom("A")), Not(Atom("B"))))

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_9(self):
        # A&B->!(A->!B)
        expr = Impl(
            And(Atom("A"), Atom("B")),
            Not(Impl(Atom("A"), Not(Atom("B"))))
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_10(self):
        # A&!B->!(A->B)
        expr = Impl(
            And(Atom("A"), Not(Atom("B"))),
            Not(Impl(Atom("A"), Atom("B")))
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_11(self):
        # (A->!B) -> !(A&B)
        expr = Impl(
            Impl(Atom("A"), Not(Atom("B"))),
            Not(And(Atom("A"), Atom("B")))
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_12(self):
        # !(A&B) -> (A->!B)
        expr = Impl(
            Not(And(Atom("A"), Atom("B"))),
            Impl(Atom("A"), Not(Atom("B")))
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_13(self):
        # A|B -> (!A->B)
        expr = Impl(
            Or(Atom("A"), Atom("B")),
            Impl(Not(Atom("A")), Atom("B"))
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_14(self):
        # (!A|B)->(A->B)
        expr = Impl(
            Or(Not(Atom("A")), Atom("B")),
            Impl(Atom("A"), Atom("B"))
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_15(self):
        # (A<->B)<->((A->B)&(B->A))
        expr = Eq(
            Eq(Atom("A"), Atom("B")),
            And(
                Impl(Atom("A"), Atom("B")),
                Impl(Atom("B"), Atom("A")),
            )
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_16(self):
        # (A->B)<->((A|B)<->B)
        expr = Eq(
            Impl(Atom("A"), Atom("B")),
            Eq(
                Or(Atom("A"), Atom("B")),
                Atom("B"),
            )
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_17(self):
        # (A->B)<->((A&B)<->A)
        expr = Eq(
            Impl(Atom("A"), Atom("B")),
            Eq(
                And(Atom("A"), Atom("B")),
                Atom("A"),
            )
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())

    def test_closing_18(self):
        # (A&B)<->((A->B)<->A)
        expr = Eq(
            And(Atom("A"), Atom("B")),
            Eq(
                Impl(Atom("A"), Atom("B")),
                Atom("A"),
            )
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
    
    def test_closing_19(self):
        # (A&B)<->(((A|B)<->B)<->A)
        expr = Eq(
            And(Atom("A"), Atom("B")),
            Eq(
                Eq(
                    Or(Atom("A"), Atom("B")),
                    Atom("B"),
                ),
                Atom("A"),
            )
        )

        builder = IpcTableauxBuilder(false_exprs=[expr])
        builder.auto_resolve()

        self.assertTrue(builder.is_closed())
