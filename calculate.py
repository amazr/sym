import re
# todo:
# refactor ops list to include a sign in the 0th position
# make creation of symbolic and literal terms list be lterms-rterms or lterms/*rterms
# maybe do more research into creating symbolic and literal terms
class Calculate:
    def __init__(self):
        self.function = ""
        self.lterms = []
        self.rterms = []
        self.symbols = []
        self.lops = []
        self.rops = []
        self.ops_list = ["+","-","*","/","="]
    
    def clear(self):
        self.lterms = []
        self.rterms = []
        self.function = ""
        self.symbols = []
        self.rops = []
        self.lops = []

    def eval(self, function):
        self.load_function(function)
        self.resolve_symbols()
        #self.debug()
        if len(self.symbols) == 0:
            if len(self.rterms) == 0:
                return self.simple_solve(self.lterms, self.lops)
            else:
                l_result = self.simple_solve(self.lterms, self.lops)
                r_result = self.simple_solve(self.rterms, self.rops)
                if l_result != r_result:
                    return str(l_result) + " != " + str(r_result)
                else:
                    return str(l_result) + " = " + str(r_result)
        elif len(self.symbols) == 1:
            return self.symbolic_solve()
        else:
            return "Error: Cannot solve for more than one symbol" 

    # If the function doesn't have an equal sign then all the terms get loaded into lterms, this is most likely a simple problem
    def load_function(self, function):
        self.function = function
        load_r = False
        temp_term = ""
        for symbol in function:
            if symbol not in self.ops_list:
                temp_term = temp_term + symbol
            elif symbol == "=":
                load_r = True
                self.lterms.append(temp_term)
                temp_term = ""
            else:
                if load_r:
                    if len(self.rterms) == 0 and symbol == "-" and len(temp_term) == 0:
                        temp_term = "-" + temp_term
                        continue
                    elif len(self.rterms) == 0 and len(temp_term) == 0:
                        temp_term = ""
                        continue
                    self.rterms.append(temp_term)
                    self.rops.append(symbol)
                else:
                    if len(self.lterms) == 0 and symbol == "-" and len(temp_term) == 0:
                        temp_term = "-" + temp_term
                        continue
                    elif len(self.lterms) == 0 and len(temp_term) == 0:
                        temp_term = ""
                        continue
                    self.lterms.append(temp_term)
                    self.lops.append(symbol)
                temp_term = ""
        if load_r:
            self.rterms.append(temp_term)
        else:
            self.lterms.append(temp_term)
        self.debug()
    
    def simple_solve(self, terms, ops):
        result = smart_cast(terms[0])
        for i in range(0,len(ops)):
            if ops[i] == self.ops_list[0]:
                result = result + smart_cast(terms[i+1])
            elif ops[i] == self.ops_list[1]:
                result = result - smart_cast(terms[i+1])
            elif ops[i] == self.ops_list[2]:
                result = result * smart_cast(terms[i+1])
            elif ops[i] == self.ops_list[3]:
                if result % smart_cast(terms[i+1]) == 0:
                    result = int(result / smart_cast(terms[i+1]))
                else:
                    result = result / smart_cast(terms[i+1])
            else:
                result = "Error: Unknown Operator \""+str(ops[i])+"\""
                return result
        return result

    #Todo allow symbol multiplicative coefficients
    def symbolic_solve(self):
        symbolic_terms = []
        symbolic_ops = []
        literal_terms = []
        literal_ops = []
        for i in range(0,len(self.lterms)):
            if self.symbols[0] in self.lterms[i]:
                symbolic_terms.append(self.lterms[i])
                if len(symbolic_terms) > 1 and self.lops[i-1] == "-":
                    symbolic_ops.append("-")
                if len(symbolic_terms) > 1:
                    symbolic_ops.append("+")
            else:
                literal_terms.append(self.lterms[i])
                if len(literal_terms) > 1:
                    literal_ops.append(self.lops[i-1])
        for i in range(0,len(self.rterms)):
            if self.symbols[0] in self.rterms[i]:
                symbolic_terms.append(self.rterms[i])
                if i != 0 and self.rops[i-1] == "-":
                    symbolic_ops.append("-")
                elif len(symbolic_terms) > 0:
                    symbolic_ops.append("+")
            else:
                literal_terms.append(self.rterms[i])
                if i != 0:
                    literal_ops.append(self.rops[i-1])
                elif len(literal_terms) > 0:
                    literal_ops.append("+")
        #remove x from symbolic terms, simple solve
        for i in range(0,len(symbolic_terms)):
            symbolic_terms[i] = symbolic_terms[i].replace(self.symbols[0], '')
        print(symbolic_terms)
        sym_result = self.simple_solve(symbolic_terms, symbolic_ops)
        #simple solve literal terms
        lit_result = self.simple_solve(literal_terms, literal_ops)
        #divide literal terms by symbolic terms without x
        result = lit_result/sym_result
        #x=result from above
        return self.symbols[0] + " = " + str(result)
        self.debug()
                    


    def resolve_symbols(self):
        self.symbols = list(set(re.findall('[a-zA-Z]', self.function)))



    def debug(self):
        print("##############")
        print(self.lterms)
        print(self.rterms)
        print(self.lops)
        print(self.rops)
        print(self.symbols)
        print("##############")

#############
## Helpers
#############
def smart_cast(to_cast):
    if '.' in to_cast:
        return float(to_cast)
    else:
        return int(to_cast)