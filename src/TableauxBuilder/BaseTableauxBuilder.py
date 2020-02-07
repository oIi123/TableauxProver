from abc import abstractmethod
from typing import Callable
from src.Model.PropositionalExpressionTree import Expr, Not, And, Impl, Or, Eq
import copy

false_exprs = "false"
true_exprs = "true"
false_atoms = "false_atoms"
true_atoms = "true_atoms"
false_processed = "false_processed"
true_processed = "true_processed"
processed_true_impls = "processed_true_impls"
processed_true_quantor_expressions = "processed_true_quantor_expressions"
processed_false_quantor_expressions = "processed_false_quantor_expressions"
established_constants = "established_constants"
variable_constant_mapping = "variable_constant_mapping"
certain_falsehood_exprs = "certain_falsehood_exprs"
certain_falsehood_atoms = "certain_falsehood_atoms"
processed_certain_false_exquantor_exprs = "processed_certain_false_exquantor_exprs"
processed_certain_false_allquantor_exprs = "processed_certain_false_allquantor_exprs"


class BaseTableauxBuilder:
    visiting_false = True
    visiting_certain_falsehood_exprs = False

    left_side_sign = "T"
    right_side_sign = "F"

    last_multiprocess_false = None
    last_multiprocess_true = None

    def __init__(self, sequent: dict = None, **kwargs):
        self.visit_idx = kwargs.get('visit_idx', 0)

        if sequent is not None:
            self.sequent = sequent
        else:
            self.sequent = {
                false_exprs: kwargs.get('false_exprs', []),
                true_exprs: kwargs.get('true_exprs', []),
                false_atoms: [],
                true_atoms: [],
                false_processed: [],
                true_processed: [],
                certain_falsehood_exprs: [],
                certain_falsehood_atoms: [],
                processed_true_impls: dict(),
                processed_true_quantor_expressions: dict(),
                processed_false_quantor_expressions: dict(),
                processed_certain_false_exquantor_exprs: dict(),
                processed_certain_false_allquantor_exprs: dict(),
                established_constants: kwargs.get('constants', []),
                variable_constant_mapping: dict(),
            }
        self.done = False
        self.children = []
        self.parent = kwargs.get('parent')

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

            self.visiting_certain_falsehood_exprs = False
            self.visit_expr(options[0][1], options[0][2])

    def visit_expr(self, false_side, expr):
        self.visiting_false = false_side
        expr.visit(self)
        side = false_exprs if false_side else true_exprs
        processed_side = false_processed if false_side else true_processed
        partially_processed_side = processed_false_quantor_expressions if false_side else processed_true_quantor_expressions
        last = self.last_multiprocess_false if false_side else self.last_multiprocess_true
        if expr == last and expr in self.sequent[side]:
            # if expr is a partially processed, only remove it from exprs and add to partially processed
            self.sequent[side].remove(expr)
            if self.parent is not None:
                self.parent.add_multiprocess(side, partially_processed_side, expr)
        elif expr in self.sequent[side]:
            self.add_processed(side, processed_side, expr)

    def add_processed(self, side, processed_side, expr):
        if expr in self.sequent[side]:
            self.sequent[side].remove(expr)
            self.sequent[processed_side].append(expr)

            if self.parent is not None:
                self.parent.add_processed(side, processed_side, expr)

    def add_multiprocess(self, side, m_p_side, expr):
        if expr in self.sequent[side]:
            self.sequent[side].remove(expr)
            self.sequent[m_p_side][expr] = []

            if self.parent is not None:
                self.parent.add_multiprocess(side, m_p_side, expr)

    def create_copy(self, remove_false=None, remove_true=None):
        cpy = type(self)(sequent=copy.deepcopy(self.sequent), parent=self, visit_idx=self.visit_idx+1)
        cpy.sequent[true_processed] = list()
        cpy.sequent[false_processed] = list()

        if remove_false is not None:
            cpy.sequent[false_exprs].remove(remove_false)
        if remove_true is not None:
            cpy.sequent[true_exprs].remove(remove_true)

        return cpy

    def clear_false(self):
        self.sequent[false_exprs] = []
        self.sequent[false_atoms] = []

    def add_to(self, side: str, expr: Expr):
        self.sequent[side].append(expr)

        if side not in [true_atoms, false_atoms]:
            expr.visit_idx = self.visit_idx
            self.visit_idx += 1

    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def process_multiprocess_exprs(self) -> bool:
        pass

    def is_closed(self):
        if len(self.children) == 0:
            for true_atom in self.sequent[true_atoms]:
                if true_atom in self.sequent[false_atoms] or true_atom in self.sequent[certain_falsehood_atoms]:
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
        self.add_to(true_exprs if self.visiting_false else false_exprs, n.expr)

    def visited_And(self, a: And):
        if self.visiting_false:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = self.create_copy(remove_false=a)
            rhs = self.create_copy(remove_false=a)
            lhs.add_to(false_exprs, a.lhs)
            rhs.add_to(false_exprs, a.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            self.add_to(true_exprs, a.lhs)
            self.add_to(true_exprs, a.rhs)

    def visited_Or(self, o: Or):
        if self.visiting_false:
            self.add_to(false_exprs, o.lhs)
            self.add_to(false_exprs, o.rhs)
        else:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = self.create_copy(remove_true=o)
            rhs = self.create_copy(remove_true=o)
            lhs.add_to(true_exprs, o.lhs)
            rhs.add_to(true_exprs, o.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Impl(self, impl: Impl):
        if self.visiting_false:
            self.add_to(true_exprs, impl.lhs)
            self.add_to(false_exprs, impl.rhs)
        else:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = self.create_copy(remove_true=impl)
            rhs = self.create_copy(remove_true=impl)
            lhs.add_to(false_exprs, impl.lhs)
            rhs.add_to(true_exprs, impl.rhs)
            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Eq(self, eq: Eq):
        if self.visiting_false:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = self.create_copy(remove_false=eq)
            rhs = self.create_copy(remove_false=eq)

            lhs.add_to(false_exprs, eq.lhs)
            lhs.add_to(true_exprs, eq.rhs)

            rhs.add_to(true_exprs, eq.lhs)
            rhs.add_to(false_exprs, eq.rhs)
            self.children.append(lhs)
            self.children.append(rhs)
        else:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = self.create_copy(remove_true=eq)
            rhs = self.create_copy(remove_true=eq)

            lhs.add_to(true_exprs, eq.lhs)
            lhs.add_to(true_exprs, eq.rhs)

            rhs.add_to(false_exprs, eq.lhs)
            rhs.add_to(false_exprs, eq.rhs)

            self.children.append(lhs)
            self.children.append(rhs)

    def get_drawn_width(self, get_width_from_str: Callable[[str], int],
                        margin: int) -> (int, int):
        """
        Calculates the width of this Tableau Branch
        """
        exprs = self.get_all_exprs()
        max_expr_width_left = max(
                                [get_width_from_str(str(expr))
                                    for expr in exprs[0]],
                                default=0)

        max_expr_width_right = max(
                                [get_width_from_str(str(expr))
                                    for expr in exprs[1]],
                                default=0)

        if len(self.children) == 0:
            return (max_expr_width_left, max_expr_width_right)

        left_child_width = self.children[0].get_drawn_width(
                                                    get_width_from_str,
                                                    margin)
        right_child_width = self.children[1].get_drawn_width(
                                                    get_width_from_str,
                                                    margin)

        width_left = max([sum(left_child_width), max_expr_width_left])
        width_right = max([sum(right_child_width), max_expr_width_right])

        return (width_left + margin, width_right + margin)

    def get_all_exprs(self) -> (list, list):
        """
        Returns all expressions left and right in the tableau
        """
        exprs = (list(), list())
        for fun in [
                    self.get_processed_exprs,
                    self.get_atom_exprs,
                    self.get_unprocessed_exprs,
                    self.get_partially_processed_exprs,
                    ]:
            tmp = fun()
            exprs[0].extend(tmp[0])
            exprs[1].extend(tmp[1])
        return exprs

    def get_processed_exprs(self):
        """
        Returns all fully processed expressions
        """
        return (
            self.sequent[true_processed],
            self.sequent[false_processed])

    def get_partially_processed_exprs(self):
        """
        Returns all partially unprocessed expressions that are not
        partially unprocessed in parent
        """
        return ([], [])
    
    def get_atom_exprs(self):
        """
        Returns all atoms not in the parent tableau
        """
        true_atoms_parent = len(self.parent.sequent[true_atoms]) if self.parent else 0
        false_atoms_parent = len(self.parent.sequent[false_atoms]) if self.parent else 0

        return  (
            self.sequent[true_atoms][true_atoms_parent:],
            self.sequent[false_atoms][false_atoms_parent:])

    def get_unprocessed_exprs(self):
        """
        Returns all unprocessed expressions that are not unprocessed in parent
        """
        true_parent = len(self.parent.sequent[true_exprs]) if self.parent else 0
        false_parent = len(self.parent.sequent[false_exprs]) if self.parent else 0

        return (
            self.sequent[true_exprs][true_parent:],
            self.sequent[false_exprs][false_parent:])
