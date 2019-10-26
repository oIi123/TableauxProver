# Generated from D:/Studium/7_Studienarbeit/Impl/src/Parser\Propositional.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\13")
        buf.write(" \4\2\t\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2\r\n\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2\33")
        buf.write("\n\2\f\2\16\2\36\13\2\3\2\2\3\2\3\2\2\2\2$\2\f\3\2\2\2")
        buf.write("\4\5\b\2\1\2\5\r\7\3\2\2\6\7\7\7\2\2\7\r\5\2\2\b\b\t\7")
        buf.write("\t\2\2\t\n\5\2\2\2\n\13\7\n\2\2\13\r\3\2\2\2\f\4\3\2\2")
        buf.write("\2\f\6\3\2\2\2\f\b\3\2\2\2\r\34\3\2\2\2\16\17\f\7\2\2")
        buf.write("\17\20\7\5\2\2\20\33\5\2\2\b\21\22\f\6\2\2\22\23\7\4\2")
        buf.write("\2\23\33\5\2\2\7\24\25\f\5\2\2\25\26\7\6\2\2\26\33\5\2")
        buf.write("\2\6\27\30\f\4\2\2\30\31\7\b\2\2\31\33\5\2\2\5\32\16\3")
        buf.write("\2\2\2\32\21\3\2\2\2\32\24\3\2\2\2\32\27\3\2\2\2\33\36")
        buf.write("\3\2\2\2\34\32\3\2\2\2\34\35\3\2\2\2\35\3\3\2\2\2\36\34")
        buf.write("\3\2\2\2\5\f\32\34")
        return buf.getvalue()


class PropositionalParser ( Parser ):

    grammarFileName = "Propositional.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'|'", "'&'", "'->'", "'!'", 
                     "'<->'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "Atom", "OR", "AND", "IMPL", "NOT", "EQ", 
                      "OPENCLAMP", "CLOSECLAMP", "WS" ]

    RULE_expr = 0

    ruleNames =  [ "expr" ]

    EOF = Token.EOF
    Atom=1
    OR=2
    AND=3
    IMPL=4
    NOT=5
    EQ=6
    OPENCLAMP=7
    CLOSECLAMP=8
    WS=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom(self):
            return self.getToken(PropositionalParser.Atom, 0)

        def NOT(self):
            return self.getToken(PropositionalParser.NOT, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PropositionalParser.ExprContext)
            else:
                return self.getTypedRuleContext(PropositionalParser.ExprContext,i)


        def OPENCLAMP(self):
            return self.getToken(PropositionalParser.OPENCLAMP, 0)

        def CLOSECLAMP(self):
            return self.getToken(PropositionalParser.CLOSECLAMP, 0)

        def AND(self):
            return self.getToken(PropositionalParser.AND, 0)

        def OR(self):
            return self.getToken(PropositionalParser.OR, 0)

        def IMPL(self):
            return self.getToken(PropositionalParser.IMPL, 0)

        def EQ(self):
            return self.getToken(PropositionalParser.EQ, 0)

        def getRuleIndex(self):
            return PropositionalParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = PropositionalParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [PropositionalParser.Atom]:
                self.state = 3
                self.match(PropositionalParser.Atom)
                pass
            elif token in [PropositionalParser.NOT]:
                self.state = 4
                self.match(PropositionalParser.NOT)
                self.state = 5
                self.expr(6)
                pass
            elif token in [PropositionalParser.OPENCLAMP]:
                self.state = 6
                self.match(PropositionalParser.OPENCLAMP)
                self.state = 7
                self.expr(0)
                self.state = 8
                self.match(PropositionalParser.CLOSECLAMP)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 26
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 24
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = PropositionalParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 12
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 13
                        self.match(PropositionalParser.AND)
                        self.state = 14
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = PropositionalParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 15
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 16
                        self.match(PropositionalParser.OR)
                        self.state = 17
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = PropositionalParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 18
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 19
                        self.match(PropositionalParser.IMPL)
                        self.state = 20
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = PropositionalParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 21
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 22
                        self.match(PropositionalParser.EQ)
                        self.state = 23
                        self.expr(3)
                        pass

             
                self.state = 28
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
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
         




