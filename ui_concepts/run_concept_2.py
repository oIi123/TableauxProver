import sys
from typing import Union, Optional

import PySide2
from PySide2.QtGui import QPainter, QPaintEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit
from PySide2.QtCore import QFile
from ui_mainwindow import Ui_MainWindow
from ui_input_window import Ui_MainWindow as Ui_InputWindow


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

        btn = QPushButton(parent=self.scroll_area_content)
        btn.setText("B&&!C")
        btn.setGeometry(575, 280, 45, 25)
        btn.show()

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
            p.drawLine(550, 250, 550, 350)

            p.drawLine(175, 400, 225, 400)

            p.drawText(312, 50, "T")
            p.drawText(437, 50, "F")

            p.drawText(400, 170, "A")
            p.drawText(150, 350, "A")

            p.setFont(underlined_font)
            p.drawText(400, 120, "A|!A&(B|!C)")
            p.drawText(400, 220, "!A&(B|!C)")
            p.drawText(225, 300, "!A")

            p.end()

            self.scroll_area_content.setMinimumSize(700, 550)

        return False


class Input(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InputWindow()
        self.ui.setupUi(self)

        self.scroll_area_single_content = get_child_widget(self, "scrollAreaWidgetContentsSingle")
        self.scroll_area_single_content.installEventFilter(self)
        self.scroll_area_branch_content = get_child_widget(self, "scrollAreaWidgetContentsBranch")
        self.scroll_area_branch_content.installEventFilter(self)

        geoms = [
            (425, 140, 150, 130),
            (225, 140, 150, 130),
        ]
        for geom in geoms:
            text_input = QTextEdit(parent=self.scroll_area_single_content)
            text_input.setGeometry(*geom)
            text_input.show()

        geoms = [
            (225, 165, 150, 130),
            (25, 165, 150, 130),
            (425, 165, 150, 130),
            (625, 165, 150, 130),
        ]
        for geom in geoms:
            text_input = QTextEdit(parent=self.scroll_area_branch_content)
            text_input.setGeometry(*geom)
            text_input.show()

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent):
        if type(event) is not QPaintEvent:
            return False

        if watched is self.scroll_area_single_content:
            self.draw_tableau_boilerplate(self.scroll_area_single_content, self.draw_single_tableau)
        elif watched is self.scroll_area_branch_content:
            self.draw_tableau_boilerplate(self.scroll_area_branch_content, self.draw_branch_tableau)

        return False

    def draw_single_tableau(self, painter: QPainter):
        painter.drawLine(400, 140, 400, 270)

    def draw_branch_tableau(self, painter: QPainter):
        painter.drawLine(200, 140, 600, 140)
        painter.drawLine(200, 140, 200, 295)
        painter.drawLine(600, 140, 600, 295)

    def draw_tableau_boilerplate(self, scroll_area_content, draw_tableau_content):
        normal_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
        underlined_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
        underlined_font.setUnderline(True)

        p = QPainter()
        p.begin(scroll_area_content)
        p.setPen(PySide2.QtGui.QColor(0, 0, 0))
        p.setFont(normal_font)

        p.drawLine(275, 75, 525, 75)
        p.drawLine(400, 25, 400, 140)

        p.drawText(337, 50, "T")
        p.drawText(462, 50, "F")

        p.setFont(underlined_font)
        p.drawText(425, 120, "B&!C")

        draw_tableau_content(p)

        p.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    input_window = Input()
    input_window.show()

    sys.exit(app.exec_())
