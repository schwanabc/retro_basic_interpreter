stack_LL1 = ["EOF"]
alphabet_set = set([chr(e) for e in range(ord('A'), ord('Z')+1)])
terminal_set = set(["+", "-", "IF", "<", "=", "PRINT", "GOTO", "STOP", "EOF"])

bcode_type ={
    "#line" : 10,
    "#id" : 11,
    "#const" : 12,
    "#if" : 13,
    "#goto" : 14,
    "#print" : 15,
    "#stop" : 16,
    "#op" : 17,
}

next_set ={
    1 : ["line", "pgm"],
    2 : ["EOF"],
    3 : ["line_num", "stmt"],
    4 : ["asgmnt"],
    5 : ["if"],
    6 : ["print"],
    7 : ["goto"],
    8 : ["stop"],
    9 : ["id", "=", "exp"],
    10 : ["term", "split1"],
    11 : ["+", "term"],
    12 : ["-", "term"],
    13 : None,
    14 : ["id"],
    15 : ["const"],
    16 : ["IF", "cond", "line_num"],
    17 : ["term", "split2"],
    18 : ["<", "term"],
    19 : ["=", "term"],
    20 : ["PRINT", "id"],
    21 : ["GOTO", "line_num"],
    22 : ["STOP"]
}

# A parsing tble in form of dict of dict
parsing_table = {
    "pgm" : {"line_num" : 1, "EOF" : 2},
    "line" : {"line_num" : 3},
    "asgmnt" : {"id" : 9},
    "split1" : {"line_num" : 13, "+" : 11, "-" : 12, "EOF" : 13},
    "term" : {"id" : 14, "const" : 15},
    "if" : {"IF" : 16},
    "split2" : {"<" : 18, "=" : 19},
    "print" : {"PRINT" : 20},
    "goto" : {"GOTO" : 21},
    "stop" : {"STOP" : 22},
    "stmt" : {"id" : 4, "IF" : 5, "PRINT" : 6, "GOTO" : 7, "STOP" : 8},
    "exp" : {"id" : 10, "const" : 10},
    "cond" : {"id" : 17, "const" : 17}
}

#return terminal type
def get_terminal_type(token, idx = -1):
    if token.isdigit():
        return "num"
    if(token in alphabet_set):
        return "id"
    if token in terminal_set:
        return token 
    raise Exception('Wrong Input Grammar : symbol ' +token +' is not in terminal set') 

#return what path to choose from parsing table
def get_rule(stack_top, token):
    terminal_type = get_terminal_type(token)
    if(terminal_type != "num" and terminal_type in parsing_table[stack_top]):
        return parsing_table[stack_top][terminal_type]
    if("line_num" in parsing_table[stack_top]):
        return parsing_table[stack_top]["line_num"]
    if("const" in parsing_table[stack_top]):
        return parsing_table[stack_top]["const"]
    raise Exception('Wrong Grammar : The rule is not defined') 

#check if both argument is same terminate symbol
def is_same_terminal(token, top_stack):       
    terminal_type = get_terminal_type(token)
    if(terminal_type != "num"):
        return terminal_type == top_stack
    else:
        return top_stack == "line_num" or top_stack == "const"
    
# check if the symbol is terminal symbol 
# the symbol that are not in non terminal set is terminal set
# the symbol is considered non terminal set if the symbol is in parsing table
def is_terminal(symbol):
    return not symbol in parsing_table

# interpreter scanner
def tokenize(line):
    return line.strip().split()

def get_bcode(terminal_symbol, value):
    if(terminal_symbol == "line_num"): 
        return ("#line", int(value))
    if(terminal_symbol == "id"): 
        return ("#id", ord(value) - ord('A') + 1)
    if(terminal_symbol == "const"): 
        return ("#const", int(value))
    if(terminal_symbol == "IF"): 
        return ("#if", 0)
    if(terminal_symbol == "GOTO"): 
        return ("#goto", int(value))
    if(terminal_symbol == "PRINT"): 
        return ("#print", 0)
    if(terminal_symbol == "STOP"): 
        return ("#stop", 0)
    if(terminal_symbol == "+"): 
        return ("#op", 1)
    if(terminal_symbol == "-"): 
        return ("#op", 2)
    if(terminal_symbol == "<"): 
        return ("#op", 3)
    if(terminal_symbol == "="): 
        return ("#op", 4)

def generate_bcode(parsed_list):
    bcode_list = []
    for i in range(len(parsed_list)):
#         if(parsed_list[i-1][0] == "GOTO" and i>0):
#             continue
        #include first line_num case
        if(parsed_list[i][0] not in ["GOTO","line_num"] or i == 0):
            bcode_list.append(get_bcode(parsed_list[i][0], parsed_list[i][1]))
        else:
            #omit GOTO case
            if(parsed_list[i][0] == 'line_num' and i != 0):
                bcode_list.append(get_bcode("GOTO", parsed_list[i][1]))
    return bcode_list
#interpreter parser
def parse(token):
    while(not is_same_terminal(token, stack_LL1[-1])):
        stack_top = stack_LL1.pop()
        if is_terminal(stack_top):
            raise Exception("Wrong Grammar: symbol '"+ token + "' is an unexpected terminal symbol") 
        rule = get_rule(stack_top, token)
        #print("-->",stack_top,rule, next_set[rule])
        if(next_set[rule] != None):
            stack_LL1.extend(next_set[rule][::-1])
        #print(stack_LL1)
        
    return stack_LL1.pop()
    
#convert scanned line to bcode
def convert_to_bcode(scanned_line):
    parsed_list = []
    for token in scanned_line:
        parsed_list.append((parse(token), token))
    bcode_list = generate_bcode(parsed_list)
    print('Generated bcode : ',bcode_list)
    bcode_string = ''
    for types, value in bcode_list:
        bcode_string = bcode_string + str(bcode_type[types])+ ' ' + str(value) + ' '
    return bcode_string.strip()
import sys
file_name = str(sys.argv[1])
file = open(file_name, 'r')
outfile = open(file_name+'.bout','w')
for line_count,line in enumerate(file):
    if line_count == 0:
        #init pgm if the chosen file is not a blank file 
        stack_LL1.append("pgm")
    scanned_line = tokenize(line)
    print(line.strip())
    bcode_string = convert_to_bcode(scanned_line)
    print('bcode : '+bcode_string)
    outfile.write(bcode_string+'\n')
outfile.write('0\n')
file.close()
outfile.close()