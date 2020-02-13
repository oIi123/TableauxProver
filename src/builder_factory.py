from src.Parser.PropParser import PropParser
from src.Parser.FoplParser import FoplParser

from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder
from src.TableauxBuilder.IfoplTableauxBuilder import IfoplTableauxBuilder

class LogicType:
    PROPOSITIONAL = 1
    FOPL = 2
    IPROPOSITIONAL = 3
    IFOPL = 4


def create_parser(logic_type: int):
    if logic_type == LogicType.PROPOSITIONAL:
        return PropParser
    if logic_type == LogicType.FOPL:
        return FoplParser
    if logic_type == LogicType.IPROPOSITIONAL:
        return PropParser
    if logic_type == LogicType.IFOPL:
        return FoplParser


def create_tableau_builder(logic_type: int, left_exprs: list,
                          right_exprs: list, visit_idx:int=0,
                          cf: list=None, constants=[], functions=[]):
    if logic_type == LogicType.PROPOSITIONAL:
        tableau_builder = PropositionalTableauxBuilder(
            true_exprs=left_exprs,
            false_exprs=right_exprs,
            visit_idx=visit_idx,
        )
        return tableau_builder
    if logic_type == LogicType.FOPL:
        tableau_builder = FoplTableauxBuilder(
            true_exprs=left_exprs,
            false_exprs=right_exprs,
            constants=constants,
            functions=functions,
            visit_idx=visit_idx,
        )
        return tableau_builder
    if logic_type == LogicType.IPROPOSITIONAL:
        tableau_builder = IpcTableauxBuilder(
            true_exprs=left_exprs,
            false_exprs=right_exprs,
            visit_idx=visit_idx,
            cf_exprs=cf if cf is not None else [],
        )
        return tableau_builder
    if logic_type == LogicType.IFOPL:
        tableau_builder = IfoplTableauxBuilder(
            true_exprs=left_exprs,
            false_exprs=right_exprs,
            constants = constants,
            functions=functions,
            visit_idx=visit_idx,
            cf_exprs=cf if cf is not None else [],
        )
        return tableau_builder
