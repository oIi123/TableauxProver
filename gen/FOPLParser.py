# Generated from D:/Studium/7_Studienarbeit/Impl/src/Parser\FOPL.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\20")
        buf.write("V\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\5\2 \n\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\7\2.\n\2\f\2\16\2\61\13\2\3\3\3\3\3\3\3")
        buf.write("\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\5\6")
        buf.write("C\n\6\3\7\3\7\5\7G\n\7\3\b\3\b\3\t\3\t\3\t\3\t\3\t\5\t")
        buf.write("P\n\t\3\n\3\n\3\n\3\n\3\n\2\3\2\13\2\4\6\b\n\f\16\20\22")
        buf.write("\2\3\3\2\16\17\2V\2\37\3\2\2\2\4\62\3\2\2\2\6\66\3\2\2")
        buf.write("\2\b:\3\2\2\2\nB\3\2\2\2\fF\3\2\2\2\16H\3\2\2\2\20O\3")
        buf.write("\2\2\2\22Q\3\2\2\2\24\25\b\2\1\2\25 \5\4\3\2\26\27\7\t")
        buf.write("\2\2\27 \5\2\2\t\30\31\5\6\4\2\31\32\5\2\2\4\32 \3\2\2")
        buf.write("\2\33\34\7\13\2\2\34\35\5\2\2\2\35\36\7\f\2\2\36 \3\2")
        buf.write("\2\2\37\24\3\2\2\2\37\26\3\2\2\2\37\30\3\2\2\2\37\33\3")
        buf.write("\2\2\2 /\3\2\2\2!\"\f\b\2\2\"#\7\7\2\2#.\5\2\2\t$%\f\7")
        buf.write("\2\2%&\7\6\2\2&.\5\2\2\b\'(\f\6\2\2()\7\b\2\2).\5\2\2")
        buf.write("\7*+\f\5\2\2+,\7\n\2\2,.\5\2\2\6-!\3\2\2\2-$\3\2\2\2-")
        buf.write("\'\3\2\2\2-*\3\2\2\2.\61\3\2\2\2/-\3\2\2\2/\60\3\2\2\2")
        buf.write("\60\3\3\2\2\2\61/\3\2\2\2\62\63\7\3\2\2\63\64\5\b\5\2")
        buf.write("\64\65\7\f\2\2\65\5\3\2\2\2\66\67\t\2\2\2\678\5\16\b\2")
        buf.write("89\5\20\t\29\7\3\2\2\2:;\5\f\7\2;<\5\n\6\2<\t\3\2\2\2")
        buf.write("=>\7\r\2\2>?\5\f\7\2?@\5\n\6\2@C\3\2\2\2AC\3\2\2\2B=\3")
        buf.write("\2\2\2BA\3\2\2\2C\13\3\2\2\2DG\5\16\b\2EG\5\22\n\2FD\3")
        buf.write("\2\2\2FE\3\2\2\2G\r\3\2\2\2HI\7\4\2\2I\17\3\2\2\2JK\7")
        buf.write("\r\2\2KL\5\16\b\2LM\5\20\t\2MP\3\2\2\2NP\3\2\2\2OJ\3\2")
        buf.write("\2\2ON\3\2\2\2P\21\3\2\2\2QR\7\5\2\2RS\5\b\5\2ST\7\f\2")
        buf.write("\2T\23\3\2\2\2\b\37-/BFO")
        return buf.getvalue()


