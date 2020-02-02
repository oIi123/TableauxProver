from src.Model.PropositionalExpressionTree import Atom
from src.Parser.FoplParser import FoplParser
from src.Parser.PropParser import PropParser
from src.TableauxBuilder.FoplTableauxBuilder import FoplTableauxBuilder
from src.TableauxBuilder.IpcTableauxBuilder import IpcTableauxBuilder
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from PySide2.QtWidgets import QApplication

from src.view.MainWindow import MainWindow

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
