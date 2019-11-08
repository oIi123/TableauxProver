# Generated from D:/Studium/7_Studienarbeit/Impl/src/Parser\FOPL.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("a\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\5\2\"\n\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\7\2\60\n\2\f\2\16\2\63\13\2\3")
        buf.write("\3\3\3\3\3\5\38\n\3\3\3\3\3\3\4\3\4\3\4\3\4\3\5\3\5\3")
        buf.write("\5\3\6\3\6\3\6\3\6\3\6\5\6H\n\6\3\7\3\7\3\7\5\7M\n\7\3")
        buf.write("\b\3\b\3\t\3\t\3\n\3\n\3\n\3\n\3\n\5\nX\n\n\3\13\3\13")
        buf.write("\3\13\5\13]\n\13\3\13\3\13\3\13\2\3\2\f\2\4\6\b\n\f\16")
        buf.write("\20\22\24\2\3\3\2\17\20\2c\2!\3\2\2\2\4\64\3\2\2\2\6;")
        buf.write("\3\2\2\2\b?\3\2\2\2\nG\3\2\2\2\fL\3\2\2\2\16N\3\2\2\2")
        buf.write("\20P\3\2\2\2\22W\3\2\2\2\24Y\3\2\2\2\26\27\b\2\1\2\27")
        buf.write("\"\5\4\3\2\30\31\5\6\4\2\31\32\5\2\2\t\32\"\3\2\2\2\33")
        buf.write("\34\7\n\2\2\34\"\5\2\2\b\35\36\7\f\2\2\36\37\5\2\2\2\37")
        buf.write(" \7\r\2\2 \"\3\2\2\2!\26\3\2\2\2!\30\3\2\2\2!\33\3\2\2")
        buf.write("\2!\35\3\2\2\2\"\61\3\2\2\2#$\f\7\2\2$%\7\b\2\2%\60\5")
        buf.write("\2\2\b&\'\f\6\2\2\'(\7\7\2\2(\60\5\2\2\7)*\f\5\2\2*+\7")
        buf.write("\t\2\2+\60\5\2\2\6,-\f\4\2\2-.\7\13\2\2.\60\5\2\2\5/#")
        buf.write("\3\2\2\2/&\3\2\2\2/)\3\2\2\2/,\3\2\2\2\60\63\3\2\2\2\61")
        buf.write("/\3\2\2\2\61\62\3\2\2\2\62\3\3\2\2\2\63\61\3\2\2\2\64")
        buf.write("\67\7\3\2\2\658\5\b\5\2\668\3\2\2\2\67\65\3\2\2\2\67\66")
        buf.write("\3\2\2\289\3\2\2\29:\7\r\2\2:\5\3\2\2\2;<\t\2\2\2<=\5")
        buf.write("\16\b\2=>\5\22\n\2>\7\3\2\2\2?@\5\f\7\2@A\5\n\6\2A\t\3")
        buf.write("\2\2\2BC\7\16\2\2CD\5\f\7\2DE\5\n\6\2EH\3\2\2\2FH\3\2")
        buf.write("\2\2GB\3\2\2\2GF\3\2\2\2H\13\3\2\2\2IM\5\16\b\2JM\5\20")
        buf.write("\t\2KM\5\24\13\2LI\3\2\2\2LJ\3\2\2\2LK\3\2\2\2M\r\3\2")
        buf.write("\2\2NO\7\4\2\2O\17\3\2\2\2PQ\7\5\2\2Q\21\3\2\2\2RS\7\16")
        buf.write("\2\2ST\5\16\b\2TU\5\22\n\2UX\3\2\2\2VX\3\2\2\2WR\3\2\2")
        buf.write("\2WV\3\2\2\2X\23\3\2\2\2Y\\\7\6\2\2Z]\5\b\5\2[]\3\2\2")
        buf.write("\2\\Z\3\2\2\2\\[\3\2\2\2]^\3\2\2\2^_\7\r\2\2_\25\3\2\2")
        buf.write("\2\n!/\61\67GLW\\")
        return buf.getvalue()


