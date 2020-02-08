from src.Model.FoplExpressionTree import *
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
from src.TableauxBuilder.IpcTableauxBuilder import *
from src.TableauxBuilder.VariableConsantMapper import VariableConstantMapper


# TODO: implement process_multiprocess_exprs -> should call IpcTableauxBuilder first,
#  after that it should reprocess the quantor expressions
class IfoplTableauxBuilder(IpcTableauxBuilder, FoplTableauxBuilder):
    def check_unprocessed_quantor_expressions(self):
        """
        Checks if there are any quantors with unprocessed constants
        Looks up the same check in superclass, after that checks certain_false sets
        :return: Returns true if all quantors processed all constants
        """
        if super().check_unprocessed_quantor_expressions():
            num_of_constants = len(self.sequent[established_constants])
            for processed_constants in self.sequent[processed_certain_false_exquantor_exprs].values():
                if len(processed_constants) != num_of_constants:
                    return False

            for processed_constants in self.sequent[processed_certain_false_allquantor_exprs].values():
                if len(processed_constants) != num_of_constants:
                    return False

            return True
        return False

    def process_multiprocess_exprs(self) -> bool:
        """
        Processes the quantor with the most unprocessed constants or the implication that has been reprocessed
        the least
        """
        options = [(expr.priority(False), expr) for expr in self.sequent[certain_falsehood_exprs]]
        options.sort(key=lambda tpl: tpl[0])

        if len(options) > 0:
            self.visiting_certain_falsehood_exprs = True
            expr = options[0][1]
            self.visit_expr(True, expr)
        else:
            # If all certain falsehood expressions are processed, reprocess the quantor expressions or implications
            num_of_constants = len(self.sequent[established_constants])
            # Tuple: (expression, priority, false_side_or_certain_false)
            #   priority is either the number of unprocessed constants or
            #   reprocess_idx_true_impl - max(number_unprocessed_contants)
            expr_list = [(k, num_of_constants - len(v), 0) for k, v in self.sequent[processed_true_quantor_expressions].items() if len(v) != num_of_constants]
            expr_list.extend([(k, num_of_constants - len(v), 1) for k, v in self.sequent[processed_false_quantor_expressions].items() if len(v) != num_of_constants])
            expr_list.extend([(k, num_of_constants - len(v), 2) for k, v in self.sequent[processed_certain_false_exquantor_exprs].items() if len(v) != num_of_constants])

            max_number_unprocessed_constants = max(expr_list, key=lambda tpl: tpl[1], default=0)
            repr_exprs_list = [(k, v - max_number_unprocessed_constants, 0) for k, v in self.sequent[processed_true_impls].items()]
            repr_exprs_list.extend([(k, v - max_number_unprocessed_constants, 2) for k, v in self.sequent[processed_certain_false_allquantor_exprs].items()])

            expr_list.sort(key=lambda tpl: tpl[0], reverse=True)
            repr_exprs_list.sort(key=lambda tpl: tpl[0], reverse=True)

            if len(expr_list) == len(repr_exprs_list) == 0:
                raise Exception("There are no expressions to reprocess")
            else:
                if len(expr_list) == 0:
                    expr_list = [(None, -1, 0)]
                if len(repr_exprs_list) == 0:
                    repr_exprs_list = [(None, -1, 0)]

                if expr_list[0][1] > repr_exprs_list[0][1]:
                    # Reprocess quantor expression
                    self.visiting_certain_falsehood_exprs = expr_list[0][2] == 2
                    self.visiting_false = expr_list[0][2]
                    self.generate_existing_constant_expression(expr_list[0][0])
                else:
                    # Reprocess true implication or certain falsehood allquantor
                    if repr_exprs_list[0][2] == 2:
                        self.visiting_false = True
                        self.generate_new_constant_expression(repr_exprs_list[0][0])
                    else:
                        self.visiting_false = False
                        repr_exprs_list[0][0].visit(self)

                    self.sequent[processed_certain_false_allquantor_exprs if self.visiting_false else processed_true_impls][repr_exprs_list[0][0]] += 1

    def visited_ExistentialQuantor(self, quantor: ExistentialQuantor):
        if self.visiting_certain_falsehood_exprs or self.visiting_false:
            processed_quantor_exprs = processed_certain_false_exquantor_exprs if self.visiting_certain_falsehood_exprs else processed_false_quantor_expressions
            self.generate_existing_constant_expression(quantor, processed_quantor_expressions=processed_quantor_exprs, append_to=false_exprs)
        else:
            self.generate_new_constant_expression(quantor)

    def visited_AllQuantor(self, quantor: AllQuantor):
        if self.visiting_certain_falsehood_exprs or self.visiting_false:
            child = self.create_copy(clears_false_exprs=True)
            child.visiting_false = True
            child.visiting_certain_falsehood_exprs = self.visiting_certain_falsehood_exprs
            child.generate_new_constant_expression(quantor)
            self.children.append(child)

            if child.visiting_certain_falsehood_exprs and quantor not in child.sequent[processed_certain_false_allquantor_exprs]:
                child.sequent[processed_certain_false_allquantor_exprs][quantor] = []
        else:
            self.generate_existing_constant_expression(quantor)

    def visited_Predicate(self, predicate: Predicate):
        if self.visiting_certain_falsehood_exprs:
            self.add_to(certain_falsehood_atoms, predicate)
        else:
            super().visited_Predicate(predicate)

    def get_partially_processed_exprs(self):
        t_1, f_1, cf_1 = IpcTableauxBuilder.get_partially_processed_exprs(self)
        t_2, f_2, cf_2 = FoplTableauxBuilder.get_partially_processed_exprs(self)

        return (t_1 + t_2, f_1 + f_2, cf_1 + cf_2)
