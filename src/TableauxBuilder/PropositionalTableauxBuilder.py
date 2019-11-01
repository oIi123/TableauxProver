from src.Model.PropositionalExpressionTree import Atom

from src.TableauxBuilder.BaseTableauxBuilder import *


class PropositionalTableauxBuilder(BaseTableauxBuilder):
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

    def is_closed(self):
        if len(self.children) == 0:
            for true_atom in self.sequent[true_atoms]:
                if true_atom in self.sequent[false_atoms]:
                    return True
            return False
        else:
            for child in self.children:
                if not child.is_closed():
                    return False
            return True

    def visited_Atom(self, atom: Atom):
        self.sequent[false_atoms if self.visiting_false else true_atoms].append(atom)