class FOPLParser ( Parser ):

    grammarFileName = "FOPL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'->'", "<INVALID>", 
                     "'<->'", "'('", "')'", "','" ]

    symbolicNames = [ "<INVALID>", "PREDNAME", "VARNAME", "CONSTNAME", "FUNCNAME", 
                      "OR", "AND", "IMPL", "NOT", "EQ", "OPENCLAMP", "CLOSECLAMP", 
                      "COMMA", "ALL_QUANTOR", "EX_QUANTOR", "WS" ]

    RULE_expr = 0
    RULE_predicate = 1
    RULE_quantor = 2
    RULE_terms = 3
    RULE_termlist = 4
    RULE_term = 5
    RULE_var = 6
    RULE_const = 7
    RULE_varlist = 8
    RULE_func = 9

    ruleNames =  [ "expr", "predicate", "quantor", "terms", "termlist", 
                   "term", "var", "const", "varlist", "func" ]

    EOF = Token.EOF
    PREDNAME=1
    VARNAME=2
    CONSTNAME=3
    FUNCNAME=4
    OR=5
    AND=6
    IMPL=7
    NOT=8
    EQ=9
    OPENCLAMP=10
    CLOSECLAMP=11
    COMMA=12
    ALL_QUANTOR=13
    EX_QUANTOR=14
    WS=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicate(self):
            return self.getTypedRuleContext(FOPLParser.PredicateContext,0)


        def quantor(self):
            return self.getTypedRuleContext(FOPLParser.QuantorContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FOPLParser.ExprContext)
            else:
                return self.getTypedRuleContext(FOPLParser.ExprContext,i)


        def NOT(self):
            return self.getToken(FOPLParser.NOT, 0)

        def OPENCLAMP(self):
            return self.getToken(FOPLParser.OPENCLAMP, 0)

        def CLOSECLAMP(self):
            return self.getToken(FOPLParser.CLOSECLAMP, 0)

        def AND(self):
            return self.getToken(FOPLParser.AND, 0)

        def OR(self):
            return self.getToken(FOPLParser.OR, 0)

        def IMPL(self):
            return self.getToken(FOPLParser.IMPL, 0)

        def EQ(self):
            return self.getToken(FOPLParser.EQ, 0)

        def getRuleIndex(self):
            return FOPLParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = FOPLParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.PREDNAME]:
                self.state = 21
                self.predicate()
                pass
            elif token in [FOPLParser.ALL_QUANTOR, FOPLParser.EX_QUANTOR]:
                self.state = 22
                self.quantor()
                self.state = 23
                self.expr(7)
                pass
            elif token in [FOPLParser.NOT]:
                self.state = 25
                self.match(FOPLParser.NOT)
                self.state = 26
                self.expr(6)
                pass
            elif token in [FOPLParser.OPENCLAMP]:
                self.state = 27
                self.match(FOPLParser.OPENCLAMP)
                self.state = 28
                self.expr(0)
                self.state = 29
                self.match(FOPLParser.CLOSECLAMP)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 47
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 45
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 33
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 34
                        self.match(FOPLParser.AND)
                        self.state = 35
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 36
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 37
                        self.match(FOPLParser.OR)
                        self.state = 38
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 39
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 40
                        self.match(FOPLParser.IMPL)
                        self.state = 41
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 42
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 43
                        self.match(FOPLParser.EQ)
                        self.state = 44
                        self.expr(3)
                        pass

             
                self.state = 49
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PredicateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PREDNAME(self):
            return self.getToken(FOPLParser.PREDNAME, 0)

        def CLOSECLAMP(self):
            return self.getToken(FOPLParser.CLOSECLAMP, 0)

        def terms(self):
            return self.getTypedRuleContext(FOPLParser.TermsContext,0)


        def getRuleIndex(self):
            return FOPLParser.RULE_predicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate" ):
                listener.enterPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate" ):
                listener.exitPredicate(self)




    def predicate(self):

        localctx = FOPLParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_predicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(FOPLParser.PREDNAME)
            self.state = 53
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.VARNAME, FOPLParser.CONSTNAME, FOPLParser.FUNCNAME]:
                self.state = 51
                self.terms()
                pass
            elif token in [FOPLParser.CLOSECLAMP]:
                pass
            else:
                raise NoViableAltException(self)

            self.state = 55
            self.match(FOPLParser.CLOSECLAMP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var(self):
            return self.getTypedRuleContext(FOPLParser.VarContext,0)


        def varlist(self):
            return self.getTypedRuleContext(FOPLParser.VarlistContext,0)


        def ALL_QUANTOR(self):
            return self.getToken(FOPLParser.ALL_QUANTOR, 0)

        def EX_QUANTOR(self):
            return self.getToken(FOPLParser.EX_QUANTOR, 0)

        def getRuleIndex(self):
            return FOPLParser.RULE_quantor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantor" ):
                listener.enterQuantor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantor" ):
                listener.exitQuantor(self)




    def quantor(self):

        localctx = FOPLParser.QuantorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_quantor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            _la = self._input.LA(1)
            if not(_la==FOPLParser.ALL_QUANTOR or _la==FOPLParser.EX_QUANTOR):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 58
            self.var()
            self.state = 59
            self.varlist()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(FOPLParser.TermContext,0)


        def termlist(self):
            return self.getTypedRuleContext(FOPLParser.TermlistContext,0)


        def getRuleIndex(self):
            return FOPLParser.RULE_terms

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerms" ):
                listener.enterTerms(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerms" ):
                listener.exitTerms(self)




    def terms(self):

        localctx = FOPLParser.TermsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_terms)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.term()
            self.state = 62
            self.termlist()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermlistContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMA(self):
            return self.getToken(FOPLParser.COMMA, 0)

        def term(self):
            return self.getTypedRuleContext(FOPLParser.TermContext,0)


        def termlist(self):
            return self.getTypedRuleContext(FOPLParser.TermlistContext,0)


        def getRuleIndex(self):
            return FOPLParser.RULE_termlist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermlist" ):
                listener.enterTermlist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermlist" ):
                listener.exitTermlist(self)




    def termlist(self):

        localctx = FOPLParser.TermlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_termlist)
        try:
            self.state = 69
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.COMMA]:
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.match(FOPLParser.COMMA)
                self.state = 65
                self.term()
                self.state = 66
                self.termlist()
                pass
            elif token in [FOPLParser.CLOSECLAMP]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var(self):
            return self.getTypedRuleContext(FOPLParser.VarContext,0)


        def const(self):
            return self.getTypedRuleContext(FOPLParser.ConstContext,0)


        def func(self):
            return self.getTypedRuleContext(FOPLParser.FuncContext,0)


        def getRuleIndex(self):
            return FOPLParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)




    def term(self):

        localctx = FOPLParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_term)
        try:
            self.state = 74
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.VARNAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 71
                self.var()
                pass
            elif token in [FOPLParser.CONSTNAME]:
                self.enterOuterAlt(localctx, 2)
                self.state = 72
                self.const()
                pass
            elif token in [FOPLParser.FUNCNAME]:
                self.enterOuterAlt(localctx, 3)
                self.state = 73
                self.func()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARNAME(self):
            return self.getToken(FOPLParser.VARNAME, 0)

        def getRuleIndex(self):
            return FOPLParser.RULE_var

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar" ):
                listener.enterVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar" ):
                listener.exitVar(self)




    def var(self):

        localctx = FOPLParser.VarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_var)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(FOPLParser.VARNAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONSTNAME(self):
            return self.getToken(FOPLParser.CONSTNAME, 0)

        def getRuleIndex(self):
            return FOPLParser.RULE_const

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConst" ):
                listener.enterConst(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConst" ):
                listener.exitConst(self)




    def const(self):

        localctx = FOPLParser.ConstContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_const)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.match(FOPLParser.CONSTNAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarlistContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMA(self):
            return self.getToken(FOPLParser.COMMA, 0)

        def var(self):
            return self.getTypedRuleContext(FOPLParser.VarContext,0)


        def varlist(self):
            return self.getTypedRuleContext(FOPLParser.VarlistContext,0)


        def getRuleIndex(self):
            return FOPLParser.RULE_varlist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarlist" ):
                listener.enterVarlist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarlist" ):
                listener.exitVarlist(self)




    def varlist(self):

        localctx = FOPLParser.VarlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_varlist)
        try:
            self.state = 85
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.COMMA]:
                self.enterOuterAlt(localctx, 1)
                self.state = 80
                self.match(FOPLParser.COMMA)
                self.state = 81
                self.var()
                self.state = 82
                self.varlist()
                pass
            elif token in [FOPLParser.PREDNAME, FOPLParser.NOT, FOPLParser.OPENCLAMP, FOPLParser.ALL_QUANTOR, FOPLParser.EX_QUANTOR]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCNAME(self):
            return self.getToken(FOPLParser.FUNCNAME, 0)

        def CLOSECLAMP(self):
            return self.getToken(FOPLParser.CLOSECLAMP, 0)

        def terms(self):
            return self.getTypedRuleContext(FOPLParser.TermsContext,0)


        def getRuleIndex(self):
            return FOPLParser.RULE_func

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunc" ):
                listener.enterFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunc" ):
                listener.exitFunc(self)




    def func(self):

        localctx = FOPLParser.FuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_func)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(FOPLParser.FUNCNAME)
            self.state = 90
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.VARNAME, FOPLParser.CONSTNAME, FOPLParser.FUNCNAME]:
                self.state = 88
                self.terms()
                pass
            elif token in [FOPLParser.CLOSECLAMP]:
                pass
            else:
                raise NoViableAltException(self)

            self.state = 92
            self.match(FOPLParser.CLOSECLAMP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         




