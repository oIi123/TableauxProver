import sys

from typing import Union, Optional

import PySide2
from PySide2.QtGui import QPainter, QPaintEvent, QFontMetrics
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit
from PySide2.QtCore import QFile, Qt
from antlr4 import RecognitionException
from src.view.ui_mainwindow import Ui_MainWindow

from src.Parser.PropParser import PropParser
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from src.TableauxBuilder.BaseTableauxBuilder import BaseTableauxBuilder
from src.builder_factory import *
from src.view import HelpWindow


def get_child_widget(parent: QWidget, name: str) -> Union[Optional[QWidget], None]:
    for child in parent.children():
        if child.objectName() == name:
            return child
        sub_child = get_child_widget(child, name)
        if sub_child is not None:
            return sub_child

    return None


def curry(function, arg):
    def curried(*args, **kwargs):
        return function(arg, *args, **kwargs)

    return curried


class ResolveMode:
    Automatic = 1
    Manual = 2


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

    def get_text_width(self, text):
        """
        Returns painted width of the text
        """
        fm = QFontMetrics(self.font())
        return fm.horizontalAdvance(text)

    def draw_dotted_underlined(self, painter: QPainter, text: str, x: int, y: int):
        """
        QFont has no dotted underlined style
        this function draws the text and a dotted line under the text
        """
        painter.drawText(x, y, text)

        txt_width = self.get_text_width(text)
        pen = painter.pen()
        pen.setStyle(Qt.DashDotLine)
        painter.setPen(pen)

        # draw the dotted line with offset of 1 for better visibility
        painter.drawLine(x, y + 1, x + txt_width, y + 1)

        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)

    def draw_underlined(self, painter: QPainter, text: str, x: int, y: int):
        """
        Draw a text with underlined font
        """
        painter.setFont(self.underlined_font)
        painter.drawText(x, y, text)
        painter.setFont(self.normal_font)

    def draw_normal(self, painter: QPainter, text: str, x: int, y: int):
        """
        Draws a text with normal font
        """
        painter.drawText(x, y, text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mode = ResolveMode.Automatic
        self.logic_type = LogicType.Propositional

        # setup slots
        self.ui.pl_radio_btn.toggled.connect(self.logic_changed)
        self.ui.fopl_radio_btn.toggled.connect(self.logic_changed)
        self.ui.ipl_radio_btn.toggled.connect(self.logic_changed)
        self.ui.ifopl_radio_btn.toggled.connect(self.logic_changed)

        self.ui.automatic_radio_btn.toggled.connect(self.mode_changed)
        self.ui.manual_radio_btn.toggled.connect(self.mode_changed)

        self.ui.start_calc_btn.clicked.connect(self.calculate_pressed)
        self.ui.help_button.clicked.connect(HelpWindow.show_help)
        self.ui.reset_btn.clicked.connect(self.reset)

        # subscribe to draw events
        self.scroll_area_content = get_child_widget(self, "scrollAreaWidgetContents")
        self.scroll_area_content.installEventFilter(self)

        self.row_height = 50
        self.margin = 10
        self.d_margin = 2 * self.margin

        # size of the scroll area content
        self.max_width = 700
        self.max_height = 400

        self.error_widget = None
        self.tableaux_builder: BaseTableauxBuilder = None

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent):
        if watched is self.scroll_area_content and type(event) is QPaintEvent:
            p = CustomPainter()
            p.begin(self.scroll_area_content)

            if self.tableaux_builder is None:
                # no expression entered yet
                self.draw_initial(p)
                p.end()
                return False

            # calculate horizontal center
            width_l, width_r = self.tableaux_builder.get_drawn_width(p.get_text_width, self.d_margin)
            x = width_l + self.d_margin
            x = max(x, self.d_margin + 125)  # ensure space to border

            p.drawLine(x - 125, 75, x + 125, 75)
            p.drawLine(x, 25, x, 125)
            p.drawText(x - 65, 50, self.tableaux_builder.left_side_sign)
            p.drawText(x + 62, 50, self.tableaux_builder.right_side_sign)

            self.draw_path(p, self.tableaux_builder, x=x)

            p.end()

            self.scroll_area_content.setMinimumSize(self.max_width + self.d_margin,
                                                    self.max_height + self.d_margin)

        return False

    def get_y(self, layer):
        """
        Returns the vertical position of the given layer
        """
        return 125 + self.row_height * layer

    def to_pos_list(self, exprs, x, txt_width_fun, draw_fun, include_atoms=False):
        """
        Converts a list of expressions to a list of tuples
        Tuples are added if include_atoms is True or the expr is not a atom
        (x-pos, expression, draw_function)
        """
        lst = [(
                    x - self.margin - txt_width_fun(str(expr)),
                    expr,
                    draw_fun
                )
               for expr in exprs[0] if not expr.is_atom or include_atoms]
        lst.extend([(
                        x + self.margin,
                        expr,
                        draw_fun
                    )
                    for expr in exprs[1] if not expr.is_atom or include_atoms])

        return lst

    def draw_path(
                    self, p: CustomPainter,
                    tableau: BaseTableauxBuilder,
                    layer=0, x=375,
                    parent_processed: (list, list)=None):
        """
        Draws all expressions in the tableau
        """
        closed = tableau.is_closed()

        parent_processed = ([], []) if parent_processed is None else parent_processed
        processed_exprs = tableau.get_processed_exprs()
        l = [x for x in processed_exprs[0] if x not in parent_processed[0]]
        r = [x for x in processed_exprs[1] if x not in parent_processed[1]]
        processed_exprs = (l, r)

        # a close tableau does not need to draw unprocessed exprs
        unprocessed_exprs = ([], []) if closed else tableau.get_unprocessed_exprs()
        atom_exprs = tableau.get_atom_exprs()
        partially_exprs = tableau.get_partially_processed_exprs()

        # calculate horizontal positions of expressions
        expr_pos = self.to_pos_list(processed_exprs, x, p.get_text_width, p.draw_underlined)
        expr_pos.extend(self.to_pos_list(partially_exprs, x, p.get_text_width, p.draw_dotted_underlined))
        expr_pos.extend(self.to_pos_list(unprocessed_exprs, x, p.get_text_width, p.draw_normal))
        expr_pos.extend(self.to_pos_list(atom_exprs, x, p.get_text_width, p.draw_normal, include_atoms=True))
        # sort by processing order
        expr_pos.sort(key=lambda x: x[1].visit_idx)

        # unvisited expressions have idx = -1
        # put those at the end of the list
        unvisited_exprs = [x for x in expr_pos if x[1].visit_idx == -1]
        expr_pos = expr_pos[len(unvisited_exprs):]
        expr_pos.extend(unvisited_exprs)

        # draw expressions
        for pos_x, expr, draw_fun in expr_pos:
            y_1 = self.get_y(layer)
            y_2 = self.get_y(layer+1)
            draw_fun(p, str(expr), pos_x, y_1)
            p.drawLine(x, y_1, x, y_2)
            layer += 1

            # update max width/height
            txt_width = p.get_text_width(str(expr))
            self.max_width = max(self.max_width,
                                 pos_x + txt_width)
            self.max_height = max(self.max_height, y_2)

        if len(tableau.children) == 0:
            # draw end sign of the branch
            done = tableau.is_done()

            if closed:
                width = 10
                y = self.get_y(layer)
                p.drawLine(x - width, y, x + width, y)

            if done and not closed:
                diameter = 10
                p.drawEllipse(x - diameter / 2, self.get_y(layer),
                              diameter, diameter)
            return

        parent_processed = (parent_processed[0] + processed_exprs[0],
                            parent_processed[1] + processed_exprs[1])

        # draw left branch
        y = self.get_y(layer)
        left = tableau.children[0]
        width_l, width_r = left.get_drawn_width(p.get_text_width,
                                                self.d_margin)
        new_x = x - width_r - self.d_margin
        p.drawLine(x, y, new_x, y)
        p.drawLine(new_x, y, new_x, self.get_y(layer+1))
        self.draw_path(p, left, layer+1, new_x, parent_processed)

        # draw right branch
        right = tableau.children[1]
        width_l, width_r = right.get_drawn_width(p.get_text_width,
                                                 self.d_margin)
        new_x = x + width_l + self.d_margin
        p.drawLine(x, y, new_x, y)
        p.drawLine(new_x, y, new_x, self.get_y(layer+1))
        self.draw_path(p, right, layer+1, new_x, parent_processed)

    def logic_changed(self):
        """
        This function is called when a logic radio button is toggled
        """
        if self.ui.pl_radio_btn.isChecked():
            self.logic_type = LogicType.Propositional
        if self.ui.fopl_radio_btn.isChecked():
            self.logic_type = LogicType.FOPL
        if self.ui.ipl_radio_btn.isChecked():
            self.logic_type = LogicType.IPropositional
        if self.ui.ifopl_radio_btn.isChecked():
            self.logic_type = LogicType.IFOPL
        self.scroll_area_content.repaint()

    def mode_changed(self):
        """
        This function is called when a mode button is toggled
        """
        if self.ui.automatic_radio_btn.isChecked():
            self.mode = ResolveMode.Automatic
        if self.ui.manual_radio_btn.isChecked():
            self.mode = ResolveMode.Manual

    def draw_initial(self, painter: CustomPainter):
        """
        Draws the initial tableau frame and lays out the text edits/button
        """
        classic = self.logic_type in [LogicType.Propositional, LogicType.FOPL]
        left_side_sign = 'T' if classic else 'P'
        right_side_sign = 'F' if classic else 'C'

        painter.drawLine(250, 75, 500, 75)
        painter.drawLine(375, 25, 375, 300)
        painter.drawText(310, 50, left_side_sign)
        painter.drawText(443, 50, right_side_sign)

    def calculate_pressed(self):
        """
        This function is called after the calculate button is pressed
        """
        parser = create_parser(self.logic_type)
        left_exprs = list()
        right_exprs = list()

        # get the entered expressions
        left_entered_text = self.ui.inital_left_exprs_text_edit.toPlainText()
        right_entered_text = self.ui.inital_right_exprs_text_edit.toPlainText()
        left_lines = [l.strip() for l in left_entered_text.split('\n') if l.strip() != '']
        right_lines = [r.strip() for r in right_entered_text.split('\n') if r.strip() != '']

        # parse the expressions
        parsed_line = None
        for nr, line in enumerate(left_lines):
            try:
                parsed_line = parser.parse(line)
            except RecognitionException as e:
                self.show_error(self.ui.inital_left_exprs_text_edit, str(e), nr+1)
                return
            left_exprs.append(parsed_line)
        for nr, line in enumerate(right_lines):
            try:
                parsed_line = parser.parse(line)
            except RecognitionException as e:
                self.show_error(self.ui.inital_right_exprs_text_edit, str(e), nr+1)
                return
            right_exprs.append(parsed_line)

        # create tableau builder with expressions
        self.tableaux_builder = create_tableau_builder(
            logic_type=self.logic_type,
            left_exprs=left_exprs,
            right_exprs=right_exprs,
            visit_idx=parser.parse_idx
        )

        # hide widgets to enter initial expressions
        self.ui.inital_left_exprs_text_edit.hide()
        self.ui.inital_right_exprs_text_edit.hide()
        self.ui.start_calc_btn.hide()
        self.ui.inital_left_exprs_text_edit.setStyleSheet('')
        self.ui.inital_right_exprs_text_edit.setStyleSheet('')
        if self.error_widget is not None:
            self.error_widget.hide()

        # if automatic, try to auto resolve the tableau
        if self.mode == ResolveMode.Automatic:
            self.tableaux_builder.auto_resolve()

        self.scroll_area_content.repaint()

    def show_error(self, view: QWidget, txt: str, line: int):
        view.setStyleSheet('border: 1px solid rgb(240, 60, 60);')

        self.error_widget = QTextEdit(parent=self.scroll_area_content)
        self.error_widget.setGeometry(25, 400, 732, 62)
        self.error_widget.setStyleSheet('background-color: rgb(240, 60, 60); border-radius: 10px;')

        txt = f'<b>Error in line {line}</b><p>{txt}</h1>'
        self.error_widget.setHtml(txt)
        self.error_widget.setReadOnly(True)

        self.error_widget.show()

    def reset(self):
        self.tableaux_builder = None
        self.ui.inital_left_exprs_text_edit.show()
        self.ui.inital_right_exprs_text_edit.show()
        self.ui.start_calc_btn.show()

        self.max_width = 700
        self.max_height = 400
        self.scroll_area_content.setMinimumSize(self.max_width + self.d_margin,
                                                    self.max_height + self.d_margin)

        self.scroll_area_content.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
