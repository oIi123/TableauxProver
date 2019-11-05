grammar Propositional;

expr :
    Atom |
    NOT expr |
    expr AND expr |
    expr OR expr |
    expr IMPL expr |
    expr EQ expr |
    OPENCLAMP expr CLOSECLAMP;

Atom : [A-Za-z0-9]+;

OR : '|' | '+';
AND : '&' | '*';
IMPL : '->';
NOT : '!' | '-';
EQ : '<->';
OPENCLAMP : '(';
CLOSECLAMP : ')';

WS : [ \t\r\n] -> skip;
