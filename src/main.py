from src.Parser.FoplParser import FoplParser
from src.Parser.PropParser import PropParser

if __name__ == '__main__':
    #parser = PropParser("A&B->!C")
    parser = FoplParser("@a,b (P(a)&K(b)->(P(a)|P(b))&P(c))")
    tree = parser.parse()
    print(tree.expr)
