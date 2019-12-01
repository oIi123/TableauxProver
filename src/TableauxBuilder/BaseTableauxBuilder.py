from abc import abstractmethod

from src.Model.PropositionalExpressionTree import Expr, Not, And, Impl, Or, Eq
import copy

false_exprs = "false"
true_exprs = "true"
false_atoms = "false_atoms"
true_atoms = "true_atoms"
considered_impls = "considered_impls"


class BaseTableauxBuilder:
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
                considered_impls: [],
            }
        self.done = False
        self.children = []

    def auto_resolve(self, debug=False, depth=0):
        while not self.is_done():
            if debug:
                self.print(depth)
            if len(self.children) > 0:
                for child in self.children:
                    child.auto_resolve(debug, depth+1)
                return

            # Options Tuple (Priority, False_Side, Expression)
            options = [(expr.priority(False), True, expr) for expr in self.sequent[false_exprs]]
            options.extend([(expr.priority(True), False, expr) for expr in self.sequent[true_exprs]])
            options.sort(key=lambda tpl: tpl[0])

            if len(options) == 0:
                self.process_multiprocess_exprs()
                continue

            self.visit_expr(options[0][1], options[0][2])

    def visit_expr(self, false_side, expr):
        self.visiting_false = false_side
        expr.visit(self)
        side = false_exprs if false_side else true_exprs
        if expr in self.sequent[side]:
            self.sequent[side].remove(expr)


    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def process_multiprocess_exprs(self) -> bool:
        pass

    def is_closed(self):
        if len(self.children) == 0:
            for true_atom in self.sequent[true_atoms]:
                if true_atom in self.sequent[false_atoms]:
                    return True
        else:
            for child in self.children:
                if not child.is_closed():
                    return False
            return True
        return False

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

    def visited_Not(self, n: Not):
        self.sequent[true_exprs if self.visiting_false else false_exprs].append(n.expr)

    def visited_And(self, a: And):
        if self.visiting_false:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = type(self)(sequent=copy.deepcopy(self.sequent))
            rhs = type(self)(sequent=copy.deepcopy(self.sequent))
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
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = type(self)(sequent=copy.deepcopy(self.sequent))
            rhs = type(self)(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(o)
            rhs.sequent[true_exprs].remove(o)
            lhs.sequent[true_exprs].append(o.lhs)
            rhs.sequent[true_exprs].append(o.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Impl(self, impl: Impl):
        if self.visiting_false:
            self.sequent[true_exprs].append(impl.lhs)
            self.sequent[false_exprs].append(impl.rhs)
        else:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = type(self)(sequent=copy.deepcopy(self.sequent))
            rhs = type(self)(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(impl)
            rhs.sequent[true_exprs].remove(impl)
            lhs.sequent[false_exprs].append(impl.lhs)
            rhs.sequent[true_exprs].append(impl.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Eq(self, eq: Eq):
        if self.visiting_false:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = type(self)(sequent=copy.deepcopy(self.sequent))
            rhs = type(self)(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[false_exprs].remove(eq)
            rhs.sequent[false_exprs].remove(eq)

            lhs.sequent[false_exprs].append(eq.lhs)
            lhs.sequent[true_exprs].append(eq.rhs)

            rhs.sequent[true_exprs].append(eq.lhs)
            rhs.sequent[false_exprs].append(eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = type(self)(sequent=copy.deepcopy(self.sequent))
            rhs = type(self)(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(eq)
            rhs.sequent[true_exprs].remove(eq)
            lhs.sequent[true_exprs].append(eq.lhs)
            lhs.sequent[true_exprs].append(eq.rhs)
            rhs.sequent[false_exprs].append(eq.lhs)
            rhs.sequent[false_exprs].append(eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
