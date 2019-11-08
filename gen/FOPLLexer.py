# Generated from D:/Studium/7_Studienarbeit/Impl/src/Parser\FOPL.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\21")
        buf.write("f\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\3\2\7\2$\n\2\f\2\16\2\'")
        buf.write("\13\2\3\2\3\2\3\3\3\3\7\3-\n\3\f\3\16\3\60\13\3\3\4\3")
        buf.write("\4\7\4\64\n\4\f\4\16\4\67\13\4\3\5\3\5\7\5;\n\5\f\5\16")
        buf.write("\5>\13\5\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\b\3\t\3\t\3")
        buf.write("\n\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\16")
        buf.write("\3\16\3\16\5\16Z\n\16\3\17\3\17\3\17\3\17\3\17\5\17a\n")
        buf.write("\17\3\20\3\20\3\20\3\20\2\2\21\3\3\5\4\7\5\t\6\13\7\r")
        buf.write("\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21\3")
        buf.write("\2\n\3\2C\\\6\2\62;C\\aac|\3\2c|\5\2\62;C\\c|\4\2--~~")
        buf.write("\4\2((,,\4\2##//\5\2\13\f\17\17\"\"\2k\2\3\3\2\2\2\2\5")
        buf.write("\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2")
        buf.write("\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2")
        buf.write("\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2")
        buf.write("\2\37\3\2\2\2\3!\3\2\2\2\5*\3\2\2\2\7\61\3\2\2\2\t8\3")
        buf.write("\2\2\2\13A\3\2\2\2\rC\3\2\2\2\17E\3\2\2\2\21H\3\2\2\2")
        buf.write("\23J\3\2\2\2\25N\3\2\2\2\27P\3\2\2\2\31R\3\2\2\2\33Y\3")
        buf.write("\2\2\2\35`\3\2\2\2\37b\3\2\2\2!%\t\2\2\2\"$\t\3\2\2#\"")
        buf.write("\3\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3\2\2\2&(\3\2\2\2\'%\3")
        buf.write("\2\2\2()\7*\2\2)\4\3\2\2\2*.\t\4\2\2+-\t\5\2\2,+\3\2\2")
        buf.write("\2-\60\3\2\2\2.,\3\2\2\2./\3\2\2\2/\6\3\2\2\2\60.\3\2")
        buf.write("\2\2\61\65\t\2\2\2\62\64\t\5\2\2\63\62\3\2\2\2\64\67\3")
        buf.write("\2\2\2\65\63\3\2\2\2\65\66\3\2\2\2\66\b\3\2\2\2\67\65")
        buf.write("\3\2\2\28<\t\4\2\29;\t\3\2\2:9\3\2\2\2;>\3\2\2\2<:\3\2")
        buf.write("\2\2<=\3\2\2\2=?\3\2\2\2><\3\2\2\2?@\7*\2\2@\n\3\2\2\2")
        buf.write("AB\t\6\2\2B\f\3\2\2\2CD\t\7\2\2D\16\3\2\2\2EF\7/\2\2F")
        buf.write("G\7@\2\2G\20\3\2\2\2HI\t\b\2\2I\22\3\2\2\2JK\7>\2\2KL")
        buf.write("\7/\2\2LM\7@\2\2M\24\3\2\2\2NO\7*\2\2O\26\3\2\2\2PQ\7")
        buf.write("+\2\2Q\30\3\2\2\2RS\7.\2\2S\32\3\2\2\2TU\7*\2\2UV\7C\2")
        buf.write("\2VZ\7+\2\2WX\7\61\2\2XZ\7^\2\2YT\3\2\2\2YW\3\2\2\2Z\34")
        buf.write("\3\2\2\2[\\\7*\2\2\\]\7G\2\2]a\7+\2\2^_\7^\2\2_a\7\61")
        buf.write("\2\2`[\3\2\2\2`^\3\2\2\2a\36\3\2\2\2bc\t\t\2\2cd\3\2\2")
        buf.write("\2de\b\20\2\2e \3\2\2\2\t\2%.\65<Y`\3\b\2\2")
        return buf.getvalue()


class FOPLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    PREDNAME = 1
    VARNAME = 2
    CONSTNAME = 3
    FUNCNAME = 4
    OR = 5
    AND = 6
    IMPL = 7
    NOT = 8
    EQ = 9
    OPENCLAMP = 10
    CLOSECLAMP = 11
    COMMA = 12
    ALL_QUANTOR = 13
    EX_QUANTOR = 14
    WS = 15

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'->'", "'<->'", "'('", "')'", "','" ]

    symbolicNames = [ "<INVALID>",
            "PREDNAME", "VARNAME", "CONSTNAME", "FUNCNAME", "OR", "AND", 
            "IMPL", "NOT", "EQ", "OPENCLAMP", "CLOSECLAMP", "COMMA", "ALL_QUANTOR", 
            "EX_QUANTOR", "WS" ]

    ruleNames = [ "PREDNAME", "VARNAME", "CONSTNAME", "FUNCNAME", "OR", 
                  "AND", "IMPL", "NOT", "EQ", "OPENCLAMP", "CLOSECLAMP", 
                  "COMMA", "ALL_QUANTOR", "EX_QUANTOR", "WS" ]

    grammarFileName = "FOPL.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


