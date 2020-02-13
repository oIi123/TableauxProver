import PySide2

from src.TableauxBuilder.BaseManualTableau import BaseManualTableau
from src.builder_factory import *
from src.view.ui_inputwindow import Ui_MainWindow as Ui_InputWindow
from src.view.CustomPainter import CustomPainter
from PySide2.QtGui import QPainter, QPaintEvent, QHideEvent, QFontMetrics
from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QMainWindow
from src.view.BaseWindow import BaseWindow

class InputWindow(BaseWindow):
    margin = 10

    def __init__(self, callback, logic_type, expr, tableau_builder):
        super().__init__()
        self.ui = Ui_InputWindow()
        self.ui.setupUi(self)

        self.ui.ok_btn.clicked.connect(self.ok_pressed)
        self.ui.cancel_btn.clicked.connect(self.cancel_pressed)
        self.ui.help_btn.clicked.connect(self.show_help)

        self.installEventFilter(self)
        self.ui.scrollAreaContentsSingle.installEventFilter(self)
        self.ui.scrollAreaContentsBranch.installEventFilter(self)

        self.callback = callback
        self.logic_type = logic_type
        self.expr = expr
        l, r, cf = expr
        if l:
            self.expr_name = l.name
        elif r:
            self.expr_name = r.name
        elif cf:
            self.expr_name = cf.name
        self.manual_tableau = BaseManualTableau(logic_type, tableau_builder)

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent):
        if watched is self.ui.scrollAreaContentsSingle and type(event) is QPaintEvent:
            self.draw_single()
        elif watched is self.ui.scrollAreaContentsBranch and type(event) is QPaintEvent:
            self.draw_branch()
        elif event.type() == QEvent.Close:
            self.callback(False)
        
        return False

    def ok_pressed(self):
        self.reset()
        intuitionistic_logic = self.logic_type in [LogicType.IPROPOSITIONAL, LogicType.IFOPL]

        if self.ui.tab_bar.currentIndex() == 0:
            # single tab
            left_exprs = self.parse_exprs(self.ui.deduction_single_left, self.ui.scrollAreaContentsSingle)
            right_exprs = self.parse_exprs(self.ui.deduction_single_right, self.ui.scrollAreaContentsSingle, include_cf=intuitionistic_logic)
            cf_exprs = []
            
            # check if parsing successfull
            if left_exprs is None or right_exprs is None:
                return
            
            if intuitionistic_logic:
                right_exprs, cf_exprs = right_exprs

            constants = self.constants_from_trees(left_exprs + right_exprs)
            left_exprs = self.exprs_from_trees(left_exprs)
            right_exprs = self.exprs_from_trees(right_exprs)
            cf_exprs = self.exprs_from_trees(cf_exprs)

            if self.manual_tableau.merge(self.expr, [left_exprs], [right_exprs], [cf_exprs], constants):
                self.callback(True)
                self.close()
                return
            self.show_error(self.ui.scrollAreaContentsSingle,
                            f'<b>Wrong Derivation</b><p>Wrong application of the resolution rule for {self.expr_name}</<p>')
        else:
            # branch tab
            ll_exprs = self.parse_exprs(self.ui.deduction_branch_ll, self.ui.scrollAreaContentsBranch)
            lr_exprs = self.parse_exprs(self.ui.deduction_branch_lr, self.ui.scrollAreaContentsBranch, include_cf=intuitionistic_logic)
            rl_exprs = self.parse_exprs(self.ui.deduction_branch_rl, self.ui.scrollAreaContentsBranch)
            rr_exprs = self.parse_exprs(self.ui.deduction_branch_rr, self.ui.scrollAreaContentsBranch, include_cf=intuitionistic_logic)
            cf_exprs = ([],[])

            # check if parsing successfull
            if ll_exprs is None or lr_exprs is None or rl_exprs is None or rr_exprs is None:
                return

            if intuitionistic_logic:
                lr_exprs, l_cf_exprs = lr_exprs
                rr_exprs, r_cf_exprs = rr_exprs
                cf_exprs = (self.exprs_from_trees(l_cf_exprs), self.exprs_from_trees(r_cf_exprs))
            
            constants_l = self.constants_from_trees(ll_exprs + lr_exprs)
            constants_r = self.constants_from_trees(rl_exprs + rr_exprs)
            ll_exprs = self.exprs_from_trees(ll_exprs)
            lr_exprs = self.exprs_from_trees(lr_exprs)
            rl_exprs = self.exprs_from_trees(rl_exprs)
            rr_exprs = self.exprs_from_trees(rr_exprs)

            if self.manual_tableau.merge(self.expr, (ll_exprs, rl_exprs), (lr_exprs, rr_exprs), cf_exprs, (constants_l, constants_r)):
                self.callback(True)
                self.close()
                return
            self.show_error(self.ui.scrollAreaContentsBranch,
                            f'<b>Wrong Derivation</b><p>Wrong application of the resolution rule for {self.expr_name}</<p>')

    def reset(self):
        for txt_input in [
            self.ui.deduction_single_left,
            self.ui.deduction_single_right,
            self.ui.deduction_branch_ll,
            self.ui.deduction_branch_lr,
            self.ui.deduction_branch_rl,
            self.ui.deduction_branch_rr,
        ]:
            txt_input.setStyleSheet('')

    def cancel_pressed(self):
        self.callback(False)
        self.close()

    def draw_expr(self, painter, x=400):
        t, f, cf = self.expr

        expr_str = ""
        if t is not None:
            expr_str = str(t)
            x -= self.margin + painter.get_text_width(expr_str)
        elif f is not None:
            expr_str = str(f)
            x += self.margin
        elif cf is not None:
            expr_str = "[" + str(cf) + "]"
            x += self.margin
        
        painter.draw_normal(expr_str, x, 125)

    def draw_single(self):
        p = CustomPainter()
        p.begin(self.ui.scrollAreaContentsSingle)

        center_x = self.get_tableau_center(p)
        p.draw_tableau_header(self.logic_type, center_x=center_x, height=275)
        self.draw_expr(p, center_x)

        self.ui.deduction_single_left.setGeometry(center_x - 175, 135, 165, 200)
        self.ui.deduction_single_right.setGeometry(center_x + 10, 135, 165, 200)

        width = max(400, self.get_expr_width(p) + 2 * self.margin) + 400

        p.end()
        
        self.ui.scrollAreaContentsSingle.setMinimumSize(width, 407)

    def draw_branch(self):
        p = CustomPainter()
        p.begin(self.ui.scrollAreaContentsBranch)

        center_x = self.get_tableau_center(p)
        p.draw_tableau_header(self.logic_type, center_x=center_x, height=100)

        # draw branch lines
        l = center_x - 190
        r = center_x + 190
        p.drawLine(l, 175, r, 175)
        p.drawLine(l, 175, l, 400)
        p.drawLine(r, 175, r, 400)

        # position text areas
        self.ui.deduction_branch_ll.setGeometry(l - 175, 185, 165, 200)
        self.ui.deduction_branch_lr.setGeometry(l + 10, 185, 165, 200)
        self.ui.deduction_branch_rl.setGeometry(r - 175, 185, 165, 200)
        self.ui.deduction_branch_rr.setGeometry(r + 10, 185, 165, 200)

        self.draw_expr(p, center_x)

        width = max(400, self.get_expr_width(p) + 2 * self.margin) + 400

        p.end()

        self.ui.scrollAreaContentsBranch.setMinimumSize(width, 407)

    def get_tableau_center(self, painter):
        t, f, cf = self.expr
        x = 400
        if t is not None:
            width = painter.get_text_width(str(t))
            width += 2 * self.margin
            x = max(width, x)
        return x

    def get_expr_width(self, painter):
        t, f, cf = self.expr
        if t is not None:
            return painter.get_text_width(str(t))
        if f is not None:
            return painter.get_text_width(str(f))
        if cf is not None:
            return painter.get_text_width('[' + str(cf) + ']')
