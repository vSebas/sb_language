import math

class Operations:
    def __init__(self):
        # self.operator = ''
        pass
    def oper_manager(self,operand1,oper,operand2):
        if   oper == '+':
            return operand1 + operand2
        elif oper == '-':
            return operand1 - operand2
        elif oper == '*':
            return operand1 * operand2
        elif oper == '/':
            return operand1 / operand2
        elif oper == '^':
            return math.pow(operand1,operand2)


class Program(Operations):
    def __init__(self):
        # Layout : 
        # symbols_ = {variable,dict_val}
        # dict_val = {type, value}
        self.symbols={}
        self.symbols_mat={}
        super().__init__()
    
    # def oper_manager(self,operand1,oper,operand2):
    #     return super().oper_manager(operand1,oper,operand2)

    def check_in_symbols(self,symbol,value):
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
            self.symbols[symbol] = assignment

    def create_symbol_mat(self,data_type,symbol,mat,assignment=None):
        if data_type != "INT" and data_type != "FLT":
            print("Invalid datatype!")
        else:
            if symbol not in self.symbols_mat:
                self.symbols_mat[symbol] = None
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