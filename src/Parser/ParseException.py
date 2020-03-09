from antlr4 import RecognitionException
from antlr4.error.ErrorListener import ErrorListener


class ParseException(RecognitionException):
    def __init__(self, message=None, column=0, width=1, recognizer=None, input=None, ctx=None):
        super().__init__(message=message, recognizer=recognizer, input=input, ctx=ctx)
        self.column = column
        self.width = width


class ParserErrorListener(ErrorListener):
    error_msg = None
    column = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if self.error_msg is None:
            self.error_msg = f"The input was incorrect."
        self.error_msg += f"<br/>Column {column}: {msg}"
        self.column = column
