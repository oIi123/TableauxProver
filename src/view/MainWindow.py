import sys
from typing import Union, Optional

import PySide2
from PySide2.QtGui import QPainter, QPaintEvent, QFontMetrics
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit
from PySide2.QtCore import QFile, Qt
from src.view.ui_mainwindow import Ui_MainWindow

from src.Parser.PropParser import PropParser
from src.TableauxBuilder.PropositionalTableauxBuilder import PropositionalTableauxBuilder
from src.TableauxBuilder.BaseTableauxBuilder import BaseTableauxBuilder
from src.builder_factory import *
from src.view.BaseWindow import BaseWindow
from src.view.InputWindow import InputWindow
from src.view.CustomPainter import CustomPainter
from src.view.DrawingCalculator import DrawingCalculator


def get_child_widget(parent: QWidget, name: str) -> Union[Optional[QWidget], None]:
    for child in parent.children():
        if child.objectName() == name:
            return child
        sub_child = get_child_widget(child, name)
        if sub_child is not None:
            return sub_child

    return None


def curry(function, *c_args, **c_kwargs):
    def curried(*args, **kwargs):
        return function(*c_args, *args, **c_kwargs, **kwargs)

    return curried


class ResolveMode:
    Automatic = 1
    Manual = 2


class MainWindow(BaseWindow):
    input_window = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mode = ResolveMode.Automatic

        # create reset button in code to put it over scroll area
        self.reset_btn = QPushButton(self)
        self.reset_btn.setText('Reset')
        self.reset_btn.setGeometry(16, 118, 45, 28)
        self.reset_btn.show()

        # setup slots
        self.ui.pl_radio_btn.toggled.connect(self.logic_changed)
        self.ui.fopl_radio_btn.toggled.connect(self.logic_changed)
        self.ui.ipl_radio_btn.toggled.connect(self.logic_changed)
        self.ui.ifopl_radio_btn.toggled.connect(self.logic_changed)

        self.ui.automatic_radio_btn.toggled.connect(self.mode_changed)
        self.ui.manual_radio_btn.toggled.connect(self.mode_changed)

        self.ui.start_calc_btn.clicked.connect(self.calculate_pressed)
        self.ui.help_button.clicked.connect(self.show_help)
        self.reset_btn.clicked.connect(self.reset)

        # subscribe to draw events
        self.scroll_area_content = self.ui.scrollAreaWidgetContents
        self.scroll_area_content.installEventFilter(self)

        self.row_height = 50
        self.margin = 10
        self.d_margin = 2 * self.margin

        # size of the scroll area content
        self.max_width = 700
        self.max_height = 400

        self.tableaux_builder: BaseTableauxBuilder = None

        self.expr_btns = dict()

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent):
        if watched is self.scroll_area_content and type(event) is QPaintEvent:
            p = CustomPainter(self.scroll_area_content)
            p.begin()

            if self.tableaux_builder is None:
                # no expression entered yet
                p.draw_tableau_header(self.logic_type)
                p.end()
                return False

            # calculate horizontal center
            width_l, width_r = self.tableaux_builder.get_drawn_width(
                                    p.get_text_width, self.d_margin, self.mode == ResolveMode.Manual)
            x = width_l + self.d_margin
            x = max(x, self.d_margin + 125)  # ensure space to border

            p.drawLine(x - 125, 75, x + 125, 75)
            p.drawLine(x, 25, x, 125)
            p.drawText(x - 65, 50, self.tableaux_builder.left_side_sign)
            p.drawText(x + 62, 50, self.tableaux_builder.right_side_sign)

            manual = self.mode == ResolveMode.Manual
            intuitionistic = self.logic_type in [LogicType.IPROPOSITIONAL, LogicType.IFOPL]
            drawing_calculator = DrawingCalculator(
                self.tableaux_builder, p, manual,
                intuitionistic, self.margin, x
            )
            self.draw_path(p, self.tableaux_builder, drawing_calculator, x=x)

            p.end()

            self.scroll_area_content.setMinimumSize(self.max_width + self.d_margin,
                                                    self.max_height + self.d_margin)

        return False

    def get_y(self, layer):
        """
        Returns the vertical position of the given layer
        """
        return 125 + self.row_height * layer

    def manually_entered(self, success):
        self.input_window = None

        for k, btn in self.expr_btns.items():
            btn.hide()
            del btn
        self.expr_btns = dict()

        self.scroll_area_content.repaint()

    def manual_btn_pressed_wrapper(self, expr, tableau):
        def manual_btn_pressed():
            if self.input_window is not None:
                return
            self.input_window = InputWindow(self.manually_entered, self.logic_type, expr, tableau)
            self.input_window.show()
        return manual_btn_pressed

    def draw_btn(self, painter, tableau):
        def draw_btn(text, x, y, expr):
            if (x,y) not in self.expr_btns:
                btn = QPushButton(self.scroll_area_content)
                btn.show()
                btn.setText(text.replace('&', '&&'))
                btn.setGeometry(x, y - 20, painter.get_text_width(text), 26)
                btn.clicked.connect(self.manual_btn_pressed_wrapper(expr, tableau))

                self.expr_btns[(x,y)] = btn
        return draw_btn

    def draw_path(
                    self, p: CustomPainter,
                    tableau: BaseTableauxBuilder,
                    drawing_calculator,
                    layer=0, x=375):
        """
        Draws all expressions in the tableau
        """
        expr_pos = drawing_calculator.calc_expr_positions(self.draw_btn)

        # draw expressions
        for pos_x, expr, draw_fun, expr_str in expr_pos:
            y_1 = self.get_y(layer)
            y_2 = self.get_y(layer+1)
            draw_fun(expr_str, pos_x, y_1)
            p.drawLine(x, y_1, x, y_2)
            layer += 1

            # update max width/height
            txt_width = p.get_text_width(expr_str)
            self.max_width = max(self.max_width,
                                 pos_x + txt_width)
            self.max_height = max(self.max_height, y_2)

        if len(tableau.children) == 0:
            # draw end sign of the branch
            if drawing_calculator.closed:
                width = 10
                y = self.get_y(layer)
                p.drawLine(x - width, y, x + width, y)

            if drawing_calculator.done and not drawing_calculator.closed:
                diameter = 10
                p.drawEllipse(x - diameter / 2, self.get_y(layer),
                              diameter, diameter)
            return

        if len(tableau.children) == 1 and tableau.children[0].clears_false_exprs:
            # only a single child that clears false expressions
            child = tableau.children[0]
            width_l, width_r = child.get_drawn_width(p.get_text_width,
                                                    self.d_margin,
                                                    drawing_calculator.manual)
            y = self.get_y(layer)
            p.drawLine(x - width_l, y, x + width_r, y)
            p.drawLine(x, y, x, self.get_y(layer+1))
            self.draw_path(p, child,
                           drawing_calculator.get_child(0, x),
                           layer+1, x)

            return

        # draw left branch
        y = self.get_y(layer)
        left = tableau.children[0]
        width_l, width_r = left.get_drawn_width(p.get_text_width,
                                                self.d_margin,
                                                drawing_calculator.manual)
        new_x = x - width_r - self.d_margin
        x_1 = new_x - width_l - self.d_margin if left.clears_false_exprs else new_x
        p.drawLine(x, y, x_1, y)
        p.drawLine(new_x, y, new_x, self.get_y(layer+1))
        self.draw_path(p, left,
                       drawing_calculator.get_child(0, new_x),
                       layer+1, new_x)

        # draw right branch
        right = tableau.children[1]
        width_l, width_r = right.get_drawn_width(p.get_text_width,
                                                 self.d_margin,
                                                 drawing_calculator.manual)
        new_x = x + width_l + self.d_margin
        x_1 = new_x + width_r + self.d_margin if right.clears_false_exprs else new_x
        p.drawLine(x, y, x_1, y)
        p.drawLine(new_x, y, new_x, self.get_y(layer+1))
        self.draw_path(p, right,
                       drawing_calculator.get_child(1, new_x),
                       layer+1, new_x)

    def logic_changed(self):
        """
        This function is called when a logic radio button is toggled
        """
        if self.ui.pl_radio_btn.isChecked():
            self.logic_type = LogicType.PROPOSITIONAL
        if self.ui.fopl_radio_btn.isChecked():
            self.logic_type = LogicType.FOPL
        if self.ui.ipl_radio_btn.isChecked():
            self.logic_type = LogicType.IPROPOSITIONAL
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

    def calculate_pressed(self):
        """
        This function is called after the calculate button is pressed
        """
        # get the entered expressions
        left_exprs = self.parse_exprs(self.ui.inital_left_exprs_text_edit, self.scroll_area_content)
        right_exprs = self.parse_exprs(self.ui.inital_right_exprs_text_edit, self.scroll_area_content)

        if left_exprs is None or right_exprs is None:
            return

        constants = self.constants_from_trees(left_exprs + right_exprs)
        functions = self.functions_from_trees(left_exprs + right_exprs)
        left_exprs = self.exprs_from_trees(left_exprs)
        right_exprs = self.exprs_from_trees(right_exprs)

        # create tableau builder with expressions
        self.tableaux_builder = create_tableau_builder(
            logic_type=self.logic_type,
            left_exprs=left_exprs,
            right_exprs=right_exprs,
            visit_idx=self.parser.parse_idx,
            constants=constants,
            functions=functions,
        )

        # hide widgets to enter initial expressions
        self.ui.inital_left_exprs_text_edit.hide()
        self.ui.inital_right_exprs_text_edit.hide()
        self.ui.start_calc_btn.hide()
        self.ui.inital_left_exprs_text_edit.setStyleSheet('')
        self.ui.inital_right_exprs_text_edit.setStyleSheet('')
        self.ui.logic_type_gb.setEnabled(False)
        self.ui.calc_mode_gb.setEnabled(False)
        if self.error_widget is not None:
            self.error_widget.hide()

        # if automatic, try to auto resolve the tableau
        if self.mode == ResolveMode.Automatic:
            try:
                self.tableaux_builder.auto_resolve()
                self.scroll_area_content.repaint()
            except Exception as e:
                print(e)
                self.show_error(self.scroll_area_content,
                                '<b>No automatic resolution possible</b>'\
                                '<p>The automatic resolution failed. Try to calculate the Tableau manually.</p>')
                self.reset()

        self.scroll_area_content.repaint()

    def reset(self):
        if self.tableaux_builder is None:
            self.ui.inital_left_exprs_text_edit.setText('')
            self.ui.inital_right_exprs_text_edit.setText('')
        self.tableaux_builder = None
        self.ui.inital_left_exprs_text_edit.show()
        self.ui.inital_right_exprs_text_edit.show()
        self.ui.start_calc_btn.show()
        self.ui.logic_type_gb.setEnabled(True)
        self.ui.calc_mode_gb.setEnabled(True)
        self.ui.start_calc_btn.setEnabled(True)

        self.max_width = 700
        self.max_height = 400
        self.scroll_area_content.setMinimumSize(self.max_width + self.d_margin,
                                                    self.max_height + self.d_margin)

        for k, btn in self.expr_btns.items():
            btn.hide()
            del btn
        
        self.expr_btns = dict()

        self.scroll_area_content.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


