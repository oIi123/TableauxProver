import copy

from antlr4 import RecognitionException
from antlr4.tree.Tree import *

from gen.FOPLParser import FOPLParser
from src.Model.Visitor import visitor


class FoplExpressionTree:
    def __init__(
                self,
                expr_context: FOPLParser.ExprContext = None,
                expr=None,
                constants: [str] = None,
                visit_idx: int = 0):
        self.var_stack = []
        self.constants = []
        if expr is not None:
            self.expr = expr
            self.constants = [] if constants is None else constants
        else:
            self.expr = Expr.create(expr_context.children, tree=self)
        
        self.expr.visit_idx = visit_idx

    def add_const(self, name: str):
        if name not in self.constants:
            self.constants.append(name)


class Expr:
    is_atom = False
    op_priority = 0

    def permute(self):
        """Returns all permutations of the expression
        """
        return [self]

    @staticmethod
    def create(expr, tree: FoplExpressionTree):
        val = Predicate.create(expr, tree=tree)
        if val is not None:
            return val
        val = Not.create(expr, tree=tree)
        if val is not None:
            return val
        val = Operation.create(expr, tree=tree)
        if val is not None:
            return val
        val = Quantor.create(expr, tree=tree)
        if val is not None:
            return val
        return Expr.create(expr[1].children, tree=tree)


class Term:
    @staticmethod
    def create(terms: FOPLParser.TermsContext, tree: FoplExpressionTree):
        t = []
        term_context: FOPLParser.TermContext = terms.children[0]
        term_list_context: FOPLParser.TermlistContext = terms.children[1]
        while True:
            if len(term_context.children) == 1:
                if type(term_context.children[0]) == FOPLParser.VarContext:
                    name = term_context.children[0].children[0].symbol.text
                    if name in tree.var_stack:
                        t.append(Var.create(term_context.children[0]))
                    else:
                        raise RecognitionException(f"The variable {name} is not in the scope of a quantor.\n"
                                                   "Begin with an uppercase letter to turn into a constant or add a quantor.")
                elif type(term_context.children[0]) == FOPLParser.ConstContext:
                    t.append(Const.create(term_context.children[0], tree=tree))
                elif type(term_context.children[0]) == FOPLParser.FuncContext:
                    t.append(Func.create(term_context.children[0], tree=tree))

            if (
                    term_list_context.children is not None and
                    len(term_list_context.children) == 3
            ):
                term_context = term_list_context.children[1]
                term_list_context = term_list_context.children[2]
            else:
                break

        return t


@visitor
class Var(Term):
    @staticmethod
    def create(var_context: FOPLParser.VarContext, tree: FoplExpressionTree = None):
        return Var(var_context.children[0].symbol.text)

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return (
            type(other) == type(self) and
            other.name == self.name
        )

    def __str__(self):
        return self.name


@visitor
class Const(Term):
    @staticmethod
    def create(var_context: FOPLParser.VarContext, tree: FoplExpressionTree):
        name = var_context.children[0].symbol.text
        tree.add_const(name)
        return Const(name)

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return (
            type(other) == type(self) and
            other.name == self.name
        )

    def __str__(self):
        return self.name


@visitor
class Func(Term):
    @staticmethod
    def create(func_context: FOPLParser.FuncContext, tree: FoplExpressionTree):
        name: TerminalNodeImpl = func_context.children[0]
        if len(func_context.children) == 2:
            return Func(name.symbol.text[:-1], [])
        terms: FOPLParser.TermsContext = func_context.children[1]
        return Func(name.symbol.text[:-1], Term.create(terms, tree=tree))

    def __init__(self, name: str, terms: list):
        self.name = name
        self.terms = terms

    def __eq__(self, other):
        return (
            type(other) == type(self) and
            other.name == self.name and
            other.terms == self.terms
        )

    def __str__(self):
        return f"{self.name}({','.join([str(i) for i in self.terms])})"


@visitor
class Predicate(Expr):
    is_atom = True

    @staticmethod
    def create(expr, tree: FoplExpressionTree):
        if len(expr) == 1 and type(expr[0]) == FOPLParser.PredicateContext:
            if len(expr[0].children) == 2:
                return Predicate(expr[0].children[0].symbol.text[:-1], [])
            predicate_name: TerminalNodeImpl = expr[0].children[0]
            terms: FOPLParser.TermsContext = expr[0].children[1]
            closing_bracket: TerminalNodeImpl = expr[0].children[2]
            if (
                type(predicate_name) == TerminalNodeImpl and
                type(terms) == FOPLParser.TermsContext and
                type(closing_bracket) == TerminalNodeImpl
            ):
                if predicate_name.symbol.type == FOPLParser.PREDNAME:
                    return Predicate(predicate_name.symbol.text[:-1], Term.create(terms, tree=tree))

    def __init__(self, name, terms):
        self.name = name
        self.terms = terms

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.name == self.name and
                other.terms == self.terms
        )

    def __str__(self):
        return f"{self.name}({','.join([str(i) for i in self.terms])})"

    def priority(self, true_side: bool) -> int:
        return 0


