from src.Model.PropositionalExpressionTree import Atom

from src.TableauxBuilder.BaseTableauxBuilder import *


class PropositionalTableauxBuilder(BaseTableauxBuilder):
    def visited_Atom(self, atom: Atom):
        self.sequent[false_atoms if self.visiting_false else true_atoms].append(atom)
