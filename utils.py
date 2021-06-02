from exceptions import SBLanguageExceptions
import math

class Program:
    def __init__(self):
        # Constants found
        self.constants=[]

        # Symbols found
        self.symbols={}

        # Symbols as matrices
        self.symbols_mat={}

        self.temporal_avail={}

        # Generated quadruples in 'compilation'
        self.quadruples=[[None, None, None, None]]

        # Procedures
        self.procedures={}

        # Program counter
        self.PC=0

        # Array to save interesting directions in PC
        self.PCs=[]

        # Array to save jumps made in loops
        self.loops_jp_to=[]

        # Eliminar siguientes:
        self.symbols_type={}
        self.symbols_mat_type={}

    def start_program(self):
        self.PC=0
        self.quadruples[0][0] = "GOTO"  # First quadruple
        self.quadruples[0][1] = 1       # Can go to the first position as PROCEDURES are located after the main program

    def end_program(self):
        self.quadruples.append(["ENDPROGRAM",None,None,None])

    def generate_procedure(self, quad1):
        dir = len(self.quadruples)
        self.quadruples.append(["PROCEDURE",dir,None,None])
        self.procedures[quad1] = dir
    
    def end_procedure(self, quad1):
        self.quadruples.append(["ENDPROCEDURE",None,None,None])

    def generate_if_then(self, quad1):
        self.quadruples.append(["GOTOf",quad1,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        # print(self.quadruples)
        # print("Dirección GOTOf:",self.loops_jp_to)
        
    def generate_if_else(self, quad1):
        dir = self.loops_jp_to.pop(0)
        self.quadruples.append(["GOTO",None,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        self.quadruples[dir][2] = len(self.quadruples)
        # print(self.quadruples)
        # print("Dirección GOTO:",self.loops_jp_to)
        # print("Rellenar GOTOf:",self.quadruples[dir][1])

    def generate_if_end(self):
        dir = self.loops_jp_to.pop(0)
        self.quadruples[dir][1] = len(self.quadruples)
        # print(self.quadruples)
        # print("Rellenar GOTO:",self.quadruples[dir][1])

    def generate_while_begin(self,quad1):
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        self.quadruples.append(["GOTOf",quad1,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)

    def generate_while_end(self):
        dir = self.loops_jp_to.pop(0)
        ret = self.loops_jp_to.pop(0)
        self.quadruples.append(["GOTO",ret,None,None])
        self.quadruples[dir][2] = len(self.quadruples)

    def generate_for_eval(self, quad1):
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        self.quadruples.append(["GOTOf",quad1,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)

    def generate_for_mod(self):
        self.quadruples.append(["GOTO",None,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        dir = self.loops_jp_to.pop(2)
        ret = self.loops_jp_to.pop(0)
        self.quadruples.append(["GOTO",dir,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        self.quadruples[ret][1] = len(self.quadruples)

    def generate_for_end(self):
        dir = self.loops_jp_to.pop(0)
        ret = self.loops_jp_to.pop(0)
        self.quadruples.append(["GOTO",dir,None,None])
        self.loops_jp_to.insert(0,len(self.quadruples)-1)
        self.quadruples[ret][2] = len(self.quadruples)

    def generate_quadruple(self,quad1,quad2,quad3=None,quad4=None):
        pos=len(self.temporal_avail)
        self.temporal_avail[f"T{pos}"]=None
        if quad4 is None: # There is a RD or SH instruction
            if quad3 is not None:
                if quad2 != "=":
                    # print("{} {} {} {}".format(quad2,quad1,quad3,f"T{pos}"))
                    '''
                    if quad1 in self.temporal_avail.keys():
                        del self.temporal_avail[quad1]

                    if quad3 in self.temporal_avail.keys():
                        del self.temporal_avail[quad3]
                    '''
                    self.quadruples.append([quad2,quad1,quad3,f"T{pos}"])
                    return f"T{pos}"
                else:
                    # print("{} {} {}".format(quad2,quad1,quad3))
                    '''
                    if quad3[0] != "T":
                        del self.temporal_avail[quad3]
                    '''
                    self.quadruples.append([quad2,quad1,None,quad3])
            else:
                if quad1 == "CALL":
                    # Se genera cuádruplo de un call a un procedure
                    self.quadruples.append([quad1,quad2,None,None])
                # elif quad1 == "IF":
                #     self.quadruples.append([quad1,quad2,None,None])
                else:
                    # expresiones estilo: not A, o -5
                    # print("{} {} {} {}".format(quad2," ",quad2,f"T{pos}"))
                    '''
                    if quad1 in self.temporal_avail.keys():
                        del self.temporal_avail[quad1]

                    if quad3 in self.temporal_avail.keys():
                        del self.temporal_avail[quad3]
                    '''
                    self.quadruples.append([quad1,None,quad2,f"T{pos}"])
                    return f"T{pos}"
        else:
            if quad3 is not None: # There is a RD or SH instruction
                self.quadruples.append([quad1,quad3,None,None])

        return None

    def clean_temporal_avail(self):
        self.temporal_avail.clear()

    def check_intermediate_code(self):
        print("Check:")
        for quadruple in self.quadruples:
            print(quadruple[0], quadruple[1], quadruple[2], quadruple[3])

    def code_execution(self):
        quad1_flag = ""
        quad2_flag = ""
        quad3_flag = ""
        jump = 0
        index = 0

        while(True):
            jump = 0
            quadruple = self.quadruples[self.PC]
            opcode = quadruple[0]
            print(quadruple[0],quadruple[1],quadruple[2],quadruple[3])

            # print(quadruple[0])
            # print(quadruple[1])
            if   quadruple[1] in self.symbols.keys():
                quadruple1 =  self.symbols[quadruple[1]]
                quad1_flag = "symbol"
                print("SYM")
            elif quadruple[1] in self.temporal_avail.keys():
                quadruple1 =  self.temporal_avail[quadruple[1]]
                quad1_flag = "temporal"
                print("TEMP")
            elif quadruple[1] in self.procedures.keys():
                quadruple1 =  self.procedures[quadruple[1]]
                quad1_flag = "procedure"
                print("PROCC")
            elif quadruple[1] in self.constants:
                index = self.constants.index(quadruple[1])
                quadruple1 =  self.constants[index]
                quad1_flag = "constant"
                print("CONS")
            print(quadruple1)
            
            # else:
            #     quad1_flag = ""

            if quadruple[2] is not None:
                if   quadruple[2] in self.symbols.keys():
                    quadruple2 =  self.symbols[quadruple[2]]
                    quad2_flag = "symbol"
                elif quadruple[2] in self.temporal_avail.keys():
                    quadruple2 =  self.temporal_avail[quadruple[2]]
                    quad2_flag = "temporal"
                elif quadruple[2] in self.constants:
                    index = self.constants.index(quadruple[2])
                    quadruple2 =  self.constants[index]
                    quad2_flag = "constant"
                print(quadruple2)
                
                # else:
                #     quad2_flag = ""

            if quadruple[3] is not None:
                if   quadruple[3] in self.symbols.keys():
                    quadruple3 =  self.symbols[quadruple[3]]
                    quad3_flag = "symbol"
                elif quadruple[3] in self.temporal_avail.keys():
                    quadruple3 =  self.temporal_avail[quadruple[3]]
                    quad3_flag = "temporal"
                elif quadruple[3] in self.constants:
                    index = self.constants.index(quadruple[3])
                    quadruple3 =  self.constants[index]
                    quad3_flag = "constant"
                print(quadruple3)
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
                print(quadruple3)
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
                # print(quadruple2)
            elif opcode == "RD":
                quadruple1 = input("Input:")
                if "." in quadruple1:
                    quadruple1 = float(quadruple1)
                else:
                    quadruple1 = int(quadruple1)
                self.constants.append(quadruple1)
            elif opcode == "SH":
                print(f"<{quadruple1}>")
            elif opcode == "CALL":
                # print("CALL")
                # print(quadruple1)
                self.PCs.insert(0,self.PC)  # Debo guardar el PC actual
                self.PC = quadruple1 # Dirección del procedure
            elif opcode == "ENDPROCEDURE":
                # print("ENDPROC")
                self.PC = self.PCs.pop(0) # Devolver PC a donde estaba
            elif opcode == 'GOTO':
                self.PC = quadruple[1]
                jump = 1
            elif opcode == 'GOTOf':
                # print(quadruple1)
                # print(quadruple2)
                if not quadruple1:
                    self.PC = quadruple[2]
                    jump = 1
            elif opcode == 'ENDPROGRAM':
                print("Program finished")
                # self.check_symbol_values()
                exit()

            # print(self.PC)
            
            if (not jump):
                if quad3_flag == "symbol":
                    self.symbols[quadruple[3]] = quadruple3
                # else:
                #     self.temporal_avail[quadruple[3]] = quadruple3

                if quad2_flag == "symbol":
                    self.symbols[quadruple[2]] = quadruple2
                elif quad2_flag == "temporal":
                    self.temporal_avail[quadruple[2]] = quadruple2

                if quad1_flag == "symbol":
                    self.symbols[quadruple[1]] = quadruple1
                elif quad1_flag == "temporal":
                    self.temporal_avail[quadruple[1]] = quadruple1

                self.PC += 1

    def check_symbol_values(self):
        for key in self.symbols.keys():
            print(key, self.symbols[key])

    def check_in_symbols(self,val):
        if type(val) != int and type(val) != float:
            if val in self.symbols.keys():
                # return self.symbols[val]
                return val
            elif val in self.symbols_mat.keys():
                # return self.symbols_mat[val]
                return val
            else:
                raise SBLanguageExceptions(f'Undefined variable "{val}"!')
            return None
        else:
            self.constants.append(val)
            return val
    
    # def oper_manager(self,operand1,oper,operand2):
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

    def print_symbols(self):
        # Dictionaries are unordered, but who cares
        i=0
        for symbol in self.symbols_type:
            print(i,symbol,self.symbols_type[symbol])
            i+=1

    def update_symbol(self,symbol,value):
        if symbol in self.symbols:
            self.symbols[symbol] = value
        elif symbol in self.symbols_mat:
            self.symbols_mat[symbol] = value
        else:
            print("Undefined variable!")
    
    def create_symbol(self,data_type,symbol,assignment=None):
        if data_type != "INT" and data_type != "FLT":
            print("Invalid datatype!")
        else:
            if symbol not in self.symbols:
                self.symbols[symbol] = None
                self.symbols_type[symbol] = data_type
                self.symbols[symbol] = assignment
            else:
                print(f"ERROR: Already existent variable! --> {symbol}")

    def create_symbol_mat(self,data_type,symbol,mat,assignment=None):
        if data_type != "INT" and data_type != "FLT":
            print("Invalid datatype!")
        else:
            if symbol not in self.symbols_mat:
                self.symbols_mat[symbol] = None
                self.symbols_mat_type[symbol] = data_type
            # print(type(mat))
            if type(mat) is tuple:
                if len(mat) == 2:
                    rows, cols = mat
                    self.symbols_mat[symbol] = [[None]*rows]*cols
                    # print(self.symbols_kmat[symbol])
                elif len(mat) == 3:
                    rows, cols, dim = mat
                    self.symbols_mat[symbol] = [[[None]*rows]*cols]*dim
                    # print(self.symbols_mat[symbol])
            else:
                rows = mat
                self.symbols_mat[symbol] = [None]*rows
                # print(self.symbols_mat[symbol])

            # self.symbols_mat[symbol] = assignment

    def check_symbol_dim(self,dim):
        if len(dim) == 4:
            return dim[2]
        elif len(dim) == 6:
            return dim[2], dim[4]
        elif len(dim) == 8:
            return dim[2], dim[4], dim[6]

    def id_assignment(self,symbol,assignment=None):
        if symbol in self.symbols:
            self.symbols[symbol] = assignment
        else:
            print("Undefined variable!")

    def id_mat_assignment(self,symbol,mat,assignment=None):
        # count = sum( [ len(listElem) for listElem in listOfElems2D])
        rows = 0
        cols = 0
        extra_dim = 0

        # Check dimension of desired matrix
        if symbol in self.symbols_mat:
            for n_dim_elem in self.symbols_mat[symbol]:
                if type(n_dim_elem) == list:
                    rows = len(n_dim_elem)-1
                    for two_dim_elem in n_dim_elem:
                        if type(two_dim_elem) == list:
                            cols = len(two_dim_elem)-1
                            for elem in two_dim_elem:
                                if type(elem) == list:
                                    extra_dim = len(elem)-1
            
            if type(mat) is tuple:
                if len(mat) == 2:
                    d_rows, d_cols = mat
                elif len(mat) == 3:
                    d_rows, d_cols, d_extra_dim = mat
            else:
                d_rows = mat

            if d_rows <= rows:
                self.symbols_mat[symbol][d_rows] = assignment
            elif d_cols <= cols:
                self.symbols_mat[symbol][d_rows][d_cols] = assignment
            elif d_extra_dim <= extra_dim:
                self.symbols_mat[symbol][d_rows][d_cols][d_extra_dim] = assignment
            else:
                print("Index error!")
        else:
            print("Undefined variable!")
            return None

    def ret_value(self,val):
        if type(val) != int and type(val) != float:
            if val in self.symbols:
                return self.symbols[val]
            elif val in self.symbols_mat:
                return self.symbols_mat[val]
            else:
                print("Undefined variable!")
        else:
            return val
        
    def ret_mat_value(self,val,m):
        rows = 0
        cols = 0
        extra_dim = 0

        # Check dimension of desired matrix
        if val in self.symbols_mat:
            for n_dim_elem in self.symbols_mat[val]:
                if type(n_dim_elem) == list:
                    rows = len(n_dim_elem)-1
                    for two_dim_elem in n_dim_elem:
                        if type(two_dim_elem) == list:
                            cols = len(two_dim_elem)-1
                            for elem in two_dim_elem:
                                if type(elem) == list:
                                    extra_dim = len(elem)-1

            # print(type(m))
            if type(m) is tuple:
                if len(m) == 2:
                    d_rows, d_cols = m
                elif len(m) == 3:
                    d_rows, d_cols, d_extra_dim = m
            else:
                d_rows = m

            if d_rows <= rows:
                return self.symbols_mat[val][d_rows]
            elif d_cols <= cols:
                return self.symbols_mat[val][d_rows][d_cols]
            elif d_extra_dim <= extra_dim:
                return self.symbols_mat[val][d_rows][d_cols][d_extra_dim]
            else:
                print("Index error!")
        else:
            print("Undefined variable!")