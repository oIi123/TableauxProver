from src.Model.FoplExpressionTree import *


class FoplValidator:
    def __init__(self):
        self.predicates: [Predicate] = []
        self.functions: [Func] = []
        self.valid = True

    def validate(self, expr: Expr) -> bool:
        expr.visit(self)
        return self.valid

    def visited_Predicate(self, predicate: Predicate):
        for pred in self.predicates:
            if pred.name == predicate.name:
                if len(pred.terms) != len(predicate.terms):
                    self.valid = False
                for term in predicate.terms:
                    term.visit(self)
                return
        self.predicates.append(predicate)
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
        for f in self.functions:
            if f.name == func.name:
                if len(f.terms) != len(func.terms):
                    self.valid = False
                for term in func.terms:
                    term.visit(self)
                return
        self.functions.append(func)
        for term in func.terms:
            term.visit(self)

    def visited_Var(self, var: Var):
        pass
