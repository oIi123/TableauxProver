from src.Model.PropositionalExpressionTree import Impl, Atom
from src.TableauxBuilder.BaseTableauxBuilder import *
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder


class IpcTableauxBuilder(PropositionalTableauxBuilder):
    def is_done(self):
        if self.is_closed():
            return True
        if super().is_done():
            return len(self.sequent[certain_falsehood_exprs]) == 0 and len(self.sequent[processed_true_impls]) == 0
        else:
            return False

    def process_multiprocess_exprs(self) -> bool:
        options = [(expr.priority(False), expr) for expr in self.sequent[certain_falsehood_exprs]]
        options.sort(key=lambda tpl: tpl[0])

        if len(options) > 0:
            self.visiting_certain_falsehood_exprs = True
            expr = options[0][1]
            expr.visit(self)
            if expr in self.sequent[certain_falsehood_exprs]:
                self.sequent[certain_falsehood_exprs].remove(expr)
        elif len(self.sequent[processed_true_impls]) > 0:
            # calculate least processed true impl
            kv_list = [(k, v) for k, v in self.sequent[processed_true_impls].items()]
            kv_list.sort(key=lambda x: x[1])

            # increase process counter for true impl
            self.sequent[processed_true_impls][kv_list[0][0]] += 1
            self.sequent[true_exprs].append(kv_list[0][0])
        else:
            raise Exception("No more multiprocess expressions available")

    def visited_Not(self, n: Not):
        if self.visiting_false or self.visiting_certain_falsehood_exprs:
            self.clear_false()
            self.add_to(true_exprs, n.expr)
        else:
            self.add_to(certain_falsehood_exprs, n.expr)

    def visited_And(self, a: And):
        if self.visiting_certain_falsehood_exprs:
            lhs = self.create_copy()
            rhs = self.create_copy()

            lhs.clear_false()
            rhs.clear_false()

            lhs.sequent[certain_falsehood_exprs].remove(a)
            rhs.sequent[certain_falsehood_exprs].remove(a)

            lhs.add_to(certain_falsehood_exprs, a.lhs)
            rhs.add_to(certain_falsehood_exprs, a.rhs)

            self.children.append(lhs)
            self.children.append(rhs)
        else:
            super().visited_And(a)

    def visited_Or(self, o: Or):
        if self.visiting_certain_falsehood_exprs:
            self.add_to(certain_falsehood_exprs, o.lhs)
            self.add_to(certain_falsehood_exprs, o.rhs)
        else:
            super().visited_Or(o)

    def visited_Impl(self, impl: Impl):
        if self.visiting_certain_falsehood_exprs or self.visiting_false:
            self.clear_false()
            self.sequent[true_exprs].append(impl.lhs)
            self.sequent[false_exprs].append(impl.rhs)
        else:
            lhs = self.create_copy(remove_true=impl)
            rhs = self.create_copy(remove_true=impl)

            if impl not in lhs.sequent[processed_true_impls]:
                lhs.sequent[processed_true_impls][impl] = 0
            lhs.add_to(false_exprs, impl.lhs)
            rhs.add_to(true_exprs, impl.rhs)

            self.children.append(lhs)
            self.children.append(rhs)

    def visited_Eq(self, eq: Eq):
        side = false_exprs if self.visiting_false else true_exprs
        if self.visiting_certain_falsehood_exprs:
            side = certain_falsehood_exprs
        
        subst = And(Impl(eq.lhs, eq.rhs), Impl(eq.rhs, eq.lhs))
        self.add_to(side, subst)

    def visited_Atom(self, atom: Atom):
        if self.visiting_certain_falsehood_exprs:
            self.add_to(certain_falsehood_atoms, atom)
        else:
            super().visited_Atom(atom)
