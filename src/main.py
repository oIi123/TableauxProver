from src.Parser.PropParser import PropParser

if __name__ == '__main__':
    parser = PropParser("A&B->!C")
    tree = parser.parse()
    print("done")
