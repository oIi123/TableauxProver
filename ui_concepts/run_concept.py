import sys
from typing import Union, Optional

import PySide2
from PySide2.QtGui import QPainter, QPaintEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtCore import QFile
from ui_mainwindow import Ui_MainWindow


def get_child_widget(parent: QWidget, name: str) -> Union[Optional[QWidget], None]:
    for child in parent.children():
        if child.objectName() == name:
            return child
        sub_child = get_child_widget(child, name)
        if sub_child is not None:
            return sub_child

    return None


class Main(QMainWindow):
    resize_height = 0
    resize_width = 0

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scroll_area_content = get_child_widget(self, "scrollAreaWidgetContents")
        self.scroll_area_content.installEventFilter(self)

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent):
        if watched is self.scroll_area_content and type(event) is QPaintEvent:
            normal_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
            underlined_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
            underlined_font.setUnderline(True)

            p = QPainter()
            p.begin(self.scroll_area_content)
            p.setPen(PySide2.QtGui.QColor(0, 0, 0))
            p.setFont(normal_font)

            p.drawLine(250, 75, 500, 75)
            p.drawLine(375, 25, 375, 250)
            p.drawLine(200, 250, 550, 250)
            p.drawLine(200, 250, 200, 400)
            p.drawLine(550, 250, 550, 500)

            p.drawLine(175, 400, 225, 400)
            p.drawEllipse(545, 500, 10, 10)

            p.drawText(312, 50, "T")
            p.drawText(437, 50, "F")

            p.drawText(400, 170, "A")
            p.drawText(150, 350, "A")
            p.drawText(575, 350, "B")
            p.drawText(500, 450, "C")

            p.setFont(underlined_font)
            p.drawText(400, 120, "A|!A&(B|!C)")
            p.drawText(400, 220, "!A&(B|!C)")
            p.drawText(225, 300, "!A")
            p.drawText(575, 300, "B|!C")
            p.drawText(575, 400, "!C")

            p.end()

            self.scroll_area_content.setMinimumSize(700, 550)

        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec_())
