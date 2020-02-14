from src.Model.FoplExpressionTree import *
from src.TableauxBuilder.BaseTableauxBuilder import *
from src.TableauxBuilder.VariableConsantMapper import VariableConstantMapper



def to_base(s, b, BS):
    res = []
    while s:
        res.append(BS[s%b])
        s//= b
    return res[::-1] or []


def permute_array(length, array):
    perms = []
    idx = 0
    while True:
        perm = to_base(idx, len(array), array)
        idx += 1
        diff = length - len(perm)
        if diff < 0:
            return perms
        if diff > 0:
            x = [array[0]] * diff
            perm = x + perm
        perms.append(perm)


class FoplTableauxBuilder(BaseTableauxBuilder):
    function_depth = 0

    def __init__(self, tree: FoplExpressionTree = None, sequent: dict = None, **kwargs):
        super().__init__(tree=tree, sequent=sequent, **kwargs)

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
            self.process_multiprocess_exprs()

    def establish_new_constant(self):
        name = f"X_{self.constant_idx}"
        self.constant_idx += 1
        self.sequent[established_constants].append(name)

        return name

    def calculate_functions(self, depth=0):
        perms = []
        constants = self.sequent[established_constants][:]
        constants = [Const(x) for x in constants]
        if depth < self.function_depth:
            perms = self.calc_fun(depth+1)
        
        for name, arity in self.sequent[established_functions]:
            f_perms = permute_array(arity, perms + constants)
            for f_perm in f_perms:
                fun = Func(name, f_perm)
                perms.append(fun)
        
        return perms

    def process_multiprocess_exprs(self):
        """
        Processes the quantor with the most unprocessed constants
        :return:
        """
        num_of_constants = len(self.sequent[established_constants])
        num_of_constants += len(self.calculate_functions())

        # Tuple (Unprocessed_Constants, False_Side, Quantor)
        options = [(num_of_constants - len(v), False, k) for k, v in self.sequent[processed_true_quantor_expressions].items() if len(v) != num_of_constants]
        options.extend([(num_of_constants - len(v), True, k) for k, v in self.sequent[processed_false_quantor_expressions].items() if len(v) != num_of_constants])
        options.sort(key=lambda tpl: tpl[0], reverse=True)

        if len(options) > 0:
            self.visiting_false = options[0][1]
            self.generate_existing_constant_expression(options[0][2])
        else:
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

        # if functions and multiprocess quantors exist, no calculation end
        if len(self.sequent[processed_true_quantor_expressions]) != 0 or len(self.sequent[processed_false_quantor_expressions]) != 0:
            for _, arity in self.sequent[established_functions]:
                if arity > 0:
                    self.function_depth += 1
                    return False

        return True

    def generate_existing_constant_expression(self, quantor: Quantor, processed_quantor_expressions: str = None, append_to: str = None):
        if processed_quantor_expressions is None:
            processed_quantor_expressions = processed_false_quantor_expressions if self.visiting_false else processed_true_quantor_expressions
        if append_to is None:
            append_to = false_exprs if self.visiting_false else true_exprs

        if len(self.sequent[established_constants]) == 0:
            # If no Constants exist, generate a new one
            self.establish_new_constant()

        # Add Quantor to list of processed quantors
        if quantor not in self.sequent[processed_quantor_expressions]:
            self.sequent[processed_quantor_expressions][quantor] = []

        # Stash existing mapping in case already existing in outer scope
        stashed_const = None
        if quantor.variable.name in self.sequent[variable_constant_mapping]:
            stashed_const = self.sequent[variable_constant_mapping][quantor.variable.name]

        functions = copy.deepcopy(self.calculate_functions())
        function_strs = [str(fun) for fun in functions]

        # Copy established constants in case changed inside loop
        established_constants_copy = copy.deepcopy(self.sequent[established_constants])
        # Remove already processed constants from list
        for const in self.sequent[processed_quantor_expressions][quantor]:
            if const in established_constants_copy:
                established_constants_copy.remove(const)
            
            if const in function_strs:
                del functions[function_strs.index(const)]
                function_strs = [str(fun) for fun in functions]

        # Copy expression in quantor scope with all possible mappings
        for const in established_constants_copy + functions:
            self.sequent[variable_constant_mapping][quantor.variable.name] = const
            expr_copy = copy.deepcopy(quantor.expr)
            self.variable_constant_mapper.map_expr(expr_copy)
            self.add_to(append_to, expr_copy)

        # Add constants to list of already processed constants
        self.sequent[processed_quantor_expressions][quantor].extend(established_constants_copy)
        self.sequent[processed_quantor_expressions][quantor].extend(function_strs)

        # Restore stashed mapping
        if stashed_const is not None:
            self.sequent[variable_constant_mapping][quantor.variable.name] = stashed_const
        else:
            del self.sequent[variable_constant_mapping][quantor.variable.name]

    def generate_new_constant_expression(self, quantor: Quantor):
        # Create new constant
        name = self.establish_new_constant()

        # Stash existing mapping in case already existing in outer scope
        stashed_const = None
        if quantor.variable.name in self.sequent[variable_constant_mapping]:
            stashed_const = self.sequent[variable_constant_mapping][quantor.variable.name]

        # Visit expression in quantor scope with the mapping
        self.sequent[variable_constant_mapping][quantor.variable.name] = name
        expr_copy = copy.deepcopy(quantor.expr)
        self.variable_constant_mapper.map_expr(expr_copy)
        self.add_to(false_exprs if self.visiting_false else true_exprs, expr_copy)

        # Restore stashed mapping
        if stashed_const is not None:
            self.sequent[variable_constant_mapping][quantor.variable.name] = stashed_const
        else:
            del self.sequent[variable_constant_mapping][quantor.variable.name]

    def visited_ExistentialQuantor(self, quantor: ExistentialQuantor):
        if self.visiting_false:
            self.last_multiprocess_false = quantor
            self.generate_existing_constant_expression(quantor)
        else:
            self.generate_new_constant_expression(quantor)

    def visited_AllQuantor(self, quantor: AllQuantor):
        if self.visiting_false:
            self.generate_new_constant_expression(quantor)
        else:
            self.last_multiprocess_true = quantor
            self.generate_existing_constant_expression(quantor)

    def visited_Predicate(self, predicate: Predicate):
        self.add_to(false_atoms if self.visiting_false else true_atoms, predicate)

    def get_unprocessed_exprs(self, partially_in_trees=False):
        t, f, cf = super().get_unprocessed_exprs(partially_in_trees)

        # if partially_in_trees, filter for multiprocess exprs
        if partially_in_trees and len(self.children) > 0:
            t = [expr for expr in t if type(expr) is not AllQuantor]
            f = [expr for expr in f if type(expr) is not ExistentialQuantor]
            return t, f, cf
        return t, f, cf

    def get_partially_processed_exprs(self, partially_in_trees=False):
        if partially_in_trees:
            return self.get_partially_in_trees()

        if self.parent is None:
            return (
                list(self.sequent[processed_true_quantor_expressions]),
                list(self.sequent[processed_false_quantor_expressions]),
                list(self.sequent[processed_certain_false_allquantor_exprs]) + 
                list(self.sequent[processed_certain_false_exquantor_exprs]))
        true_exprs = [x for x in self.sequent[processed_true_quantor_expressions]
                      if x not in self.parent.sequent[processed_true_quantor_expressions]]

        false_exprs = [x for x in self.sequent[processed_false_quantor_expressions]
                       if x not in self.parent.sequent[processed_false_quantor_expressions]]

        cf_exprs = [x for x in self.sequent[processed_certain_false_allquantor_exprs]
                    if x not in self.parent.sequent[processed_certain_false_allquantor_exprs]]
        cf_exprs += [x for x in self.sequent[processed_certain_false_exquantor_exprs]
                    if x not in self.parent.sequent[processed_certain_false_exquantor_exprs]]

        return (true_exprs, false_exprs, [])

    def get_partially_in_trees(self):
        p_t, p_f, p_cf = [], [], []
        if len(self.children) > 0:
            return (p_t, p_f, p_cf)

        return (
            list(self.sequent[processed_true_quantor_expressions]),
            list(self.sequent[processed_false_quantor_expressions]),
            list(self.sequent[processed_certain_false_allquantor_exprs]) + 
            list(self.sequent[processed_certain_false_exquantor_exprs]))
