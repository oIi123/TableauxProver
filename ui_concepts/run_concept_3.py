import sys
from typing import Union, Optional

import PySide2
from PySide2.QtGui import QPainter, QPaintEvent, QPen
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit
from PySide2.QtCore import QFile
from ui_concepts.ui_mainwindow import Ui_MainWindow
from ui_concepts.ui_input_window import Ui_MainWindow as Ui_InputWindow


def get_child_widget(parent: QWidget, name: str) -> Union[Optional[QWidget], None]:
    for child in parent.children():
        if child.objectName() == name:
            return child
        sub_child = get_child_widget(child, name)
        if sub_child is not None:
            return sub_child

    return None


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scroll_area_content = get_child_widget(self, "scrollAreaWidgetContents")
        self.scroll_area_content.installEventFilter(self)

        # 550, 325, 550, 480
        geoms = [
            (375, 350, 150, 130),
            (575, 350, 150, 130),
        ]
        for geom in geoms:
            text_input = QTextEdit(parent=self.scroll_area_content)
            text_input.setGeometry(*geom)
            text_input.show()

        geoms = [
            (525, 480, 50, 50),
            (725, 300, 50, 50),
        ]
        for geom in geoms:
            btn = QPushButton(parent=self.scroll_area_content)
            btn.setGeometry(*geom)
            btn.setStyleSheet("QPushButton {qproperty-icon: url(add.svg); background-color: rgb(255,255,255,0); qproperty-iconSize: 24px;}")
            btn.show()

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent):
        if watched is self.scroll_area_content and type(event) is QPaintEvent:
            normal_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
            underlined_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
            underlined_font.setUnderline(True)

            normal_pen = QPen(PySide2.QtGui.QColor(0, 0, 0))
            dotted_pen = QPen(normal_pen)
            dotted_pen.setStyle(PySide2.QtCore.Qt.DashDotDotLine)

            p = QPainter()
            p.begin(self.scroll_area_content)
            p.setPen(normal_pen)
            p.setFont(normal_font)

            p.drawLine(250, 75, 500, 75)
            p.drawLine(375, 25, 375, 250)
            p.drawLine(200, 250, 550, 250)
            p.drawLine(200, 250, 200, 400)
            p.drawLine(550, 250, 550, 325)

            p.drawLine(175, 400, 225, 400)

            p.drawText(312, 50, "T")
            p.drawText(437, 50, "F")

            p.drawText(400, 170, "A")
            p.drawText(150, 350, "A")

            p.setFont(underlined_font)
            p.drawText(400, 120, "A|!A&(B|!C)")
            p.drawText(400, 220, "!A&(B|!C)")
            p.drawText(225, 300, "!A")
            p.drawText(575, 300, "B|!C")

            p.setPen(dotted_pen)
            p.drawLine(550, 325, 550, 480)
            p.drawLine(550, 325, 725, 325)

            p.end()

            self.scroll_area_content.setMinimumSize(800, 550)

        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec_())
