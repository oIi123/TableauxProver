from antlr4.tree.Tree import *

from gen.FOPLParser import FOPLParser
from src.Model.Visitor import visitor


class FoplExpressionTree:
    def __init__(self, expr: FOPLParser.ExprContext):
        self.expr = Expr.create(expr.children)


class Expr:
    @staticmethod
    def create(expr):
        if (predicate := Predicate.create(expr)) is not None:
            return predicate
        if (n := Not.create(expr)) is not None:
            return n
        if (op := Operation.create(expr)) is not None:
            return op
        if (quantor := Quantor.create(expr)) is not None:
            return quantor
        return Expr.create(expr[1].children)


@visitor
class Predicate(Expr):
    @staticmethod
    def create(expr):
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
                    return Predicate(predicate_name.symbol.text[:-1], Term.create(terms))

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
    def create(expr):
        if len(expr) == 2:
            op: TerminalNodeImpl = expr[0]
            expr: FOPLParser.ExprContext = expr[1]
            if (
                type(op) == TerminalNodeImpl and
                type(expr) == FOPLParser.ExprContext and
                op.symbol.type == FOPLParser.NOT
            ):
                return Not(Expr.create(expr.children))

    def __init__(self, expr: Expr):
        self.expr = expr

    def __eq__(self, other):
        return type(other) == type(self) and other.expr == self.expr

    def __str__(self):
        return f"Not({str(self.expr)})"


class Quantor(Expr):
    @staticmethod
    def create(expr):
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
                if quantor.children[0].symbol.type == FOPLParser.ALL_QUANTOR:
                    return AllQuantor(var_list, Expr.create(expr.children))
                elif quantor.children[0].symbol.type == FOPLParser.EX_QUANTOR:
                    return ExistentialQuantor(var_list, Expr.create(expr.children))

    def __init__(self, var_list: list, expr: Expr):
        self.var_list = var_list
        self.expr = expr

    def __eq__(self, other):
        return (
            type(other) == type(self) and
            other.var_list == self.var_list and
            other.expr == self.expr
        )

    def __str__(self):
        return f"{type(self).__name__}([{','.join([str(i) for i in self.var_list])}],{str(self.expr)})"


@visitor
class ExistentialQuantor(Quantor):
    pass


@visitor
class AllQuantor(Quantor):
    pass


class Operation(Expr):
    @staticmethod
    def create(expr):
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
                    return And(Expr.create(lhs.children), Expr.create(rhs.children))
                if t == FOPLParser.OR:
                    return Or(Expr.create(lhs.children), Expr.create(rhs.children))
                if t == FOPLParser.IMPL:
                    return Impl(Expr.create(lhs.children), Expr.create(rhs.children))
                if t == FOPLParser.EQ:
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


class Term:
    @staticmethod
    def create(terms: FOPLParser.TermsContext):
        t = []
        term_context: FOPLParser.TermContext = terms.children[0]
        term_list_context: FOPLParser.TermlistContext = terms.children[1]
        while True:
            if len(term_context.children) == 1:
                if type(term_context.children[0]) == FOPLParser.VarContext:
                    t.append(Var.create(term_context.children[0]))
                elif type(term_context.children[0]) == FOPLParser.FuncContext:
                    t.append(Func.create(term_context.children[0]))

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
    def create(var_context: FOPLParser.VarContext):
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
class Func(Term):
    @staticmethod
    def create(func_context: FOPLParser.FuncContext):
        name: TerminalNodeImpl = func_context.children[0]
        if len(func_context.children) == 2:
            return Func(name.symbol.text[:-1], [])
        terms: FOPLParser.TermsContext = func_context.children[1]
        return Func(name.symbol.text[:-1], Term.create(terms))

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
