from src.Model.PropositionalExpressionTree import Impl, Atom
from src.TableauxBuilder.BaseTableauxBuilder import *


class IpcTableauxBuilder(BaseTableauxBuilder):
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
            impls = f"\n\t\t".join([str(i) for i in self.sequent[considered_impls]])
            print(f"{tab}considered_impls: [\n\t{tab}{impls}\n{tab}],")
        print(f"{tab}children: [")
        for child in self.children:
            print(f"\t{tab}[")
            child.print(indent+1)
            print(f"\t{tab}],")
        print(f"{tab}]")

    def is_done(self) -> bool:
        if len(self.children) == 0:
            for true_atom in self.sequent[true_atoms]:
                if true_atom in self.sequent[false_atoms]:
                    return True
            if len(self.sequent[false_exprs]) == len(self.sequent[true_exprs]) == 0:
                return len(self.sequent[considered_impls]) == 0
            else:
                return False
        else:
            for child in self.children:
                if not child.is_done():
                    return False
            return True

    def process_multiprocess_exprs(self):
        if len(self.sequent[considered_impls]) > 0:
            self.sequent[true_exprs].append(self.sequent[considered_impls][0])

    def visited_Impl(self, impl: Impl):
        if self.visiting_false:
            self.sequent[true_exprs].append(impl.lhs)
            self.sequent[false_exprs] = [impl.rhs]
            self.sequent[false_atoms] = []
        else:
            # Create new fork -> Children of same TableauxBuilder type as self
            lhs = type(self)(sequent=copy.deepcopy(self.sequent))
            lhs.sequent[true_exprs].remove(impl)
            lhs.sequent[considered_impls].append(impl)
            lhs.sequent[false_exprs] = [impl.lhs]
            self.children.append(lhs)

            rhs = type(self)(sequent=copy.deepcopy(self.sequent))
            rhs.sequent[true_exprs].remove(impl)
            rhs.sequent[considered_impls].append(impl)
            rhs.sequent[true_exprs].append(impl.rhs)
            self.children.append(rhs)

    def visited_Atom(self, atom: Atom):
        self.sequent[false_atoms if self.visiting_false else true_atoms].append(atom)
