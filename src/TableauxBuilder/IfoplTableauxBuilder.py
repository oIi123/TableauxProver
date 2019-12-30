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

    def visited_ExistentialQuantor(self, quantor: ExistentialQuantor):
        if self.visiting_certain_falsehood_exprs or self.visiting_false:
            processed_quantor_exprs = processed_certain_false_exquantor_exprs if self.visiting_certain_falsehood_exprs else processed_false_quantor_expressions
            self.generate_existing_constant_expression(quantor, processed_quantor_expressions=processed_quantor_exprs, append_to=false_exprs)
        else:
            self.generate_new_constant_expression(quantor)

    def visited_AllQuantor(self, quantor: AllQuantor):
        if self.visiting_certain_falsehood_exprs or self.visiting_false:
            self.generate_new_constant_expression(quantor)
            self.clear_false()

            if self.visiting_certain_falsehood_exprs:
                self.sequent[processed_certain_false_allquantor_exprs].append(quantor)
        else:
            self.generate_existing_constant_expression(quantor)
