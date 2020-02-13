import copy

from antlr4.tree.Tree import TerminalNodeImpl

from gen.PropositionalParser import PropositionalParser
from src.Model.Visitor import visitor


class PropositionalExpressionTree:
    def __init__(self, expr: PropositionalParser.ExprContext, visit_idx: int):
        self.expr = Expr.create(expr.children)
        self.expr.visit_idx = visit_idx


class Expr:
    name = "Expression"
    is_atom = False
    op_priority = 0

    def permute(self, permutations: list=None):
        """Returns all permutations of the expression
        
        Args:
            permutations (list, optional): List of permutations to append to. Defaults to None.
        """
        return [self]

    @staticmethod
    def create(expr):
        val = Atom.create(expr)
        if val is not None:
            return val
        val = Not.create(expr)
        if val is not None:
            return val
        val = Operation.create(expr)
        if val is not None:
            return val
        return Expr.create(expr[1].children)


@visitor
class Atom(Expr):
    is_atom = True

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

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                self.name == other.name
        )

    def __str__(self):
        return self.name

    def priority(self, true_side: bool) -> int:
        return 0


@visitor
class Not(Expr):
    name = "Negation"
    op_priority = 1

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
                return Not(Expr.create(expr.children))
        return None

    def __init__(self, expr: Expr):
        self.expr = expr

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                self.expr == other.expr
        )

    def __str__(self):
        if self.expr.op_priority > self.op_priority:
            return f"!({str(self.expr)})"
        else:
            return f"!{str(self.expr)}"

    def priority(self, true_side: bool) -> int:
        return 0


class Operation(Expr):
    printable_operator: str = None

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
                    return And(Expr.create(lhs.children), Expr.create(rhs.children))
                if t == PropositionalParser.OR:
                    return Or(Expr.create(lhs.children), Expr.create(rhs.children))
                if t == PropositionalParser.IMPL:
                    return Impl(Expr.create(lhs.children), Expr.create(rhs.children))
                if t == PropositionalParser.EQ:
                    return Eq(Expr.create(lhs.children), Expr.create(rhs.children))
        return None

    def __init__(self, lhs: Expr, rhs: Expr):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                self.lhs == other.lhs and
                self.rhs == other.rhs
        )

    def __str__(self):
        children = [f"({str(child)})" if child.op_priority > self.op_priority
                    else f"{str(child)}" for child in [self.lhs, self.rhs]]
        return self.printable_operator.join(children)

    def permute(self, permutables=None):
        permutables = [] if permutables is None else permutables
        permutables.append(copy.deepcopy(self))

        if type(self.lhs) == type(self):
            for p in self.lhs.permute():
                perm = copy.deepcopy(self)
                perm.lhs = p.lhs
                perm.rhs = type(self)(p.rhs, perm.rhs)

                if perm not in permutables:
                    perm.permute(permutables)

        if type(self.rhs) == type(self):
            for p in self.rhs.permute():
                perm = copy.deepcopy(self)
                rhs = perm.rhs
                perm.rhs = p.rhs
                perm.lhs = type(self)(perm.lhs, p.lhs)

                if perm not in permutables:
                    perm.permute(permutables)

        return permutables


@visitor
class And(Operation):
    name = "Conjunction"
    op_priority = 2
    printable_operator: str = "&"

    def priority(self, true_side: bool) -> int:
        return 0 if true_side else 1


@visitor
class Or(Operation):
    name = "Disjunction"
    op_priority = 3
    printable_operator: str = "|"

    def priority(self, true_side: bool) -> int:
        return 1 if true_side else 0


@visitor
class Impl(Operation):
    name = "Conditional"
    op_priority = 4
    printable_operator: str = "->"

    def __hash__(self):
        return str(self).__hash__()

    def priority(self, true_side: bool) -> int:
        return 1 if true_side else 0
    
    def __str__(self):
        children = [f"({str(child)})" if child.op_priority >= self.op_priority
                    else f"{str(child)}" for child in [self.lhs, self.rhs]]
        return self.printable_operator.join(children)

    def permute(self, permutations: list=None):
        return [self]


@visitor
class Eq(Operation):
    name = "Biconditional"
    op_priority = 5
    printable_operator: str = "<->"

    def priority(self, true_side: bool) -> int:
        return 1