@visitor
class Not(Expr):
    op_priority = 2

    @staticmethod
    def create(expr, tree: FoplExpressionTree):
        if len(expr) == 2:
            op: TerminalNodeImpl = expr[0]
            expr: FOPLParser.ExprContext = expr[1]
            if (
                type(op) == TerminalNodeImpl and
                type(expr) == FOPLParser.ExprContext and
                op.symbol.type == FOPLParser.NOT
            ):
                return Not(Expr.create(expr.children, tree=tree))

    def __init__(self, expr: Expr):
        self.expr = expr

    def __eq__(self, other):
        return type(other) == type(self) and other.expr == self.expr

    def __str__(self):
        if self.expr.op_priority > self.op_priority:
            return f"!({str(self.expr)})"
        else:
            return f"!{str(self.expr)}"

    def priority(self, true_side: bool) -> int:
        return 0


class Quantor(Expr):
    op_priority = 1
    printable_operator: str = None

    @staticmethod
    def create(expr, tree: FoplExpressionTree):
        if len(expr) == 2:
            quantor: FOPLParser.QuantorContext = expr[0]
            expr: FOPLParser.ExprContext = expr[1]
            if (
                type(quantor) == FOPLParser.QuantorContext and
                type(expr) == FOPLParser.ExprContext
            ):
                var_list = []
                var_context: FOPLParser.VarContext = quantor.children[1]
                var_list_context: FOPLParser.VarlistContext = quantor.children[2]
                while True:
                    var_list.append(Var.create(var_context))
                    if (
                        var_list_context.children is not None and
                        len(var_list_context.children) == 3
                    ):
                        var_context = var_list_context.children[1]
                        var_list_context = var_list_context.children[2]
                    else:
                        break

                # Add Variables to the Stack
                variable_name_list = [i.name for i in var_list]
                for n in variable_name_list:
                    if n in tree.var_stack:
                        raise RecognitionException(f"The variable {n} is already in scope of another Quantor."
                                                   "Change the name of the Variable.")
                tree.var_stack.extend(variable_name_list)
                q = None
                if quantor.children[0].symbol.type == FOPLParser.ALL_QUANTOR:
                    q = AllQuantor.create_recursive(var_list, Expr.create(expr.children, tree=tree))
                elif quantor.children[0].symbol.type == FOPLParser.EX_QUANTOR:
                    q = ExistentialQuantor.create_recursive(var_list, Expr.create(expr.children, tree=tree))
                tree.var_stack = tree.var_stack[:-len(var_list)]  # Pop the added Variables from Stack
                return q

    @classmethod
    def create_recursive(cls, var_list: [Var], expr: Expr):
        if len(var_list) == 1:
            return cls(var_list[0], expr)
        return cls(var_list[0], cls.create_recursive(var_list[1:], expr))

    def __init__(self, variable: Var, expr: Expr):
        self.variable = variable
        self.expr = expr

    def __eq__(self, other):
        return (
            type(other) == type(self) and
            other.variable == self.variable and
            other.expr == self.expr
        )
    
    def __hash__(self):
        return str(self).__hash__()

    def __str__(self):
        s = f"{self.printable_operator}{str(self.variable)} "
        if self.expr.op_priority > self.op_priority:
            return s + f"({str(self.expr)})"
        return s + str(self.expr)

@visitor
class ExistentialQuantor(Quantor):
    printable_operator: str = "(E)"

    def priority(self, true_side: bool) -> int:
        return 1 if true_side else 2

@visitor
class AllQuantor(Quantor):
    printable_operator: str = "(A)"

    def priority(self, true_side: bool) -> int:
        return 2 if true_side else 1


class Operation(Expr):
    printable_operator: str = None

    @staticmethod
    def create(expr, tree: FoplExpressionTree):
        if len(expr) == 3:
            lhs: FOPLParser.ExprContext = expr[0]
            op: TerminalNodeImpl = expr[1]
            rhs: FOPLParser.ExprContext = expr[2]
            if (
                    type(lhs) == FOPLParser.ExprContext and
                    type(rhs) == FOPLParser.ExprContext and
                    type(op) == TerminalNodeImpl
            ):
                t = op.symbol.type
                if t == FOPLParser.AND:
                    return And(Expr.create(lhs.children, tree=tree), Expr.create(rhs.children, tree=tree))
                if t == FOPLParser.OR:
                    return Or(Expr.create(lhs.children, tree=tree), Expr.create(rhs.children, tree=tree))
                if t == FOPLParser.IMPL:
                    return Impl(Expr.create(lhs.children, tree=tree), Expr.create(rhs.children, tree=tree))
                if t == FOPLParser.EQ:
                    return Eq(Expr.create(lhs.children, tree=tree), Expr.create(rhs.children, tree=tree))
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
    op_priority = 3
    printable_operator: str = "&"

    def priority(self, true_side: bool) -> int:
        return 0 if true_side else 1


@visitor
class Or(Operation):
    op_priority = 4
    printable_operator: str = "|"

    def priority(self, true_side: bool) -> int:
        return 1 if true_side else 0


@visitor
class Impl(Operation):
    op_priority = 5
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
    op_priority = 6
    printable_operator: str = "<->"

    def priority(self, true_side: bool) -> int:
        return 1
