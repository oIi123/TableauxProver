from antlr4.tree.Tree import *

from gen.FOPLParser import FOPLParser
from src.Model.Visitor import visitor


class FoplExpressionTree:
    def __init__(self, expr: FOPLParser.ExprContext):
        self.var_stack = []
        self.constants = []
        self.expr = Expr.create(expr.children, tree=self)

    def add_const(self, name: str):
        if name not in self.constants:
            self.constants.append(name)


class Expr:
    @staticmethod
    def create(expr, tree: FoplExpressionTree):
        if (predicate := Predicate.create(expr, tree=tree)) is not None:
            return predicate
        if (n := Not.create(expr, tree=tree)) is not None:
            return n
        if (op := Operation.create(expr, tree=tree)) is not None:
            return op
        if (quantor := Quantor.create(expr, tree=tree)) is not None:
            return quantor
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
                    if term_context.children[0].children[0].symbol.text in tree.var_stack:
                        t.append(Var.create(term_context.children[0]))
                    else:
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
        return f"Var({self.name})"


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
        return f"Const({self.name})"


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
        return f"Func({self.name},[{','.join([str(i) for i in self.terms])}])"


@visitor
class Predicate(Expr):
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
        return f"Pred({self.name},[{','.join([str(i) for i in self.terms])}])"


@visitor
class Not(Expr):
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
        return f"Not({str(self.expr)})"


class Quantor(Expr):
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
                tree.var_stack.extend([i.name for i in var_list])
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

    def __str__(self):
        return f"{type(self).__name__}({str(self.variable)},{str(self.expr)})"


@visitor
class ExistentialQuantor(Quantor):
    pass


@visitor
class AllQuantor(Quantor):
    pass


class Operation(Expr):
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
        return f"{type(self).__name__}({str(self.lhs)},{str(self.rhs)})"


@visitor
class And(Operation):
    pass


@visitor
class Or(Operation):
    pass


@visitor
class Impl(Operation):
    pass


@visitor
class Eq(Operation):
    pass