class FOPLParser ( Parser ):

    grammarFileName = "FOPL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'|'", "'&'", "'->'", "'!'", "'<->'", "'('", "')'", 
                     "','", "'@'", "'\u00E2\u201A\u00AC'" ]

    symbolicNames = [ "<INVALID>", "PREDNAME", "VARNAME", "FUNCNAME", "OR", 
                      "AND", "IMPL", "NOT", "EQ", "OPENCLAMP", "CLOSECLAMP", 
                      "COMMA", "ALL_QUANTOR", "EX_QUANTOR", "WS" ]

    RULE_expr = 0
    RULE_predicate = 1
    RULE_quantor = 2
    RULE_terms = 3
    RULE_termlist = 4
    RULE_term = 5
    RULE_var = 6
    RULE_varlist = 7
    RULE_func = 8

    ruleNames =  [ "expr", "predicate", "quantor", "terms", "termlist", 
                   "term", "var", "varlist", "func" ]

    EOF = Token.EOF
    PREDNAME=1
    VARNAME=2
    FUNCNAME=3
    OR=4
    AND=5
    IMPL=6
    NOT=7
    EQ=8
    OPENCLAMP=9
    CLOSECLAMP=10
    COMMA=11
    ALL_QUANTOR=12
    EX_QUANTOR=13
    WS=14

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


        def NOT(self):
            return self.getToken(FOPLParser.NOT, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FOPLParser.ExprContext)
            else:
                return self.getTypedRuleContext(FOPLParser.ExprContext,i)


        def quantor(self):
            return self.getTypedRuleContext(FOPLParser.QuantorContext,0)


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
            self.state = 29
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.PREDNAME]:
                self.state = 19
                self.predicate()
                pass
            elif token in [FOPLParser.NOT]:
                self.state = 20
                self.match(FOPLParser.NOT)
                self.state = 21
                self.expr(7)
                pass
            elif token in [FOPLParser.ALL_QUANTOR, FOPLParser.EX_QUANTOR]:
                self.state = 22
                self.quantor()
                self.state = 23
                self.expr(2)
                pass
            elif token in [FOPLParser.OPENCLAMP]:
                self.state = 25
                self.match(FOPLParser.OPENCLAMP)
                self.state = 26
                self.expr(0)
                self.state = 27
                self.match(FOPLParser.CLOSECLAMP)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 45
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 43
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 31
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 32
                        self.match(FOPLParser.AND)
                        self.state = 33
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 34
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 35
                        self.match(FOPLParser.OR)
                        self.state = 36
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 37
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 38
                        self.match(FOPLParser.IMPL)
                        self.state = 39
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = FOPLParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 40
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 41
                        self.match(FOPLParser.EQ)
                        self.state = 42
                        self.expr(4)
                        pass

             
                self.state = 47
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

        def terms(self):
            return self.getTypedRuleContext(FOPLParser.TermsContext,0)


        def CLOSECLAMP(self):
            return self.getToken(FOPLParser.CLOSECLAMP, 0)

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
            self.state = 48
            self.match(FOPLParser.PREDNAME)
            self.state = 49
            self.terms()
            self.state = 50
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
            self.state = 52
            _la = self._input.LA(1)
            if not(_la==FOPLParser.ALL_QUANTOR or _la==FOPLParser.EX_QUANTOR):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 53
            self.var()
            self.state = 54
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
            self.state = 56
            self.term()
            self.state = 57
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
            self.state = 64
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.COMMA]:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.match(FOPLParser.COMMA)
                self.state = 60
                self.term()
                self.state = 61
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
            self.state = 68
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.VARNAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.var()
                pass
            elif token in [FOPLParser.FUNCNAME]:
                self.enterOuterAlt(localctx, 2)
                self.state = 67
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
            self.state = 70
            self.match(FOPLParser.VARNAME)
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
        self.enterRule(localctx, 14, self.RULE_varlist)
        try:
            self.state = 77
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FOPLParser.COMMA]:
                self.enterOuterAlt(localctx, 1)
                self.state = 72
                self.match(FOPLParser.COMMA)
                self.state = 73
                self.var()
                self.state = 74
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

        def terms(self):
            return self.getTypedRuleContext(FOPLParser.TermsContext,0)


        def CLOSECLAMP(self):
            return self.getToken(FOPLParser.CLOSECLAMP, 0)

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
        self.enterRule(localctx, 16, self.RULE_func)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(FOPLParser.FUNCNAME)
            self.state = 80
            self.terms()
            self.state = 81
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
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         




