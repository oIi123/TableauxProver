grammar FOPL;

expr :
    predicate |
    NOT expr |
    expr AND expr |
    expr OR expr |
    quantor expr |
    expr IMPL expr |
    expr EQ expr |
    OPENCLAMP expr CLOSECLAMP;

predicate : PREDNAME (terms |) CLOSECLAMP;

quantor : (ALL_QUANTOR | EX_QUANTOR) var varlist;

terms : term termlist;
termlist : COMMA term termlist | ;
term : var | func;

var : VARNAME;
varlist : COMMA var varlist |;

func : FUNCNAME (terms |) CLOSECLAMP;

PREDNAME : [A-Z][A-Za-z0-9_]*'(';
VARNAME : [a-z][A-Za-z0-9]*;
FUNCNAME : [a-z][A-Za-z0-9_]*'(';

OR : '|';
AND : '&';
IMPL : '->';
NOT : '!';
EQ : '<->';
OPENCLAMP : '(';
CLOSECLAMP : ')';
COMMA : ',';

ALL_QUANTOR : '(A)';
EX_QUANTOR : '(E)';

WS : [ \t\r\n] -> skip;