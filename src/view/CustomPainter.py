import PySide2

from PySide2.QtGui import QPainter, QFontMetrics
from src.builder_factory import LogicType


class CustomPainter(QPainter):
    def __init__(self):
        super().__init__()
        self.normal_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
        self.underlined_font = PySide2.QtGui.QFont('MS Shell Dlg 2', 14)
        self.underlined_font.setUnderline(True)

    def begin(self, widget):
        super().begin(widget)
        self.setFont(self.normal_font)
        self.setPen(PySide2.QtGui.QColor(0, 0, 0))

    def draw_tableau_header(self, logic_type, center_x=375, height=225):
        """
        Draws the initial tableau frame and lays out the text edits/button
        """
        classic = logic_type in [LogicType.PROPOSITIONAL, LogicType.FOPL]
        left_side_sign = 'T' if classic else 'P'
        right_side_sign = 'F' if classic else 'C'

        self.drawLine(center_x - 125, 75, center_x + 125, 75)
        self.drawLine(center_x, 25, center_x, 75 + height)
        self.drawText(center_x - 65, 50, left_side_sign)
        self.drawText(center_x + 68, 50, right_side_sign)

    def get_text_width(self, text):
        """
        Returns painted width of the text
        """
        fm = QFontMetrics(self.font())
        return fm.horizontalAdvance(text)

    def draw_dotted_underlined(self, text: str, x: int, y: int, **kwargs):
        """
        QFont has no dotted underlined style
        this function draws the text and a dotted line under the text
        """
        self.drawText(x, y, text)

        txt_width = self.get_text_width(text)
        pen = self.pen()
        pen.setStyle(Qt.DashDotLine)
        self.setPen(pen)

        # draw the dotted line with offset of 1 for better visibility
        self.drawLine(x, y + 1, x + txt_width, y + 1)

        pen.setStyle(Qt.SolidLine)
        self.setPen(pen)

    def draw_underlined(self, text: str, x: int, y: int, **kwargs):
        """
        Draw a text with underlined font
        """
        self.setFont(self.underlined_font)
        self.drawText(x, y, text)
        self.setFont(self.normal_font)

    def draw_normal(self, text: str, x: int, y: int, **kwargs):
        """
        Draws a text with normal font
        """
        self.drawText(x, y, text)