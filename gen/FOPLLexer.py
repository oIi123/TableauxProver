# Generated from D:/Studium/7_Studienarbeit/Impl/src/Parser\FOPL.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\20")
        buf.write("W\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\3\2\3\2\7\2\"\n\2\f\2\16\2%\13\2\3\2\3")
        buf.write("\2\3\3\3\3\7\3+\n\3\f\3\16\3.\13\3\3\4\3\4\7\4\62\n\4")
        buf.write("\f\4\16\4\65\13\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\7")
        buf.write("\3\b\3\b\3\t\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r")
        buf.write("\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\2")
        buf.write("\2\20\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27")
        buf.write("\r\31\16\33\17\35\20\3\2\6\3\2C\\\6\2\62;C\\aac|\3\2c")
        buf.write("|\5\2\13\f\17\17\"\"\2Y\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3")
        buf.write("\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2")
        buf.write("\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2")
        buf.write("\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\3\37\3\2\2\2\5")
        buf.write("(\3\2\2\2\7/\3\2\2\2\t8\3\2\2\2\13:\3\2\2\2\r<\3\2\2\2")
        buf.write("\17?\3\2\2\2\21A\3\2\2\2\23E\3\2\2\2\25G\3\2\2\2\27I\3")
        buf.write("\2\2\2\31K\3\2\2\2\33O\3\2\2\2\35S\3\2\2\2\37#\t\2\2\2")
        buf.write(" \"\t\3\2\2! \3\2\2\2\"%\3\2\2\2#!\3\2\2\2#$\3\2\2\2$")
        buf.write("&\3\2\2\2%#\3\2\2\2&\'\7*\2\2\'\4\3\2\2\2(,\t\4\2\2)+")
        buf.write("\t\3\2\2*)\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2\2-\6\3")
        buf.write("\2\2\2.,\3\2\2\2/\63\t\4\2\2\60\62\t\3\2\2\61\60\3\2\2")
        buf.write("\2\62\65\3\2\2\2\63\61\3\2\2\2\63\64\3\2\2\2\64\66\3\2")
        buf.write("\2\2\65\63\3\2\2\2\66\67\7*\2\2\67\b\3\2\2\289\7~\2\2")
        buf.write("9\n\3\2\2\2:;\7(\2\2;\f\3\2\2\2<=\7/\2\2=>\7@\2\2>\16")
        buf.write("\3\2\2\2?@\7#\2\2@\20\3\2\2\2AB\7>\2\2BC\7/\2\2CD\7@\2")
        buf.write("\2D\22\3\2\2\2EF\7*\2\2F\24\3\2\2\2GH\7+\2\2H\26\3\2\2")
        buf.write("\2IJ\7.\2\2J\30\3\2\2\2KL\7*\2\2LM\7C\2\2MN\7+\2\2N\32")
        buf.write("\3\2\2\2OP\7*\2\2PQ\7G\2\2QR\7+\2\2R\34\3\2\2\2ST\t\5")
        buf.write("\2\2TU\3\2\2\2UV\b\17\2\2V\36\3\2\2\2\6\2#,\63\3\b\2\2")
        return buf.getvalue()


class FOPLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    PREDNAME = 1
    VARNAME = 2
    FUNCNAME = 3
    OR = 4
    AND = 5
    IMPL = 6
    NOT = 7
    EQ = 8
    OPENCLAMP = 9
    CLOSECLAMP = 10
    COMMA = 11
    ALL_QUANTOR = 12
    EX_QUANTOR = 13
    WS = 14

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'|'", "'&'", "'->'", "'!'", "'<->'", "'('", "')'", "','", "'(A)'", 
            "'(E)'" ]

    symbolicNames = [ "<INVALID>",
            "PREDNAME", "VARNAME", "FUNCNAME", "OR", "AND", "IMPL", "NOT", 
            "EQ", "OPENCLAMP", "CLOSECLAMP", "COMMA", "ALL_QUANTOR", "EX_QUANTOR", 
            "WS" ]

    ruleNames = [ "PREDNAME", "VARNAME", "FUNCNAME", "OR", "AND", "IMPL", 
                  "NOT", "EQ", "OPENCLAMP", "CLOSECLAMP", "COMMA", "ALL_QUANTOR", 
                  "EX_QUANTOR", "WS" ]

    grammarFileName = "FOPL.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


