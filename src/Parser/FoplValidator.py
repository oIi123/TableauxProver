from src.Model.FoplExpressionTree import *


class FoplValidator:
    def __init__(self):
        self.predicates = {}
        self.functions = {}
        self.valid = True

    def validate(self, expr: Expr) -> bool:
        expr.visit(self)
        return self.valid

    def visited_Predicate(self, predicate: Predicate):
        if predicate.name in self.predicates:
            if len(predicate.terms) != self.predicates[predicate.name]:
                self.valid = False
                return
        else:
            self.predicates[predicate.name] = len(predicate.terms)

        for term in predicate.terms:
            term.visit(self)

    def visited_Not(self, n: Not):
        n.expr.visit(self)

    def visited_ExistentialQuantor(self, quantor: ExistentialQuantor):
        quantor.expr.visit(self)

    def visited_AllQuantor(self, quantor: AllQuantor):
        quantor.expr.visit(self)

    def visited_And(self, a: And):
        a.lhs.visit(self)
        a.rhs.visit(self)

    def visited_Or(self, o: Or):
        o.lhs.visit(self)
        o.rhs.visit(self)

    def visited_Impl(self, impl: Impl):
        impl.lhs.visit(self)
        impl.rhs.visit(self)

    def visited_Eq(self, eq: Eq):
        eq.lhs.visit(self)
        eq.rhs.visit(self)

    def visited_Func(self, func: Func):
        if func.name in self.functions:
            if len(func.terms) != self.functions[func.name]:
                self.valid = False
                return
        else:
            self.functions[func.name] = len(func.terms)

        for term in func.terms:
            term.visit(self)

    def visited_Var(self, var: Var):
        pass

    def visited_Const(self, const: Const):
        pass
