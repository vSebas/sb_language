import sys
sys.path.append('C:/Users/visem/Documents/Carrera/Octavo_semestre/Lenguajes/Proyecto/Tercera_entrega/ply')
# sys.path.insert(0, "..")
import ply.lex as lex
import sys

tokens = [  'INTEGER', 'FLOAT', 'STRING', 'ID', #'FUNC_ID', "QUOT_MARKS",
            'EQUALS', 'IS_EQUAL', 'DIFFERENT', 'GT', 'LT', 'AND', 'OR' ,'NT',
            'PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'POWER',
            'LPAREN', 'RPAREN', 'COLON', 'SEMICOLON', 'COMA'  ]

reserved = [    'INT', 'FLT', 'BEGIN', 'FINISH', 'FUNC', 'RET',  'IF', 'NOT', 'WHILE', 
                'DO', 'FOR', 'UNTIL', 'END', 'JPTO', 'CALL', 'CRT', 'RD', 'SH' ]

tokens = tokens + reserved

t_EQUALS =  r'\='
t_IS_EQUAL =  r'\=\?'
t_DIFFERENT =  r'\=\/'
t_GT =  r'\>'
t_LT =  r'\<'
t_AND =  r'\&'
t_OR =  r'\#'
t_NT =  r'\!'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_TIMES = r'\*'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_COMA = r'\,'
# t_QUOT_MARKS= r'\"'
t_ignore = r' ' #ignore spaces

def t_COMMENT(t):
	r'\\.*'
	pass    # Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_FLOAT(t):
    r'\d+\.\d+'     #111111.2232
    t.value = float(t.value)# Convert string to float
    return t    # Return token object

def t_INTEGER(t):  
    r'\d+'          # 1...
    t.value = int(t.value)# Convert string to integer
    return t    # Return token object

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' # First character class is not a number
    if t.value.upper() in reserved: # Check for reserved tokens
        t.value = t.value.upper()
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t    # Return token object

# def t_FUNC_ID(t):
#     r'[a-zA-Z_][a-zA-Z_0-9]*' # First character class is not a number
#     if t.value.upper() in reserved: # Check for reserved tokens
#         t.value = t.value.upper()
#         t.type = t.value.upper()
#     else:
#         t.type = 'FUNC_ID'
#     return t    # Return token object

def t_STRING(t):
    r'"([^"\n]|(\\"))*"'
    # print(t.value)
    # t.value = (t.value).translate({ord('"'): None}) # Delete \"" from string
    # print(t.value)
    return t    # Return token object

def t_CRT(t):
    r'CRT'
    t.type = 'CRT'
    return t 

def t_RD(t):
    r'RD'
    t.type = 'RD'
    return t 

def t_SH(t):
    r'SH'
    t.type = 'SH'
    return t 

def t_FUNC(t):
    r'FUNC'
    t.type = 'FUNCTION'
    return t 

def t_INT(t):
    r'INT'
    t.type = 'INT'
    return t 

def t_FLT(t):
    r'FLT'
    t.type = 'FLT'
    return t 

def t_BEGIN(t):
    r'BEGIN'
    t.type = 'BEGIN'
    return t 

def t_FINISH(t):
    r'FINISH'
    t.type = 'FINISH'
    return t 

def t_CALL(t):
    r'CALL'
    t.type = 'CALL'
    return t 

def t_JPTO(t):
    r'JPTO'
    t.type = 'JPTO'
    return t 

def t_IF(t):
    r'IF'
    t.type = 'IF'
    return t 

def t_RET(t):
    r'RET'
    t.type = 'RET'
    return t 

def t_NOT(t):
    r'NOT'
    t.type = 'NOT'
    return t 

def t_WHILE(t):
    r'WHILE'
    t.type = 'WHILE'
    return t 

def t_FOR(t):
    r'FOR'
    t.type = 'FOR'
    return t 

def t_UNTIL(t):
    r'UNTIL'
    t.type = 'UNTIL'
    return t 

def t_END(t):
    r'END'
    t.type = 'END'
    return t 

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# lexer.input("\\abc=123.456")

# while True:
#     tok = lexer.token()
#     FOR not tok: 
#         break      # No more input
#     print(tok)