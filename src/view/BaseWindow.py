from PySide2.QtWidgets import QMainWindow, QWidget
from src.builder_factory import *


class BaseWindow(QMainWindow):
    error_widget = None
    logic_type = LogicType.PROPOSITIONAL
    parser = None

    def parse_exprs(self, txt_area, include_cf=False):
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
                self.show_error(txt_area, str(e), nr+1)
                return None
            if nr in cf_lines:
                parsed_cf_lines.append(parsed_line)
            else:
                parsed_lines.append(parsed_line)
        
        parsed_lines = [tree.expr for tree in parsed_lines]
        parsed_cf_lines = [tree.expr for tree in parsed_cf_lines]

        if include_cf:
            return (parsed_lines, parsed_cf_lines)
        return parsed_lines

    def show_error(self, view: QWidget, txt: str, line: int):
        view.setStyleSheet('border: 1px solid rgb(240, 60, 60);')

        self.error_widget = QTextEdit(parent=self.scroll_area_content)
        self.error_widget.setGeometry(25, 400, 732, 62)
        self.error_widget.setStyleSheet(
            'background-color: rgb(240, 60, 60); border-radius: 10px;')

        txt = f'<b>Error in line {line}</b><p>{txt}</h1>'
        self.error_widget.setHtml(txt)
        self.error_widget.setReadOnly(True)

        self.error_widget.show()
