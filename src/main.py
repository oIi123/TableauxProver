from src.Parser.FoplParser import FoplParser
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder

if __name__ == '__main__':
    # parser = PropParser("A&B->A|B")
    parser = FoplParser("((A)x (A(x)->B(x))) -> ((A)x A(x) -> (A)x B(x))")
    tree = parser.parse()

    #tableaux = PropositionalTableauxBuilder(expr=tree.expr)
    tableaux = FoplTableauxBuilder(tree=tree)
    tableaux.print()
    while not tableaux.is_done():
        print("\n")
        tableaux.visit()
        tableaux.print()
