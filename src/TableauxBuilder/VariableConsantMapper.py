from src.Model.FoplExpressionTree import *


class VariableConstantMapper:
    visit_idx = 0

    def __init__(self, mapping: dict):
        self.mapping = mapping

    def map_expr(self, expr: Expr):
        expr.visit(self)

    def replace_variables(self, predicate_or_func: Predicate):
        for i, term in enumerate(predicate_or_func.terms):
            if type(term) == Var:
                if term.name in self.mapping:
                    mapping = self.mapping[term.name]
                    if type(mapping) == str:
                        predicate_or_func.terms[i] = Const(mapping)
                    else:
                        predicate_or_func.terms[i] = mapping
            elif type(term) == Func:
                self.replace_variables(term)

    def visited_Predicate(self, predicate: Predicate):
        self.replace_variables(predicate)

    def visited_Not(self, n: Not):
        n.expr.visit(self)

    def visited_Quantor(self, quantor: Quantor):
        # Check if quantor variable overrides a mapping variable
        stashed_mapping_constant = None
        if quantor.variable.name in self.mapping:
            stashed_mapping_constant = self.mapping[quantor.variable.name]
            del self.mapping[quantor.variable.name]

        quantor.expr.visit(self)

        # Restore stashed variable constant mapping
        if stashed_mapping_constant is not None:
            self.mapping[quantor.variable.name] = stashed_mapping_constant

    def visited_ExistentialQuantor(self, quantor: ExistentialQuantor):
        self.visited_Quantor(quantor)

    def visited_AllQuantor(self, quantor: AllQuantor):
        self.visited_Quantor(quantor)
    
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
