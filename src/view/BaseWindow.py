from PySide2.QtWidgets import QMainWindow, QWidget, QTextEdit
from antlr4 import RecognitionException
from src.builder_factory import *
from src.view.Help import HelpWindow


def concat_list_of_lists(list_of_lists):
    concat = list()
    for lst in list_of_lists:
        concat += lst
    return list(set(concat))


class BaseWindow(QMainWindow):
    error_widget = None
    logic_type = LogicType.PROPOSITIONAL
    parser = None

    def parse_exprs(self, txt_area, scroll_view, include_cf=False):
        parsed_lines = []
        parsed_cf_lines = []
        self.parser = create_parser(self.logic_type)

        text = txt_area.toPlainText()
        lines = [s.strip() for s in text.split('\n') if s.strip() != '']
        cf_lines = []
        if include_cf:
            cf_lines = [i for i, s in enumerate(lines) if s.startswith('[') and s.endswith(']')]
            lines = [l[1:-1] if i in cf_lines else l for i, l in enumerate(lines)]
        parsed_line = None
        for nr, line in enumerate(lines):
            try:
                parsed_line = self.parser.parse(line)
            except RecognitionException as e:
                self.show_line_error(scroll_view, txt_area, str(e), nr+1)
                return None
            if nr in cf_lines:
                parsed_cf_lines.append(parsed_line)
            else:
                parsed_lines.append(parsed_line)

        if include_cf:
            return (parsed_lines, parsed_cf_lines)
        return parsed_lines

    def exprs_from_trees(self, trees):
        return [tree.expr for tree in trees]
    
    def functions_from_trees(self, trees):
        return concat_list_of_lists([tree.functions for tree in trees if hasattr(tree, 'functions')])

    def constants_from_trees(self, trees):
        return concat_list_of_lists([tree.constants for tree in trees if hasattr(tree, 'constants')])

    def show_error(self, scroll_view: QWidget, txt: str):
        if self.error_widget is not None:
            self.error_widget.hide()
            del self.error_widget

        geometry = scroll_view.geometry()

        self.error_widget = QTextEdit(parent=scroll_view)
        self.error_widget.setGeometry(25, geometry.height() - 85, geometry.width() - 50, 60) #25, 400, 732, 62)
        self.error_widget.setStyleSheet(
            'background-color: rgb(240, 60, 60); border-radius: 10px;')

        self.error_widget.setHtml(txt)
        self.error_widget.setReadOnly(True)

        self.error_widget.show()

    def show_line_error(self, scroll_view: QWidget, txt_view: QWidget, txt: str, line: int):
        txt_view.setStyleSheet('border: 1px solid rgb(240, 60, 60);')

        txt = f'<b>Error in line {line}</b><p>{txt}</h1>'
        self.show_error(scroll_view, txt)

    def show_help(self):
        HelpWindow.show_help()
