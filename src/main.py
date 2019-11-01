from src.Parser.FoplParser import FoplParser
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder

if __name__ == '__main__':
    parser = PropParser("A&B->A|B")
    # parser = FoplParser("(A)a,b (P(a)&K(b)->(P(a)|P(b))&P(c))")
    tree = parser.parse()

    tableaux = PropositionalTableauxBuilder(expr=tree.expr)
    print(tableaux)
    while not tableaux.is_done():
        tableaux.visit()
        print(tableaux)
