from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFontDatabase
from src.view.MainWindow import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont('res/YuGothicUI Semibold.ttf')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
