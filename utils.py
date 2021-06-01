from exceptions import SBLanguageExceptions
import math

class Program:
    def __init__(self):
        # Layout : 
        # symbols_ = {variable,dict_val}
        # dict_val = {type, value}
        self.symbols={}
        self.symbols_mat={}
        self.temporal_avail={}
        self.quadruples=[[None, None, None, None]]
        self.constants=[]
        self.PC=0

        # Eliminar siguientes:
        self.symbols_type={}
        self.symbols_mat_type={}

    def start_program(self):
        self.PC=0
        self.quadruples[0][0] = "GOTO"
        self.quadruples[0][1] = 1       # Can go to the first position as PROCEDURES are located after the main program

    def end_program(self):
        self.quadruples.append(["ENDPROGRAM",None,None,None])
        # self.quadruples[0][1] = 1       # Can go to the first position as PROCEDURES are located after the main program

    def generate_quadruple(self,quad1,quad2,quad3=None):
        pos=len(self.temporal_avail)
        self.temporal_avail[f"T{pos}"]=None
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
        else: # expresiones estilo: not A, o -5
            # print("{} {} {} {}".format(quad2," ",quad2,f"T{pos}"))
            '''
            if quad1 in self.temporal_avail.keys():
                del self.temporal_avail[quad1]

            if quad3 in self.temporal_avail.keys():
                del self.temporal_avail[quad3]
            '''
            self.quadruples.append([quad1,None,quad2,f"T{pos}"])
            return f"T{pos}"
        return None

    def clean_temporal_avail(self):
        self.temporal_avail.clear()

    def check_intermediate_code(self):
        print("Check Quadruples:")
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

            if   quadruple[1] in self.symbols.keys():
                quadruple1 =  self.symbols[quadruple[1]]
                quad1_flag = "symbol"
            elif quadruple[1] in self.temporal_avail.keys():
                quadruple1 =  self.temporal_avail[quadruple[1]]
                quad1_flag = "temporal"
            elif quadruple[1] in self.constants:
                index = self.constants.index(quadruple[1])
                quadruple1 =  self.constants[index]
                quad1_flag = "constant"
            
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
                # print(quadruple2)

            elif opcode == 'GOTO':
                self.PC = quadruple[1]
                jump = 1
            elif opcode == 'ENDPROGRAM':
                print("Program finished")
                self.check_symbol_values()
                exit()

            if (not jump):
                if quad3_flag == "symbol":
                    self.symbols[quadruple[3]] = quadruple3
                else:
                    self.temporal_avail[quadruple[3]] = quadruple3

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