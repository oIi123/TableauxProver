from src.Model.PropositionalExpressionTree import Atom
from src.Parser.FoplParser import FoplParser
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder

if __name__ == '__main__':
    parser = PropParser("((A->B)->A)->A")
    # parser = FoplParser("")
    tree = parser.parse()

    #tableaux = PropositionalTableauxBuilder(expr=tree.expr)
    #tableaux = FoplTableauxBuilder(tree=tree)
    tableaux = IpcTableauxBuilder(expr=tree.expr)
    tableaux.auto_resolve(True)
    print(tableaux.is_closed())
    print(tree.expr)
