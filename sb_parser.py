# import ply.parser as parser
import sb_lexer
import math
import ply.yacc as yacc
from utils import *

debug=True
tokens = sb_lexer.tokens

program = Program()
program.symbols = {}
program.symbols_mat = {}

precedence = (
    ('nonassoc', 'LT', 'GT','LTE', 'GTE'),  # Nonassociative operators
    ('left','AND','OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)

def p_program(p):
    '''
    program : BEG body FIN routine
    '''

def p_program_begin(p):
    '''
    BEG : BEGIN
    '''
    program.start_program()

def p_program_finish(p):
    '''
    FIN : FINISH
    '''
    program.end_program()
    # program.check_intermediate_code()
    program.code_execution()

def p_routine(p):
    '''
    routine  : routine FUNC ID COLON body RET
             | empty
    '''

def p_body(p):
    '''
    body  : body st SEMICOLON
          | body cond
          | empty
    '''

# STATEMENTS
def p_st(p):
    '''
    st : CALL ID
        | JPTO ID
    '''

def p_st_read_val(p):
    '''
    st : RD LT ID GT
    '''
    # program.update_symbol(p[3],p[5])
    p[0] = program.generate_quadruple(p[1], p[2], p[3], p[4])

def p_st_show_val(p):
    '''
    st : SH LT ID GT
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3], p[4])
    # print(p[3])

# def p_st_show_str(p):
#     '''
#     st : SH LT STRING GT
#     '''
#     p[0] = program.generate_quadruple(p[1], p[2], p[3], p[4])
#     # print(p[3])

def p_st_id_declare(p):
    '''
    st : CRT data_type ID
    '''
    program.create_symbol(p[2],p[3])

def p_st_mat(p):
    '''
    st : CRT data_type ID m
    '''
    program.create_symbol_mat(p[2],p[3],p[4])

def p_m(p):
    '''
    m : LPAREN val RPAREN
      | LPAREN val COMA val RPAREN
      | LPAREN val COMA val COMA val RPAREN
    '''
    p[0] = program.check_symbol_dim(p)

# def p_log_math_exp(p):
#     '''
#     st : log_exp
#        | math_exp
#     '''
#     program.clean_temporal_avail()

def p_st_asmnt(p):
    '''
    st : assignment
       | mat_assignment
    '''
    # program.clean_temporal_avail()

def p_assignment(p):
    '''
    assignment : ID EQUALS ID
               | ID EQUALS log_exp
               | ID EQUALS math_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])

def p_mat_assignment(p):
    '''
    mat_assignment : ID m EQUALS ID
                   | ID m EQUALS log_exp
                   | ID m EQUALS math_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])

    # p[0] = program.id_mat_assignment(p[1],p[2],p[3])

# CONDITIONALS
# def p_cond(p):
#     '''
#     cond : IF LPAREN log_exp RPAREN body ent END
#          | WHILE LPAREN log_exp RPAREN body END
#          | DO body UNTIL LPAREN log_exp RPAREN END
#          | FOR LPAREN log_exp COMA math_exp RPAREN body END
#     ent  : NOT body
#          | empty
#     '''

def p_cond_if(p):
    '''
    cond : IF LPAREN log_exp RPAREN COLON body NOT body END
         | IF LPAREN log_exp RPAREN COLON body END
    '''
    print(p[3])
    if p[3]:
        p[0] = p[6]
    else:
        if len(p) >8:
            p[0] = p[8]

def p_cond_while(p):
    '''
    cond : WHILE LPAREN log_exp RPAREN COLON body END
    '''

def p_cond_do(p):
    '''
    cond : DO COLON body UNTIL LPAREN log_exp RPAREN END
    '''

def p_cond_for(p):
    '''
    cond : FOR LPAREN log_exp COMA assignment RPAREN COLON body END
    '''

