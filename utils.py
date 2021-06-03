from exceptions import SBLanguageExceptions
import math

class Program:
    def __init__(prog):
        # Constants found
        prog.constants=[]

        # Symbols found
        prog.symbols={}

        # Symbols as matrices
        prog.symbols_mat={}
        prog.symbols_mat_dim={}

        prog.temporal_avail={}

        # Generated quadruples in 'compilation'
        prog.quadruples=[[None, None, None, None]]

        # Procedures
        prog.procedures={}

        # Program counter
        prog.PC=0

        # Array to save interesting directions in PC
        prog.PCs=[]

        # Array to save jumps made in loops
        prog.loops_jp_to=[]

        # Eliminar siguientes:
        prog.symbols_type={}
        prog.symbols_mat_type={}

    def start_program(prog):
        prog.PC=0
        prog.quadruples[0][0] = "GOTO"  # First quadruple
        prog.quadruples[0][1] = 1       # Can go to the first position as PROCEDURES are located after the main program

    def end_program(prog):
        prog.quadruples.append(["ENDPROGRAM",None,None,None])

    def generate_procedure(prog, quad1):
        dir = len(prog.quadruples)
        prog.quadruples.append(["PROCEDURE",dir,None,None])
        prog.procedures[quad1] = dir
    
    def end_procedure(prog, quad1):
        prog.quadruples.append(["ENDPROCEDURE",None,None,None])

    def generate_if_then(prog, quad1):
        prog.quadruples.append(["GOTOf",quad1,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        # print(prog.quadruples)
        # print("Dirección GOTOf:",prog.loops_jp_to)
        
    def generate_if_else(prog, quad1):
        dir = prog.loops_jp_to.pop(0)
        prog.quadruples.append(["GOTO",None,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        prog.quadruples[dir][2] = len(prog.quadruples)
        # print(prog.quadruples)
        # print("Dirección GOTO:",prog.loops_jp_to)
        # print("Rellenar GOTOf:",prog.quadruples[dir][1])

    def generate_if_end(prog):
        dir = prog.loops_jp_to.pop(0)
        prog.quadruples[dir][1] = len(prog.quadruples)
        # print(prog.quadruples)
        # print("Rellenar GOTO:",prog.quadruples[dir][1])

    def generate_while_begin(prog,quad1):
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        prog.quadruples.append(["GOTOf",quad1,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)

    def generate_while_end(prog):
        dir = prog.loops_jp_to.pop(0)
        ret = prog.loops_jp_to.pop(0)
        prog.quadruples.append(["GOTO",ret,None,None])
        prog.quadruples[dir][2] = len(prog.quadruples)

    def generate_for_eval(prog, quad1):
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        prog.quadruples.append(["GOTOf",quad1,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)

    def generate_for_mod(prog):
        prog.quadruples.append(["GOTO",None,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        dir = prog.loops_jp_to.pop(2)
        ret = prog.loops_jp_to.pop(0)
        prog.quadruples.append(["GOTO",dir,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        prog.quadruples[ret][1] = len(prog.quadruples)

    def generate_for_end(prog):
        dir = prog.loops_jp_to.pop(0)
        ret = prog.loops_jp_to.pop(0)
        prog.quadruples.append(["GOTO",dir,None,None])
        prog.loops_jp_to.insert(0,len(prog.quadruples)-1)
        prog.quadruples[ret][2] = len(prog.quadruples)

    def generate_quadruple(prog,type,quad1,quad2,quad3=None,quad4=None):
        pos=len(prog.temporal_avail)
        prog.temporal_avail[f"T{pos}"]=None

        if (type == "MATH_EXP" or type == "LOG_EXP"):
            if quad3 is not None:
                prog.quadruples.append([quad2,quad1,quad3,f"T{pos}"])
            else:
                prog.quadruples.append([quad1,None,quad2,f"T{pos}"])
            return f"T{pos}"
        elif (type == "CALL"):
            prog.quadruples.append([quad1,quad2,None,None])
        elif (type == "RD" or type == "SH"):
            prog.quadruples.append([quad1,quad3,None,None])
        elif (type == "SIMPLE_ASSIGNMENT"):
            prog.quadruples.append([quad2,quad1,None,quad3])
        elif (type == "DIM_ASSIGNMENT"):
            dir = prog.ret_mat_dir(quad1,quad2)
            prog.quadruples.append([quad3,quad1,dir,quad4])
            
        return None
        
        # if quad4 is None: # There is a RD or SH instruction
        #     if quad3 is not None:
        #         if quad2 != "=":
        #             # print("{} {} {} {}".format(quad2,quad1,quad3,f"T{pos}"))
        #             '''
        #             if quad1 in prog.temporal_avail.keys():
        #                 del prog.temporal_avail[quad1]

        #             if quad3 in prog.temporal_avail.keys():
        #                 del prog.temporal_avail[quad3]
        #             '''
        #             prog.quadruples.append([quad2,quad1,quad3,f"T{pos}"])
        #             return f"T{pos}"
        #         else:
        #             # print("{} {} {}".format(quad2,quad1,quad3))
        #             '''
        #             if quad3[0] != "T":
        #                 del prog.temporal_avail[quad3]
        #             '''
        #             prog.quadruples.append([quad2,quad1,None,quad3])
        #     else:
        #         if quad1 == "CALL":
        #             # Se genera cuádruplo de un call a un procedure
        #             prog.quadruples.append([quad1,quad2,None,None])
        #         # elif quad1 == "IF":
        #         #     prog.quadruples.append([quad1,quad2,None,None])
        #         else:
        #             # expresiones estilo: not A, o -5
        #             # print("{} {} {} {}".format(quad2," ",quad2,f"T{pos}"))
        #             '''
        #             if quad1 in prog.temporal_avail.keys():
        #                 del prog.temporal_avail[quad1]

        #             if quad3 in prog.temporal_avail.keys():
        #                 del prog.temporal_avail[quad3]
        #             '''
        #             prog.quadruples.append([quad1,None,quad2,f"T{pos}"])
        #             return f"T{pos}"
        # else:
        #     if quad3 is not None: # There is a RD or SH instruction
        #         prog.quadruples.append([quad1,quad3,None,None])

        # return None

    def clean_temporal_avail(prog):
        prog.temporal_avail.clear()

    def check_intermediate_code(prog):
        print("Check:")
        for quadruple in prog.quadruples:
            print(quadruple[0], quadruple[1], quadruple[2], quadruple[3])

    def code_execution(prog):
        quad1_flag = ""
        quad2_flag = ""
        quad3_flag = ""
        jump = 0
        index = 0
        opcode = ""

        while(opcode != "ENDPROGRAM"):
            jump = 0
            quadruple = prog.quadruples[prog.PC]
            opcode = quadruple[0]
            # print(quadruple[0],quadruple[1],quadruple[2],quadruple[3])

            # print(quadruple[0])
            # print(quadruple[1])
            if quadruple[1] in prog.symbols.keys():
                quadruple1 =  prog.symbols[quadruple[1]]
                quad1_flag = "symbol"
            elif quadruple[1] in prog.symbols_mat.keys():
                if opcode != "SH":
                    quadruple1 = prog.symbols_mat[quadruple[1]][quadruple[2]]
                else:
                    quadruple1 = prog.symbols_mat[quadruple[1]]
                quad1_flag = "mat_symbol"
            elif quadruple[1] in prog.temporal_avail.keys():
                quadruple1 =  prog.temporal_avail[quadruple[1]]
                quad1_flag = "temporal"
            elif quadruple[1] in prog.procedures.keys():
                quadruple1 =  prog.procedures[quadruple[1]]
                quad1_flag = "procedure"
            elif quadruple[1] in prog.constants:
                index = prog.constants.index(quadruple[1])
                quadruple1 =  prog.constants[index]
                quad1_flag = "constant"
            
            # else:
            #     quad1_flag = ""

            if quadruple[2] is not None:
                if  quadruple[2] in prog.symbols.keys():
                    quadruple2 =  prog.symbols[quadruple[2]]
                    quad2_flag = "symbol"
                # elif quadruple[2] in prog.symbols_mat.keys():
                #     quadruple2 =  prog.symbols_mat[quadruple[2]][]
                #     quad2_flag = "mat_symbol"
                elif quadruple[2] in prog.temporal_avail.keys():
                    quadruple2 =  prog.temporal_avail[quadruple[2]]
                    quad2_flag = "temporal"
                elif quadruple[2] in prog.constants:
                    index = prog.constants.index(quadruple[2])
                    quadruple2 =  prog.constants[index]
                    quad2_flag = "constant"
                
                # else:
                #     quad2_flag = ""

            if quadruple[3] is not None:
                if   quadruple[3] in prog.symbols.keys():
                    quadruple3 =  prog.symbols[quadruple[3]]
                    quad3_flag = "symbol"
                elif quadruple[3] in prog.symbols_mat.keys():
                    quadruple3 =  prog.symbols_mat[quadruple[3]][quadruple[2]]
                    quad3_flag = "mat_symbol"
                elif quadruple[3] in prog.temporal_avail.keys():
                    quadruple3 =  prog.temporal_avail[quadruple[3]]
                    quad3_flag = "temporal"
                elif quadruple[3] in prog.constants:
                    index = prog.constants.index(quadruple[3])
                    quadruple3 =  prog.constants[index]
                    quad3_flag = "constant"
                # else:
                #     quad3_flag = ""


            if opcode == '+':
                quadruple3 = quadruple1 + quadruple2
            elif opcode == '-':
                if quadruple1 is not None:
                    quadruple3 = quadruple1 - quadruple2
                else:
                    quadruple3 = -quadruple2
            elif opcode == '*':
                quadruple3 = quadruple1 * quadruple2
            elif opcode == '/':
                quadruple3 = quadruple1 / quadruple2
            elif opcode == '^':
                quadruple3 = math.pow(quadruple1,quadruple2)
            elif opcode == '&': # AND
                quadruple3 = quadruple1 and quadruple2
            elif opcode == '#': # OR
                quadruple3 = quadruple1 or quadruple2
            elif opcode == '!': # NOT
                quadruple3 = not quadruple2
            elif opcode == '>':
                quadruple3 = quadruple1 > quadruple2
            elif opcode == '<':
                quadruple3 = quadruple1 < quadruple2
            elif opcode == '>=':
                quadruple3 = quadruple1 >= quadruple2
            elif opcode == '<=':
                quadruple3 = quadruple1 <= quadruple2
            elif opcode == '=?': # IS EQUAL?
                quadruple3 = quadruple1 == quadruple2
            elif opcode == '=/': # IS DIFFERENT?
                quadruple3 = quadruple1 != quadruple2
            elif opcode == '=':  # ASSIGN
                quadruple1 = quadruple3
                # print("=",quadruple1)
            elif opcode == "RD":
                quadruple1 = input("Input:")
                if "." in quadruple1:
                    quadruple1 = float(quadruple1)
                else:
                    quadruple1 = int(quadruple1)
                prog.constants.append(quadruple1)
            elif opcode == "SH":
                print(f"<{quadruple1}>")
            elif opcode == "CALL":
                # print("CALL")
                # print(quadruple1)
                prog.PCs.insert(0,prog.PC)  # Debo guardar el PC actual
                prog.PC = quadruple1 # Dirección del procedure
            elif opcode == "ENDPROCEDURE":
                # print("ENDPROC")
                prog.PC = prog.PCs.pop(0) # Devolver PC a donde estaba
            elif opcode == 'GOTO':
                prog.PC = quadruple[1]
                jump = 1
            elif opcode == 'GOTOf':
                # print(quadruple1)
                # print(quadruple2)
                if not quadruple1:
                    prog.PC = quadruple[2]
                    jump = 1
            elif opcode == 'ENDPROGRAM':
                print("Program finished")
                # prog.check_symbol_values()
                exit()

            # print(prog.PC)
            
            # print(quad1_flag,quad2_flag,quad3_flag)

            if (not jump):
                if quad3_flag == "temporal":
                    prog.temporal_avail[quadruple[3]] = quadruple3
                # else:
                #     prog.temporal_avail[quadruple[3]] = quadruple3

                if quad2_flag == "symbol":
                    prog.symbols[quadruple[2]] = quadruple2
                elif quad2_flag == "temporal":
                    prog.temporal_avail[quadruple[2]] = quadruple2

                if quad1_flag == "symbol":
                    prog.symbols[quadruple[1]] = quadruple1
                elif quad1_flag == "mat_symbol":
                    if opcode != "SH":
                        # print(quadruple1,quadruple2,quadruple3)
                        # print(prog.symbols_mat[quadruple[1]])
                        prog.symbols_mat[quadruple[1]][quadruple[2]] = quadruple1
                elif quad1_flag == "temporal":
                    prog.temporal_avail[quadruple[1]] = quadruple1

                prog.PC += 1

    def check_symbol_values(prog):
        for key in prog.symbols.keys():
            print(key, prog.symbols[key])

    def check_in_symbols(prog,val):
        if type(val) != int and type(val) != float:
            if val in prog.symbols.keys():
                # return prog.symbols[val]
                return val
            elif val in prog.symbols_mat.keys():
                # return prog.symbols_mat[val]
                return val
            else:
                raise SBLanguageExceptions(f'Undefined variable "{val}"!')
            return None
        else:
            prog.constants.append(val)
            return val
    
    # def oper_manager(prog,operand1,oper,operand2):
    #     if   oper == '+':
    #         return operand1 + operand2
    #     elif oper == '-':
    #         return operand1 - operand2
    #     elif oper == '*':
    #         return operand1 * operand2
    #     elif oper == '/':
    #         return operand1 / operand2
    #     elif oper == '^':
    #         return math.pow(operand1,operand2)

    def print_symbols(prog):
        # Dictionaries are unordered, but who cares
        i=0
        for symbol in prog.symbols_type:
            print(i,symbol,prog.symbols_type[symbol])
            i+=1
    
    def create_symbol(prog,data_type,symbol,assignment=None):
        if data_type != "INT" and data_type != "FLT":
            print("Invalid datatype!")
        else:
            if symbol not in prog.symbols:
                prog.symbols[symbol] = None
                prog.symbols_type[symbol] = data_type
                prog.symbols[symbol] = assignment
            else:
                print(f"ERROR: Already existent variable! --> {symbol}")
    
    def check_symbol_dim(prog,dim):
        # if dim2 is not None:
        #     if dim3 is not None:
        #         return dim1,dim2,dim3
        #     return dim1,dim2
        # return dim1

        if len(dim) == 4:
            return dim[2]
        elif len(dim) == 6:
            return dim[2],dim[4]
        elif len(dim) == 8:
            return dim[2],dim[4],dim[6]

    def create_symbol_mat(prog,data_type,symbol,dim):
        size = 0
        if type(dim) != int:
            size = len(dim)
        dim1 = 0
        dim2 = 0
        dim3 = 0
        dims = []
        base = []

        if size == 3:
            dim1,dim2,dim3 = dim
            prog.symbols_mat[symbol] =  [None]*dim1*dim2*dim3 #  [None]*(dim1*dim2*dim3)
            dims = [dim2*dim3,dim3]
            base = [0,0,0]
        elif size == 2:
            dim1,dim2 = dim
            base = [0,0]
            dims = [dim2]
            prog.symbols_mat[symbol] = [None]*dim1*dim2  # [None]*(dim1*dim2)
        else:
            dim1 = dim
            base = [0]
            dims = [1]
            prog.symbols_mat[symbol] = [None]*dim

        prog.symbols_mat_dim[symbol] = [dims,base]

        # print(prog.symbols_mat[symbol])
        # print(prog.symbols_mat_dim[symbol])
    
    def ret_mat_dir(prog,symbol,dim):
        size = 0
        x = 0
        y = None
        z = None

        if type(dim) != int:
            size = len(dim)

        if size == 3:
            x,y,z = dim
        elif size == 2:
            x,y = dim
        else:
            x = dim

        # print(x,y,z)

        if y != None:
            if z != None:
                # print(symbol)
                # print(prog.symbols_mat_dim)
                d1 = prog.symbols_mat_dim[symbol][0][0]
                d2 = prog.symbols_mat_dim[symbol][0][1]
                dir = x*d1 + y*d2 + z + 0
                # print(d1)
                # print(d2)
                # print(dir)
                return dir

            d1 = prog.symbols_mat_dim[symbol][0][0]
            dir = x*d1 + y + 0
            # print(d1)
            # print(dir)
            return dir

        d1 = prog.symbols_mat_dim[symbol][0][0]
        dir = x*d1 + 0
        # print(d1)
        # print(dir)
        return dir


    # def create_symbol_mat(prog,data_type,symbol,mat,assignment=None):
    #     if data_type != "INT" and data_type != "FLT":
    #         print("Invalid datatype!")
    #     else:
    #         if symbol not in prog.symbols_mat:
    #             prog.symbols_mat[symbol] = None
    #             prog.symbols_mat_type[symbol] = data_type
    #         # print(type(mat))
    #         if type(mat) is tuple:
    #             if len(mat) == 2:
    #                 rows, cols = mat
    #                 prog.symbols_mat[symbol] = [[None]*rows]*cols
    #                 # print(prog.symbols_kmat[symbol])
    #             elif len(mat) == 3:
    #                 rows, cols, dim = mat
    #                 prog.symbols_mat[symbol] = [[[None]*rows]*cols]*dim
    #                 # print(prog.symbols_mat[symbol])
    #         else:
    #             rows = mat
    #             prog.symbols_mat[symbol] = [None]*rows
    #             # print(prog.symbols_mat[symbol])

    #         # prog.symbols_mat[symbol] = assignment

    # def check_symbol_dim(prog,dim):
    #     if len(dim) == 4:
    #         return dim[2]
    #     elif len(dim) == 6:
    #         return dim[2], dim[4]
    #     elif len(dim) == 8:
    #         return dim[2], dim[4], dim[6]

    # def ret_mat_value(prog,val,m):
    #     rows = 0
    #     cols = 0
    #     extra_dim = 0

    #     # Check dimension of desired matrix
    #     if val in prog.symbols_mat:
    #         for n_dim_elem in prog.symbols_mat[val]:
    #             if type(n_dim_elem) == list:
    #                 rows = len(n_dim_elem)-1
    #                 for two_dim_elem in n_dim_elem:
    #                     if type(two_dim_elem) == list:
    #                         cols = len(two_dim_elem)-1
    #                         for elem in two_dim_elem:
    #                             if type(elem) == list:
    #                                 extra_dim = len(elem)-1

    #         # print(type(m))
    #         if type(m) is tuple:
    #             if len(m) == 2:
    #                 d_rows, d_cols = m
    #             elif len(m) == 3:
    #                 d_rows, d_cols, d_extra_dim = m
    #         else:
    #             d_rows = m

    #         if d_rows <= rows:
    #             return prog.symbols_mat[val][d_rows]
    #         elif d_cols <= cols:
    #             return prog.symbols_mat[val][d_rows][d_cols]
    #         elif d_extra_dim <= extra_dim:
    #             return prog.symbols_mat[val][d_rows][d_cols][d_extra_dim]
    #         else:
    #             print("Index error!")
    #     else:
    #         print("Undefined variable!")


    # def update_symbol(prog,symbol,value):
    #     if symbol in prog.symbols:
    #         prog.symbols[symbol] = value
    #     elif symbol in prog.symbols_mat:
    #         prog.symbols_mat[symbol] = value
    #     else:
    #         print("Undefined variable!")

    # def id_assignment(prog,symbol,assignment=None):
    #     if symbol in prog.symbols:
    #         prog.symbols[symbol] = assignment
    #     else:
    #         print("Undefined variable!")

    # def id_mat_assignment(prog,symbol,mat,assignment=None):
    #     # count = sum( [ len(listElem) for listElem in listOfElems2D])
    #     rows = 0
    #     cols = 0
    #     extra_dim = 0

    #     # Check dimension of desired matrix
    #     if symbol in prog.symbols_mat:
    #         for n_dim_elem in prog.symbols_mat[symbol]:
    #             if type(n_dim_elem) == list:
    #                 rows = len(n_dim_elem)-1
    #                 for two_dim_elem in n_dim_elem:
    #                     if type(two_dim_elem) == list:
    #                         cols = len(two_dim_elem)-1
    #                         for elem in two_dim_elem:
    #                             if type(elem) == list:
    #                                 extra_dim = len(elem)-1
            
    #         if type(mat) is tuple:
    #             if len(mat) == 2:
    #                 d_rows, d_cols = mat
    #             elif len(mat) == 3:
    #                 d_rows, d_cols, d_extra_dim = mat
    #         else:
    #             d_rows = mat

    #         if d_rows <= rows:
    #             prog.symbols_mat[symbol][d_rows] = assignment
    #         elif d_cols <= cols:
    #             prog.symbols_mat[symbol][d_rows][d_cols] = assignment
    #         elif d_extra_dim <= extra_dim:
    #             prog.symbols_mat[symbol][d_rows][d_cols][d_extra_dim] = assignment
    #         else:
    #             print("Index error!")
    #     else:
    #         print("Undefined variable!")
    #         return None

    # def ret_value(prog,val):
    #     if type(val) != int and type(val) != float:
    #         if val in prog.symbols:
    #             return prog.symbols[val]
    #         elif val in prog.symbols_mat:
    #             return prog.symbols_mat[val]
    #         else:
    #             print("Undefined variable!")
    #     else:
    #         return val