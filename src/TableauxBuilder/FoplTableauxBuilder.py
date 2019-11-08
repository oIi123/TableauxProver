from src.Model.FoplExpressionTree import *
from src.TableauxBuilder.BaseTableauxBuilder import *
from src.TableauxBuilder.VariableConsantMapper import VariableConstantMapper

processed_true_quantor_expressions = "processed_true_quantor_expressions"
processed_false_quantor_expressions = "processed_false_quantor_expressions"
established_constants = "established_constants"
variable_constant_mapping = "variable_constant_mapping"


class FoplTableauxBuilder(BaseTableauxBuilder):
    constant_idx = 0

    def __init__(self, tree: FoplExpressionTree = None, sequent: dict = None):
        if sequent is not None:
            super().__init__(sequent=sequent)
        else:
            super().__init__(tree.expr, sequent)
            self.sequent = {
                false_exprs: [tree.expr],
                true_exprs: [],
                false_atoms: [],
                true_atoms: [],
                # Dictionary Mapping Quantors to its already processed constants
                processed_true_quantor_expressions: dict(),
                processed_false_quantor_expressions: dict(),
                established_constants: tree.constants,
                variable_constant_mapping: dict(),
            }

        self.variable_constant_mapper = VariableConstantMapper(self.sequent[variable_constant_mapping])

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
            # If no contradicting atoms exist there are 2 possibilities
            # Either no more expressions are available (on true and false side)
            # Or there are some not processed Constants of an AllQuantor on the true side
            #   or an ExQuantor on the false side
            return (
                    len(self.sequent[false_exprs]) == 0 and
                    len(self.sequent[true_exprs]) == 0 and
                    self.check_unprocessed_quantor_expressions()
            )
        else:
            # The Tree was forked, check all children if they are done
            for child in self.children:
                if not child.is_done():
                    return False
            return True

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
            raise Exception("All possible paths are processed.")
        if len(self.sequent[false_exprs]) > 0:
            self.visiting_false = True
            expr = self.sequent[false_exprs][-1]
            expr.visit(self)
            self.sequent[false_exprs].remove(expr)
        elif len(self.sequent[true_exprs]) > 0:
            self.visiting_false = False
            expr = self.sequent[true_exprs][-1]
            expr.visit(self)
            self.sequent[true_exprs].remove(expr)
        else:
            # All Expressions are processed  -> Process quantors with unprocessed constants
            self.process_quantor_unprocessed_constants()

    def process_quantor_unprocessed_constants(self):
        num_of_constants = len(self.sequent[established_constants])
        for quantor, processed_constants in self.sequent[processed_true_quantor_expressions].items():
            if len(processed_constants) != num_of_constants:
                self.visiting_false = False
                self.generate_existing_constant_expression(quantor)
                return
        for quantor, processed_constants in self.sequent[processed_false_quantor_expressions].items():
            if len(processed_constants) != num_of_constants:
                self.visiting_false = True
                self.generate_existing_constant_expression(quantor)
                return
        raise Exception("There are no more Quantors with unprocessed constants")

    def check_unprocessed_quantor_expressions(self):
        """
        Checks if there are any quantors with unprocessed constants
        :return: Returns true if all quantors processed all constants
        """
        num_of_constants = len(self.sequent[established_constants])
        for processed_constants in self.sequent[processed_true_quantor_expressions].values():
            if len(processed_constants) != num_of_constants:
                return False
        for processed_constants in self.sequent[processed_false_quantor_expressions].values():
            if len(processed_constants) != num_of_constants:
                return False
        return True

    def generate_existing_constant_expression(self, quantor: Quantor):
        processed_quantor_expressions = processed_false_quantor_expressions if self.visiting_false else processed_true_quantor_expressions

        if len(self.sequent[established_constants]) == 0:
            # If no Constants exist, generate a new one
            name = f"x_{self.constant_idx}"
            self.constant_idx += 1
            self.sequent[established_constants].append(name)

        # Add Quantor to list of processed quantors
        if quantor not in self.sequent[processed_quantor_expressions]:
            self.sequent[processed_quantor_expressions][quantor] = []

        # Stash existing mapping in case already existing in outer scope
        stashed_const = None
        if quantor.variable.name in self.sequent[variable_constant_mapping]:
            stashed_const = self.sequent[variable_constant_mapping][quantor.variable.name]

        # Copy established constants in case changed inside loop
        established_constants_copy = copy.deepcopy(self.sequent[established_constants])
        # Remove already processed constants from list
        for const in self.sequent[processed_quantor_expressions][quantor]:
            if const in established_constants_copy:
                established_constants_copy.remove(const)
        # Copy expression in quantor scope with all possible mappings
        for const in established_constants_copy:
            self.sequent[variable_constant_mapping][quantor.variable.name] = const
            expr_copy = copy.deepcopy(quantor.expr)
            self.variable_constant_mapper.map_expr(expr_copy)
            self.sequent[false_exprs if self.visiting_false else true_exprs].append(expr_copy)

        # Add constants to list of already processed constants
        self.sequent[processed_quantor_expressions][quantor].extend(established_constants_copy)

        # Restore stashed mapping
        if stashed_const is not None:
            self.sequent[variable_constant_mapping][quantor.variable.name] = stashed_const
        else:
            del self.sequent[variable_constant_mapping][quantor.variable.name]

    def generate_new_constant_expression(self, quantor: Quantor):
        # Create new constant
        name = f"x_{self.constant_idx}"
        self.constant_idx += 1
        self.sequent[established_constants].append(name)

        # Stash existing mapping in case already existing in outer scope
        stashed_const = None
        if quantor.variable.name in self.sequent[variable_constant_mapping]:
            stashed_const = self.sequent[variable_constant_mapping][quantor.variable.name]

        # Visit expression in quantor scope with the mapping
        self.sequent[variable_constant_mapping][quantor.variable.name] = name
        expr_copy = copy.deepcopy(quantor.expr)
        self.variable_constant_mapper.map_expr(expr_copy)
        self.sequent[false_exprs if self.visiting_false else true_exprs].append(expr_copy)

        # Restore stashed mapping
        if stashed_const is not None:
            self.sequent[variable_constant_mapping][quantor.variable.name] = stashed_const
        else:
            del self.sequent[variable_constant_mapping][quantor.variable.name]

    def visited_ExistentialQuantor(self, quantor: ExistentialQuantor):
        if self.visiting_false:
            self.generate_existing_constant_expression(quantor)
        else:
            self.generate_new_constant_expression(quantor)

    def visited_AllQuantor(self, quantor: AllQuantor):
        if self.visiting_false:
            self.generate_new_constant_expression(quantor)
        else:
            self.generate_existing_constant_expression(quantor)

    def visited_Predicate(self, predicate: Predicate):
        self.sequent[false_atoms if self.visiting_false else true_atoms].append(predicate)
