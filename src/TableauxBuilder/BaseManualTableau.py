from src.builder_factory import *
import src.TableauxBuilder.BaseTableauxBuilder as BaseTableauxBuilder
from src.Model.FoplExpressionTree import AllQuantor, ExistentialQuantor


class ConstantReplacer:
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def replace(self, expr):
        expr.visit(self)

    def __getattribute__(self, name):
        if name.startswith('visited_') and name != 'visited_Const':
            def visited_any(expr):
                for attr in ['lhs', 'rhs', 'expr']:
                    if hasattr(expr, attr):
                        getattr(expr, attr).visit(self)
                if hasattr(expr, 'terms'):
                    for term in expr.terms:
                        term.visit(self)
            return visited_any
        return super().__getattribute__(name)

    def visited_Const(self, const):
        if const.name == self.old:
            const.name = self.new

class BaseManualTableau:
    def __init__(self, logic_type, tableau_builder):
        self.logic_type = logic_type
        self.tableau_builder = tableau_builder

        self.expr = None
        self.perm = None
        self.side = None
        self.processed_side = None

    def merge(self, expr, true_exprs, false_exprs, cf_exprs, constants):
        """Merges the derivation into the tableau if valid
        
        Args:
            expr ((Expr, Expr, Expr)): Expression to derive
            expr_side (int): 0=true, 1=false, 2=cf
            true_exprs ([Expr]): Expression list, true side
            false_exprs ([Expr]): Expression list, false side
            cf_exprs ([Expr]): Expression list, cf side
            constants ([[str]]): List of constants
        Returns:
            bool: True if derivation was correct and merge successfull
        """
        t, f, cf = expr
        false_side = False
        certainly_false_side = False
        self.side = BaseTableauxBuilder.true_exprs
        self.processed_side = BaseTableauxBuilder.true_processed
        if t is not None:
            self.expr = t
            if type(self.expr) is AllQuantor:
                # multiprocess expr
                self.processed_side = BaseTableauxBuilder.processed_true_quantor_expressions
        elif f is not None:
            self.expr = f
            false_side = True
            self.side = BaseTableauxBuilder.false_exprs
            self.processed_side = BaseTableauxBuilder.false_processed
            if type(self.expr) is ExistentialQuantor:
                # multiprocess expr
                self.processed_side = BaseTableauxBuilder.processed_false_quantor_expressions
        elif cf is not None:
            self.expr = cf
            false_side = True
            certainly_false_side = True
            self.side = BaseTableauxBuilder.certain_falsehood_exprs
            self.processed_side = BaseTableauxBuilder.certain_falsehood_processed
        expr_permutations = self.expr.permute()
        for perm in expr_permutations:
            self.perm = perm
            new_tableau_builder = create_tableau_builder(
                                        self.logic_type, [], [], 
                                        0, cf=[],
                                        constants=self.tableau_builder.sequent[BaseTableauxBuilder.established_constants][:])
            new_tableau_builder.sequent[self.side].append(self.expr)
            new_tableau_builder.visiting_false = false_side
            new_tableau_builder.visiting_certain_falsehood_exprs = certainly_false_side

            # if multiprocess, set already processed ones
            if self.ex_constant_expr():
                if self.expr in self.tableau_builder.sequent[self.processed_side]:
                    cpy = self.tableau_builder.sequent[self.processed_side][self.expr][:]
                    new_tableau_builder.sequent[self.processed_side][self.expr] = cpy

            self.perm.visit(new_tableau_builder)
            if self.expr in new_tableau_builder.sequent[self.side]:
                new_tableau_builder.sequent[self.side].remove(self.expr)
                if self.processed_side not in [
                        BaseTableauxBuilder.processed_false_quantor_expressions,
                        BaseTableauxBuilder.processed_true_quantor_expressions]:
                    new_tableau_builder.sequent[self.processed_side].append(self.expr)
            if len(new_tableau_builder.children) == 0:
                # check if correct single derivation
                if self.check_single(true_exprs, false_exprs, cf_exprs, new_tableau_builder, constants):
                    return True
            else:
                # check if correct branch derivation
                if self.check_branch(true_exprs, false_exprs, cf_exprs, new_tableau_builder):
                    return True
        # no valid derivation entered
        return False

    def check_single(self, true_exprs, false_exprs, cf_exprs, new_tableau_builder, constants):
        if len(true_exprs) == len(false_exprs) == len(cf_exprs) == 1:
            true_exprs = true_exprs[0]
            false_exprs = false_exprs[0]
            cf_exprs = cf_exprs[0]

            new_const_expr = self.new_constant_expr()
            ex_const_expr = self.ex_constant_expr()
            len_consts = len(self.tableau_builder.sequent[BaseTableauxBuilder.established_constants])
            if new_const_expr or ex_const_expr and len_consts == 0:
                # check if ONE new constant introduced
                new_introduced = None
                for constant in constants:
                    if constant not in self.tableau_builder.sequent[BaseTableauxBuilder.established_constants]:
                        if new_introduced is not None:
                            # multiple new constants
                            return False
                        new_introduced = constant
                if new_introduced is None:
                    return False

                new_introduced_auto = new_tableau_builder.sequent[BaseTableauxBuilder.established_constants][-1]
                self.replace_constant(new_introduced_auto, new_introduced, new_tableau_builder)

                if ex_const_expr:
                    new_tableau_builder.sequent[self.processed_side][self.expr] = [new_introduced]

            # check correct derivations
            for exprs, sequent_id in [
                (true_exprs, BaseTableauxBuilder.true_exprs),
                (false_exprs, BaseTableauxBuilder.false_exprs),
                (cf_exprs, BaseTableauxBuilder.certain_falsehood_exprs),
            ]:
                if not self.check_equal_sequent(exprs, new_tableau_builder, sequent_id):
                    return False

            self.tableau_builder.merge(new_tableau_builder)
            if ex_const_expr:
                self.set_multiprocessed()
            else:
                self.set_processed()
            return True
        return False

    def check_branch(self, true_exprs, false_exprs, cf_exprs, new_tableau_builder):
        if len(new_tableau_builder.children) == len(true_exprs) == len(false_exprs) == len(cf_exprs):
            a = new_tableau_builder.children
            b = [new_tableau_builder.children[1], new_tableau_builder.children[0]]
            for children in [a, b]:
                correct = True
                for i, child in enumerate(children):
                    for exprs, sequent_id in [
                        (true_exprs[i], BaseTableauxBuilder.true_exprs),
                        (false_exprs[i], BaseTableauxBuilder.false_exprs),
                        (cf_exprs[i], BaseTableauxBuilder.certain_falsehood_exprs),
                    ]:
                        if not self.check_equal_sequent(exprs, child, sequent_id):
                            correct = False
                            break
                    if not correct:
                        break
            
                if correct:
                    self.tableau_builder.merge(new_tableau_builder)
                    self.set_processed()
                    return True
        return False

    def check_equal_sequent(self, exprs, tableau, sequent_id):
        if len(exprs) != len(tableau.sequent[sequent_id]):
            return False
        for expr in exprs:
            if expr not in tableau.sequent[sequent_id]:
                return False
        return True

    def set_processed(self, tableau=None):
        tableau = self.tableau_builder if tableau is None else tableau

        if len(tableau.children) == 0:
            tableau.add_processed(self.side, self.processed_side, self.expr)
            return
        
        for child in tableau.children:
            self.set_processed(child)

    def set_multiprocessed(self, tableau=None):
        tableau = self.tableau_builder if tableau is None else tableau

        if len(tableau.children) == 0:
            tableau.add_multiprocess(self.side, self.processed_side, self.expr)
            return
        
        for child in tableau.children:
            self.set_multiprocessed(child)

    def new_constant_expr(self):
        if self.side == BaseTableauxBuilder.false_exprs and type(self.perm) is AllQuantor:
            return True
        elif self.side == BaseTableauxBuilder.true_exprs and type(self.perm) is ExistentialQuantor:
            return True
        return False
    
    def ex_constant_expr(self):
        if self.side == BaseTableauxBuilder.false_exprs and type(self.perm) is ExistentialQuantor:
            return True
        elif self.side == BaseTableauxBuilder.true_exprs and type(self.perm) is AllQuantor:
            return True
        return False

    def replace_constant(self, old, new, tableau):
        tableau.sequent[BaseTableauxBuilder.established_constants].remove(old)
        tableau.sequent[BaseTableauxBuilder.established_constants].append(new)
        for expr in tableau.sequent[BaseTableauxBuilder.false_exprs] + tableau.sequent[BaseTableauxBuilder.true_exprs]:
            self.replace_expr_constant(old, new, expr)
    
    def replace_expr_constant(self, old, new, expr):
        replacer = ConstantReplacer(old, new)
        replacer.replace(expr)
