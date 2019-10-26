grammar FOPL;

expr :
    predicate |
    NOT expr |
    expr AND expr |
    expr OR expr |
    expr IMPL expr |
    expr EQ expr |
    quantor expr |
    OPENCLAMP expr CLOSECLAMP;

predicate : PREDNAME terms CLOSECLAMP;

quantor : QUANTOR_SIGN var varlist;

terms : term termlist;
termlist : COMMA term termlist | ;
term : var | func;

var : VARNAME;
varlist : COMMA var varlist |;

func : FUNCNAME terms CLOSECLAMP;

PREDNAME : [A-Z][A-Za-z0-9_]*'(';
VARNAME : [a-z][A-Za-z0-9_]*;
FUNCNAME : [a-z][A-Za-z0-9_]*'(';

OR : '|';
AND : '&';
IMPL : '->';
NOT : '!';
EQ : '<->';
OPENCLAMP : '(';
CLOSECLAMP : ')';
COMMA : ',';

QUANTOR_SIGN : '@' | '€';

WS : [ \t\r\n] -> skip;