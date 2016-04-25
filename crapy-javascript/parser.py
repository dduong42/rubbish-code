import ply.lex as lex
import ply.yacc as yacc

from nodes import Assignation, Function, Name, String, Number, Boolean


reserved = {
    'var': 'VAR',
    'function': 'FUNCTION',
    'return': 'RETURN',
}



tokens = [
    'NUMBER', 'EQUALS', 'NAME', 'SEMICOLON', 'STRING', 'TRUE', 'FALSE',
    'LEFTPAR', 'RIGHTPAR', 'LEFTBRACE', 'RIGHTBRACE', 'COMMA',
] + list(reserved.values())


# Tokens
t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_LEFTBRACE = r'{'
t_RIGHTBRACE = r'}'
t_COMMA = r','
t_EQUALS = r'='
# TODO: Better name regex
t_SEMICOLON = r';'


def t_NUMBER(t):
    r'\d+'

    t.value = int(t.value)
    return t


def t_TRUE(t):
    r'true'
    t.value = True
    return t


def t_FALSE(t):
    r'false'
    t.value = False
    return t


def t_NAME(t):
    r'\w+'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_STRING(t):
    # TODO: Better string regex
    r'"\w+"'
    t.value = t.value[1:-1]
    return t


# Ignored characters
t_ignore = ' \t\n'


def t_error(t):
    print("Illegal character", t.value[0])
    t.lexer.skip(1)


# Parsing rules
def p_code_one(t):
    'code : statement'
    t[0] = [t[1]]

def p_code_multiple(t):
    'code : code statement'
    t[0] = t[1] + [t[2]]

def p_statement_assign(t):
    'statement : VAR NAME EQUALS expression SEMICOLON'
    variable_name = t[2]
    expression_result = t[4]
    t[0] = Assignation(variable_name, expression_result)


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = Number(t[1])


def p_expression_string(t):
    'expression : STRING'
    t[0] = String(t[1])


def p_expression_true(t):
    'expression : TRUE'
    t[0] = Boolean(t[1])


def p_expression_false(t):
    'expression : FALSE'
    t[0] = Boolean(t[1])


def p_expression_function(t):
    'expression : function'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    t[0] = Name(t[1])


def p_function(t):
    'function : FUNCTION function_arguments LEFTBRACE code return_statement RIGHTBRACE'
    t[0] = Function(t[2], t[4], t[5])


def p_function_void(t):
    'function : FUNCTION function_arguments LEFTBRACE code RIGHTBRACE'
    t[0] = Function(t[2], t[4])


def p_function_arguments(t):
    'function_arguments : LEFTPAR function_arguments_content RIGHTPAR'
    t[0] = t[2]


def p_function_arguments_content_empty(t):
    'function_arguments_content :'
    t[0] = []

def p_function_arguments_content_with_one(t):
    'function_arguments_content : function_arguments_content_filled'
    t[0] = t[1]


def p_function_arguments_content_filled(t):
    'function_arguments_content_filled : NAME'
    t[0] = [t[1]]


def p_function_arguments_content_many(t):
    'function_arguments_content_filled : function_arguments_content_filled COMMA NAME'
    t[0] = t[1] + [t[3]]


def p_return_statement(t):
    'return_statement : RETURN expression SEMICOLON'
    t[0] = t[2]


def p_error(t):
    print("Syntax error at", t.value)



def execute_code(statements, global_variables):
    for statement in statements:
        statement.execute(global_variables)


global_variables = {}
lexer = lex.lex()
parser = yacc.yacc()
p = parser.parse(
    '''
    var number = 1337;
    var string = "string";
    var bool_true = true;
    var bool_false = false;
    var my_func = function() {
        var local_var = 42;
        return 42;
    };
    var my_func2 = function() {
        var local_var = 42;
        var local_var2 = 43;
        return local_var;
    };
    ''')
execute_code(p, global_variables)
