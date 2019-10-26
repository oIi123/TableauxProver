from antlr4.tree.Tree import TerminalNodeImpl

from gen.PropositionalParser import PropositionalParser


class PropositionalExpressionTree:
    def __init__(self, expr: PropositionalParser.ExprContext):
        self.expr = Expr.create(expr.children)

# TerminalNodeImpl
class Expr:
    @staticmethod
    def create(expr):
        if (atom := Atom.create(expr)) is not None:
            return atom
        if (n := Not.create(expr)) is not None:
            return n
        if (op := Operation.create(expr)) is not None:
            return op
        return Expr.create(expr[1])


class Atom(Expr):
    @staticmethod
    def create(expr):
        if len(expr) == 1:
            expr = expr[0]
            if (
                    type(expr) == TerminalNodeImpl and
                    expr.symbol.type == PropositionalParser.Atom
            ):
                return Atom(expr.symbol.text)
        return None

    def __init__(self, name):
        self.name = name


class Not(Expr):
    @staticmethod
    def create(expr):
        if len(expr) == 2:
            op: TerminalNodeImpl = expr[0]
            expr: PropositionalParser.ExprContext = expr[1]
            if (
                type(op) == TerminalNodeImpl and
                type(expr) == PropositionalParser.ExprContext and
                op.symbol.type == PropositionalParser.NOT
            ):
                return Not(expr)
        return None

    def __init__(self, expr: PropositionalParser.ExprContext):
        self.expr = Expr.create(expr.children)


class Operation(Expr):
    @staticmethod
    def create(expr):
        if len(expr) == 3:
            lhs: PropositionalParser.ExprContext = expr[0]
            op: TerminalNodeImpl = expr[1]
            rhs: PropositionalParser.ExprContext = expr[2]
            if (
                    type(lhs) == PropositionalParser.ExprContext and
                    type(rhs) == PropositionalParser.ExprContext and
                    type(op) == TerminalNodeImpl
            ):
                t = op.symbol.type
                if t == PropositionalParser.AND:
                    return And(lhs, rhs)
                if t == PropositionalParser.OR:
                    return Or(lhs, rhs)
                if t == PropositionalParser.IMPL:
                    return Impl(lhs, rhs)
                if t == PropositionalParser.EQ:
                    return Impl(lhs, rhs)
        return None

    def __init__(self, lhs: PropositionalParser.ExprContext, rhs: PropositionalParser.ExprContext):
        self.lhs = Expr.create(lhs.children)
        self.rhs = Expr.create(rhs.children)


class And(Operation):
    pass


class Or(Operation):
    pass


class Impl(Operation):
    pass


class Eq(Operation):
    pass
