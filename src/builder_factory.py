from src.Parser.PropParser import PropParser
from src.Parser.FoplParser import FoplParser

from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder


class LogicType:
    Propositional = 1
    FOPL = 2
    IPropositional = 3
    IFOPL = 4


def create_parser(logic_type: int):
    if logic_type == LogicType.Propositional:
        return PropParser
    if logic_type == LogicType.FOPL:
        return FoplParser


def concat_list_of_lists(list_of_lists):
    concat = list()
    for lst in list_of_lists:
        concat += lst
    return concat


def create_tableau_builder(logic_type: int, left_exprs: list, right_exprs: list, visit_idx:int=0):
    if logic_type == LogicType.Propositional:
        tableau_builder = PropositionalTableauxBuilder(
            true_exprs=[tree.expr for tree in left_exprs],
            false_exprs=[tree.expr for tree in right_exprs],
            visit_idx=visit_idx,
        )
        return tableau_builder
    if logic_type == LogicType.FOPL:
        constants = concat_list_of_lists([k.constants for k in left_exprs + right_exprs])
        tableau_builder = FoplTableauxBuilder(
            true_exprs=[tree.expr for tree in left_exprs],
            false_exprs=[tree.expr for tree in right_exprs],
            constants=constants,
            visit_idx=visit_idx
        )
        return tableau_builder
