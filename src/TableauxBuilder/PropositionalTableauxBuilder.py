from src.Model.PropositionalExpressionTree import Atom

from src.TableauxBuilder.BaseTableauxBuilder import *


class PropositionalTableauxBuilder(BaseTableauxBuilder):
    def print(self, indent=0):
        tab = "\t" * indent
        print(f"{tab}done: {self.is_done()}, closed: {self.is_closed()}")
        if len(self.children) == 0:
            false_e = f"\n\t\t{tab}".join([str(i) for i in self.sequent[false_exprs]])
            true_e = f"\n\t\t{tab}".join([str(i) for i in self.sequent[true_exprs]])
            exprs = f"{tab}exprs: [" \
                    f"\n\t{tab}false: [\n\t\t{tab}{false_e}\n\t{tab}]," \
                    f"\n\t{tab}true: [\n\t\t{tab}{true_e}\n\t{tab}]\n{tab}],"
            print(exprs)
            false_a = f"\n\t\t{tab}".join([str(i) for i in self.sequent[false_atoms]])
            true_a = f"\n\t\t{tab}".join([str(i) for i in self.sequent[true_atoms]])
            atoms = f"{tab}atoms: [" \
                    f"\n\t{tab}false: [\n\t\t{tab}{false_a}\n\t{tab}]," \
                    f"\n\t{tab}true: [\n\t\t{tab}{true_a}\n\t{tab}]\n{tab}],"
            print(atoms)
        print(f"{tab}children: [")
        for child in self.children:
            print(f"\t{tab}[")
            child.print(indent+1)
            print(f"\t{tab}],")
        print(f"{tab}]")

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

    def visited_Atom(self, atom: Atom):
        self.add_to(false_atoms if self.visiting_false else true_atoms, atom)
