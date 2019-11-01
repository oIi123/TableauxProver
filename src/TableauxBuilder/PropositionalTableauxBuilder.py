from src.Model.FoplExpressionTree import Expr, Not, And, Impl, Or, Eq
from src.Model.PropositionalExpressionTree import Atom
import copy


class PropositionalTableauxBuilder:
    visiting_false = True

    def __init__(self, expr: Expr = None, sequent: dict = None):
        if sequent is not None:
            self.sequent = sequent
        else:
            self.sequent = {
                "false": [expr],
                "true": [],
                "false_atoms": [],
                "true_atoms": []
            }
        self.done = False
        self.children = []

    def is_done(self):
        if len(self.children) == 0:
            for true_atom in self.sequent["true_atoms"]:
                if true_atom in self.sequent["false_atoms"]:
                    return True
            return len(self.sequent["false"]) == len(self.sequent["true"]) == 0
        else:
            for child in self.children:
                if not child.is_done():
                    return False
            return True

    def __str__(self):
        exprs = f"exprs: [false: {[str(i) for i in self.sequent['false']]} true: {[str(i) for i in self.sequent['true']]}]\n"
        atoms = f"atoms: [false: {[str(i) for i in self.sequent['false_atoms']]} true: {[str(i) for i in self.sequent['true_atoms']]}]\n"
        children = f"children: [{[str(i) for i in self.children]}]\n"
        return exprs + atoms + children

    def visit(self):
        if len(self.children) > 0:
            for child in self.children:
                if not child.is_done():
                    child.visit()
                    return
            return
        if len(self.sequent["false"]) > 0:
            self.visiting_false = True
            expr = self.sequent["false"][-1]
            expr.visit(self)
            self.sequent["false"].remove(expr)
        else:
            self.visiting_false = False
            expr = self.sequent["true"][-1]
            expr.visit(self)
            self.sequent["true"].remove(expr)

    def visited_Atom(self, atom: Atom):
        self.sequent["false_atoms" if self.visiting_false else "true_atoms"].append(atom)

    def visited_Not(self, n: Not):
        self.sequent["true" if self.visiting_false else "false"].append(n.expr)

    def visited_And(self, a: And):
        if self.visiting_false:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent["false"].remove(a)
            rhs.sequent["false"].remove(a)
            lhs.sequent["false"].append(a.lhs)
            rhs.sequent["false"].append(a.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            self.sequent["true"].append(a.lhs)
            self.sequent["true"].append(a.rhs)

    def visited_Or(self, o: Or):
        if self.visiting_false:
            self.sequent["false"].append(o.lhs)
            self.sequent["false"].append(o.rhs)
        else:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent["true"].remove(o)
            rhs.sequent["true"].remove(o)
            lhs.sequent["true"].append(o.lhs)
            rhs.sequent["true"].append(o.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Impl(self, impl: Impl):
        if self.visiting_false:
            self.sequent["false"].append(impl.lhs)
            self.sequent["true"].append(impl.rhs)
        else:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent["true"].remove(impl)
            rhs.sequent["true"].remove(impl)
            lhs.sequent["false"].append(impl.lhs)
            rhs.sequent["true"].append(impl.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Eq(self, eq: Eq):
        if self.visiting_false:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent["false"].remove(eq)
            rhs.sequent["false"].remove(eq)

            lhs.sequent["false"].append(eq.lhs)
            lhs.sequent["true"].append(eq.rhs)

            rhs.sequent["true"].append(eq.lhs)
            rhs.sequent["false"].append(eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent["true"].remove(eq)
            rhs.sequent["true"].remove(eq)
            lhs.sequent["true"].append(eq.lhs)
            lhs.sequent["true"].append(eq.rhs)
            rhs.sequent["false"].append(eq.lhs)
            rhs.sequent["false"].append(eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