# # Logical expressions
def p_log_exp_is_eq(p):
    '''
    log_exp : log_exp IS_EQUAL log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])
    # p[0] = p[1] == p[3]

def p_log_exp_neq(p):
    '''
    log_exp : log_exp DIFFERENT log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])
    # p[0] = p[1] != p[3]

def p_log_gt(p):
    '''
    log_exp : log_exp GT log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])
    # p[0] = p[1] > p[3]

def p_log_lt(p):
    '''
    log_exp : log_exp LT log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])
    # if p[1] is not None and p[2] is not None:
        # p[0] = p[1] < p[3]

def p_log_gte(p):
    '''
    log_exp : log_exp GTE log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])

def p_log_lte(p):
    '''
    log_exp : log_exp LTE log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])

def p_log_and(p):
    '''
    log_exp : log_exp AND log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])
    # p[0] = p[1] and p[3]

def p_log_or(p):
    '''
    log_exp : log_exp OR log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2], p[3])
    # p[0] = p[1] or p[3]

def p_log_not(p):
    '''
    log_exp : NT log_exp
    '''
    p[0] = program.generate_quadruple(p[1], p[2])
    # p[0] = not p[2]

def p_log_par(p):
    '''
    log_exp : LPAREN log_exp RPAREN
    '''
    p[0] = p[2]

def p_log_val(p):
    '''
    log_exp : val
    '''
    p[0] = p[1]

# # Mathematical expressions
def p_math_exp_plus(p):
    '''
    math_exp : math_exp PLUS math_exp
    '''
    p[0] = program.generate_quadruple(p[1],p[2],p[3])
    #p[0] = program.oper_manager(p[1],p[2],p[3])

def p_math_exp_minus(p):
    '''
    math_exp : math_exp MINUS math_exp
    '''
    p[0] = program.generate_quadruple(p[1],p[2],p[3])
    #p[0] = program.oper_manager(p[1],p[2],p[3])

def p_math_exp_times(p):
    '''
    math_exp : math_exp TIMES math_exp
    '''
    p[0] = program.generate_quadruple(p[1],p[2],p[3])
    #p[0] = program.oper_manager(p[1],p[2],p[3])

def p_math_exp_divide(p):
    '''
    math_exp : math_exp DIVIDE math_exp
    '''
    p[0] = program.generate_quadruple(p[1],p[2],p[3])
    #p[0] = program.oper_manager(p[1],p[2],p[3])

def p_math_exp_power(p):
    '''
    math_exp : math_exp POWER math_exp
    '''
    p[0] = program.generate_quadruple(p[1],p[2],p[3])
    #p[0] = program.oper_manager(p[1],p[2],p[3])

def p_math_exp_uminus(p):
    'math_exp : MINUS val %prec UMINUS'
    p[0] = program.generate_quadruple(p[1],p[2])
    # p[0] = program.oper_manager(0,p[2],p[3])

def p_math_par(p):
    '''
    math_exp : LPAREN math_exp RPAREN
    '''
    p[0] = p[2]

def p_math_exp_val(p):
    '''
    math_exp : val
    '''
    p[0] = p[1]

def p_data_type(p):
    # To declare variables
    '''
    data_type : INT
              | FLT
    '''
    p[0] = p[1]

def p_val(p):
    # For assignments
    '''
    val : ID
        | FLOAT
        | INTEGER
    '''
    # p[0] = program.ret_value(p[1])
    # p[0] = p[1]
    p[0] = program.check_in_symbols(p[1])

def p_val_mat(p):
    # For assignments
    '''
    val : ID m
    '''
    p[0] = program.ret_mat_value(p[1],p[2])

####

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("Syntax error found")
    print(p)
    # if not p:
    #     print("SYNTAX ERROR AT EOF")

parser = yacc.yacc()

try:
    with open("C:/Users/visem/Documents/Carrera/Octavo_semestre/Lenguajes/Proyecto/ply/project/tests/program_execution/test.txt",  encoding="utf8") as f:
        file = f.read()
    parser.parse(file)
    # program.print_symbols()
except EOFError:
    pass