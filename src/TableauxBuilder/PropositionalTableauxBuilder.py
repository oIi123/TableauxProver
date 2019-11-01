from src.Model.FoplExpressionTree import Expr, Not, And, Impl, Or, Eq
from src.Model.PropositionalExpressionTree import Atom
import copy

false_exprs = "false"
true_exprs = "true"
false_atoms = "false_atoms"
true_atoms = "true_atoms"


class PropositionalTableauxBuilder:
    visiting_false = True

    def __init__(self, expr: Expr = None, sequent: dict = None):
        if sequent is not None:
            self.sequent = sequent
        else:
            self.sequent = {
                false_exprs: [expr],
                true_exprs: [],
                false_atoms: [],
                true_atoms: [],
            }
        self.done = False
        self.children = []

    def is_done(self):
        if len(self.children) == 0:
            for true_atom in self.sequent[true_atoms]:
                if true_atom in self.sequent[false_atoms]:
                    return True
            return len(self.sequent[false_exprs]) == len(self.sequent[true_exprs]) == 0
        else:
            for child in self.children:
                if not child.is_done():
                    return False
            return True

    def __str__(self):
        exprs = f"exprs: [false: {[str(i) for i in self.sequent[false_exprs]]} true: {[str(i) for i in self.sequent[true_exprs]]}]\n"
        atoms = f"atoms: [false: {[str(i) for i in self.sequent[false_atoms]]} true: {[str(i) for i in self.sequent[true_atoms]]}]\n"
        children = f"children: [{[str(i) for i in self.children]}]\n"
        return exprs + atoms + children

    def visit(self):
        if len(self.children) > 0:
            for child in self.children:
                if not child.is_done():
                    child.visit()
                    return
            return
        if len(self.sequent[false_exprs]) > 0:
            self.visiting_false = True
            expr = self.sequent[false_exprs][-1]
            expr.visit(self)
            self.sequent[false_exprs].remove(expr)
        else:
            self.visiting_false = False
            expr = self.sequent[true_exprs][-1]
            expr.visit(self)
            self.sequent[true_exprs].remove(expr)

    def visited_Atom(self, atom: Atom):
        self.sequent[false_atoms if self.visiting_false else true_atoms].append(atom)

    def visited_Not(self, n: Not):
        self.sequent[true_exprs if self.visiting_false else false_exprs].append(n.expr)

    def visited_And(self, a: And):
        if self.visiting_false:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[false_exprs].remove(a)
            rhs.sequent[false_exprs].remove(a)
            lhs.sequent[false_exprs].append(a.lhs)
            rhs.sequent[false_exprs].append(a.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            self.sequent[true_exprs].append(a.lhs)
            self.sequent[true_exprs].append(a.rhs)

    def visited_Or(self, o: Or):
        if self.visiting_false:
            self.sequent[false_exprs].append(o.lhs)
            self.sequent[false_exprs].append(o.rhs)
        else:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(o)
            rhs.sequent[true_exprs].remove(o)
            lhs.sequent[true_exprs].append(o.lhs)
            rhs.sequent[true_exprs].append(o.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Impl(self, impl: Impl):
        if self.visiting_false:
            self.sequent[false_exprs].append(impl.lhs)
            self.sequent[true_exprs].append(impl.rhs)
        else:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(impl)
            rhs.sequent[true_exprs].remove(impl)
            lhs.sequent[false_exprs].append(impl.lhs)
            rhs.sequent[true_exprs].append(impl.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Eq(self, eq: Eq):
        if self.visiting_false:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[false_exprs].remove(eq)
            rhs.sequent[false_exprs].remove(eq)

            lhs.sequent[false_exprs].append(eq.lhs)
            lhs.sequent[true_exprs].append(eq.rhs)

            rhs.sequent[true_exprs].append(eq.lhs)
            rhs.sequent[false_exprs].append(eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            lhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            rhs = PropositionalTableauxBuilder(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(eq)
            rhs.sequent[true_exprs].remove(eq)
            lhs.sequent[true_exprs].append(eq.lhs)
            lhs.sequent[true_exprs].append(eq.rhs)
            rhs.sequent[false_exprs].append(eq.lhs)
            rhs.sequent[false_exprs].append(eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
