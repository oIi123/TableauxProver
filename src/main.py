from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFontDatabase
from src.view.MainWindow import MainWindow
import sys
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)

    font_path = f'{os.getcwd()}/YuGothB.ttc'
    QFontDatabase.addApplicationFont('YuGothB.ttc')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
