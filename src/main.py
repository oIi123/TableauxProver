from src.Model.PropositionalExpressionTree import Atom
from src.Parser.FoplParser import FoplParser
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from PySide2.QtWidgets import QApplication

from ui_concepts.run_concept_2 import Main

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    # input_window = Input()
    # input_window.show()

    sys.exit(app.exec_())
