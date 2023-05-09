import argparse
import xml.etree.ElementTree as ET
import re
import sys

# ERRORS
# 31 - chybný XML formát ve vstupním souboru (soubor není tzv. dobře formátovaný, angl.well-formed, viz [1]);
# 32 - neočekávaná struktura XML (např. element pro argument mimo element pro instrukci,instrukce s duplicitním pořadím nebo záporným pořadím)
#      či lexikální nebo syntaktická chybatextových elementů a atributů ve vstupním XML souboru (např. chybný lexém pro číselnýnebo řetězcový literál,
#      neznámý operační kód apod.).
# 52 - chyba při sémantických kontrolách vstupního kódu v IPPcode21 (např. použití nedefino-vaného návěští, redefinice proměnné);
# 53 - běhová chyba interpretace – špatné typy operandů;
# 54 - běhová chyba interpretace – přístup k neexistující proměnné (rámec existuje);
# 55 - běhová chyba interpretace – rámec neexistuje (např. čtení z prázdného zásobníku rámců);
# 56 - běhová chyba interpretace – chybějící hodnota (v proměnné, na datovém zásobníku nebo zásobníku volání);
# 57 - běhová chyba interpretace – špatná hodnota operandu (např. dělení nulou, špatná návra-tová hodnota instrukce exit);
# 58 - běhová chyba interpretace – chybná práce s řetězcem. Řádek obsahující pouze bílé znaky je považován za prázdný.

# ==========================================
# global variables
instr_list = []

frames = {"GF": {}}
local_frames = []
label_indexes = {}
past_calls = []
memory_stack = []

instr_calls = 0
curr_index = 0
inFile = ""

class instruction:
    def __init__(self, operands, funcPtr):
        self.operands = operands
        self.funcPtr = funcPtr

    def call(self):
        self.funcPtr(self.operands)

    def __str__(self):
        return "%-10s %s" % (self.funcPtr.__name__, " ".join([str(i) for i in self.operands]))

class var:
    def __init__(self):
        self.initialized = False

    def __repr__(self):
        if self.initialized:
            return str(self.value)
        else:
            return "uninitialized"

    def setValue(self, value):
        self.initialized = True
        self.value = value

    def getValue(self):
        if not self.initialized:
            sys.exit(56)
        return self.value

class operand:
    def __str__(self):
        if self.opType == "var":
            return "v: %-15s" % (f"{self.frame_name}@{self.var_name}")
        else:
            return "o: %-15s" % (f"{self.value}")

    def __repr__(self):
        return self.__str__()

    def __init__(self, opType, value):
        self.opType = opType
        if self.opType == "var":
            self.frame_name, self.var_name = value.split("@", 1)
        else:
            self.value = value

    def getVar(self):
        frame = frames.get(self.frame_name)
        if frame == None:
            sys.exit(55)
        var = frame.get(self.var_name)
        if var == None:
            sys.exit(54)
        return var

    def setVarValue(self, value):
        if self.opType != "var":
            sys.exit(53)
        self.getVar().setValue(value)

    def getVarValue(self):
        return self.getVar().getValue()

    def getValue(self):
        if self.opType == "var":
            return self.getVarValue()
        else:
            return self.value

# escape \065 to unicode
def escape(match):
    return chr(int(match.group(1)))

# tajp = type, because default function in python
def parseSymb(value, tajp):
    if tajp == "string":
        if value == None:
            return operand(tajp, "")
        gstring = re.match(r"^([^\\]|(\\\d{3})*)*$", value)

        if gstring:
            value = re.sub(r"\\(\d\d\d)", escape, value)
            return operand(tajp, value)
        else:
            sys.exit(32)

    if tajp == "int":
        gint = re.match(r"^[+-]?[\d][\d]*$", value)
        if gint:
            return operand(tajp, int(value))
        else:
            sys.exit(32)

    if tajp == "float":
        gfloat = re.match(r"^[\d]*[.][\d]*$", value)
        if gfloat:
            value = float(value)
        else:
            value = float.fromhex(value)
        return operand(tajp, value)

    if tajp == "bool":
        gbool = re.match(r"^(true|false)$", value)
        if gbool:
            return operand(tajp, value == "true")
        else:
            sys.exit(32)

    if tajp == "nil":
        gnil = re.match(r"^(nil)$", value)
        if gnil:
            return operand(tajp, None)
        else:
            sys.exit(32)

    if tajp == "var":
        return parseVar(value, tajp)

    sys.exit(32)

def parseVar(value, tajp):
    if tajp != "var":
        sys.exit(32)
    match = re.match(
        r"^(GF|TF|LF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$", value)
    if not match:
        sys.exit(53)
    return operand(tajp, value)

def parseType(value, tajp):
    types = {
        "int": int,
        "float": float,
        "bool": bool,
        "string": str,
        "nil": type(None)
    }
    if not value in types or tajp != "type":
        sys.exit(53)
    return operand(tajp, types[value])

def parseLabel(value, tajp):
    match = re.match(r"^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$", value)
    if not match:
        sys.exit(53)
    return operand(tajp, value)

# ==========================================
# Main function
def main():
    # parse arguments
    arg = argparse.ArgumentParser()
    arg.add_argument("--source", type=str,
                     help="vstupní soubor s XML reprezentací zdrojového kódu")
    arg.add_argument("--input", type=str,
                     help="soubor se vstupy pro samotnou interpretaci zadaného zdrojového kódu")
    args = arg.parse_args()

    if args.source is None and args.input is None:
        sys.exit("--source nebo --input, alespoň jeden parametr musí být vždy zadán")

    if args.source is not None:
        sourcefile = args.source
    else:
        sourcefile = sys.stdin

    global inFile
    if args.input:
        inFile = open(args.input, "r")
    else:
        inFile = sys.stdin

    # xml tree
    try:
        tree = ET.parse(sourcefile)
        root = tree.getroot()
    except Exception:
        sys.exit(31)

    if root.tag != "program":
        sys.exit(32)

    # check orders for negative number and string
    orders = []
    for child in root:
        global instr_calls
        instr_calls += 1
        order = child.attrib.get("order")
        try:
            order = int(order)
        except Exception:
            sys.exit(32)
        if order <= 0:
            sys.exit(32)

        orders.append(order)

    # if duplicit orders
    if len(set(orders)) != len(orders):
        sys.exit(32)

    # order "order"
    root[:] = sorted(root, key=lambda elem: int(elem.attrib.get("order", 0)))
    for child in root:
        parseInstruction(child)

    global instr_list
    inst_count = len(instr_list)

    global curr_index
    while curr_index < inst_count:
        instr_list[curr_index].call()
        curr_index += 1

def parseLabelInst(label, index):
    global label_indexes
    if label in label_indexes:
        sys.exit(52)
    label_indexes[label] = index

def parseInstruction(child):
    if child.tag != "instruction":
        sys.exit(32)
    if not ("order" in child.attrib) or not ("opcode" in child.attrib):
        sys.exit(32)

    opcode = child.attrib.get("opcode")
    opcode = opcode.upper()
    if not opcode in INSTRUCTS:
        sys.exit(32)

    global instr_list
    vzor = INSTRUCTS[opcode]
    operands = parseOperands(child, vzor[0])
    if opcode == "LABEL":
        parseLabelInst(operands[0].getValue(), len(instr_list))
    funcPtr = vzor[1]
    instr_list.append(instruction(operands, funcPtr))

def parseOperands(child, vzor):
    operands = []

    child[:] = sorted(child, key=lambda elem: elem.tag)
    if len(vzor) != len(child):
        sys.exit(32)

    for i in range(len(vzor)):
        arg = child[i]

        if not(re.match(f"^arg{len(operands)+1}$", arg.tag)):
            sys.exit(32)
        operands.append(vzor[i](arg.text, arg.attrib.get("type")))

    return operands

# Called functions from dict instructs
def funcmove(operands):
    operands[0].setVarValue(operands[1].getValue())

def funcdefvar(operands):
    global frames
    frame = frames.get(operands[0].frame_name)
    if frame == None:
        sys.exit(55)
    variable = frame.get(operands[0].var_name)
    if variable != None:
        sys.exit(52)
    frame[operands[0].var_name] = var()

def funccreateframe(operands):
    global frames
    frames["TF"] = {}

def funcpushframe(operands):
    global frames
    global local_frames
    if not "TF" in frames:
        sys.exit(55)
    local_frames.append(frames["TF"])
    frames.pop("TF")
    frames["LF"] = local_frames[len(local_frames) - 1]

def funcpopframe(operands):
    global frames
    global local_frames
    if len(local_frames) <= 0:
        sys.exit(55)
    frames["TF"] = local_frames.pop()

    if len(local_frames) > 0:
        frames["LF"] = local_frames[len(local_frames) - 1]
    else:
        frames.pop("LF")

def funccall(operands):
    global curr_index
    global label_indexes
    past_calls.append(curr_index)
    curr_index = label_indexes.get(operands[0].getValue())
    if curr_index == None:
        sys.exit(53)

def funcreturn(operands):
    global curr_index
    if len(past_calls) == 0:
        sys.exit(56)
    curr_index = past_calls.pop()

def funcpushs(operands):
    memory_stack.append(operands[0].getValue())

def funcpops(operands):
    if len(memory_stack) <= 0:
        sys.exit(56)
    operands[0].setVarValue(memory_stack.pop())

def funcadd(operands):
    if ((type(operands[1].getValue()) != int) or (type(operands[2].getValue()) != int)) and ((type(operands[1].getValue()) != float) or (type(operands[2].getValue()) != float)):
        sys.exit(53)
    res = operands[1].getValue() + operands[2].getValue()
    operands[0].setVarValue(res)

def funcsub(operands):
    if ((type(operands[1].getValue()) != int) or (type(operands[2].getValue()) != int)) and ((type(operands[1].getValue()) != float) or (type(operands[2].getValue()) != float)):
        sys.exit(53)
    res = operands[1].getValue() - operands[2].getValue()
    operands[0].setVarValue(res)

def funcmul(operands):
    if ((type(operands[1].getValue()) != int) or (type(operands[2].getValue()) != int)) and ((type(operands[1].getValue()) != float) or (type(operands[2].getValue()) != float)):
        sys.exit(53)
    res = operands[1].getValue() * operands[2].getValue()
    operands[0].setVarValue(res)

def funcidiv(operands):
    if (type(operands[1].getValue()) != int) or (type(operands[2].getValue()) != int):
        sys.exit(53)
    if operands[2].getValue() == 0:
        sys.exit(57)
    res = operands[1].getValue() // operands[2].getValue()
    operands[0].setVarValue(res)

def funclt(operands):
    if type(operands[1].getValue()) != type(operands[2].getValue()):
        sys.exit(53)
    res = operands[1].getValue() < operands[2].getValue()
    operands[0].setVarValue(res)

def funcgt(operands):
    if type(operands[1].getValue()) != type(operands[2].getValue()):
        sys.exit(53)
    res = operands[1].getValue() > operands[2].getValue()
    operands[0].setVarValue(res)

def funceq(operands):
    type1 = type(operands[1].getValue())
    type2 = type(operands[2].getValue())
    if type1 != type2 and (type1 != type(None) and type2 != type(None)):
        sys.exit(53)
    res = operands[1].getValue() == operands[2].getValue()
    operands[0].setVarValue(res)

def funcand(operands):
    if type(operands[1].getValue()) == bool and type(operands[2].getValue()) == bool:
        res = operands[1].getValue() and operands[2].getValue()
        operands[0].setVarValue(res)
        return
    sys.exit(53)

def funcor(operands):
    if type(operands[1].getValue()) == bool and type(operands[2].getValue()) == bool:
        res = operands[1].getValue() or operands[2].getValue()
        operands[0].setVarValue(res)
        return
    sys.exit(53)

def funcnot(operands):
    if type(operands[1].getValue()) == bool:
        res = not operands[1].getValue()
        operands[0].setVarValue(res)
        return
    sys.exit(53)

def funcint2char(operands):
    if(type(operands[1].getValue()) != int):
        sys.exit(53)
    try:
        res = chr(operands[1].getValue())
    except Exception:
        sys.exit(58)
    operands[0].setVarValue(res)

def funcstri2int(operands):
    s = operands[1].getValue()
    i = operands[2].getValue()
    c = s[i]
    if 0 <= i < len(s):
        sys.exit(58)
    operands[0].setVarValue(ord(c))

def funcread(operands):
    x = inFile.readline()
    if x == "":
        operands[0].setVarValue(None)
        return
    x = x.rstrip()

    tajp = operands[1].getValue()
    if tajp == str:
        res = x
    if tajp == bool:
        res = x.lower() == "true"
    if tajp == int:
        try:
            res = int(x)
        except:
            res = "nil"
    if tajp == float:
        try:
            res = float.fromhex(x)
        except:
            res = "nil"
    if tajp == type(None):
        sys.exit(53)
    operands[0].setVarValue(res)

def funcwrite(operands):
    text = operands[0].getValue()
    if (type(text) == bool):
        print(text.__str__().lower(), end="")
    elif(type(text) == float):
        print(float.hex(text), end="")
    elif (type(text) == type(None)):
        print("", end="")
    else:
        print(text, end="")

def funcconcat(operands):
    if (type(operands[1].getValue()) != str) or (type(operands[2].getValue()) != str):
        sys.exit(53)
    res = operands[1].getValue() + operands[2].getValue()
    operands[0].setVarValue(res)

def funcstrlen(operands):
    x = operands[1].getValue()
    if type(x) != str:
        sys.exit(53)
    res = len(x)
    operands[0].setVarValue(res)

def funcgetchar(operands):
    s = operands[1].getValue()
    i = operands[2].getValue()

    if type(s) != str or type(i) != int:
        sys.exit(53)
    if not (0 <= i < len(s)):
        sys.exit(58)
    c = s[i]
    operands[0].setVarValue(c)

def funcsetchar(operands):
    s = operands[0].getValue()
    i = operands[1].getValue()
    c = operands[2].getValue()

    if type(i) != int or type(s) != str or type(c) != str:
        sys.exit(53)
    if (not (0 <= i < len(s))) or c == "":
        sys.exit(58)

    s[i] = c
    operands[0].setVarValue(s)

def functype(operands):
    if operands[1].opType == "var" and operands[1].getVar().initialized == False:
        operands[0].setVarValue("")
    else:
        tajp = type(operands[1].getValue())
        if(tajp == int):
            res = "int"
        if(tajp == float):
            res = "float"
        if(tajp == str):
            res = "string"
        if(tajp == bool):
            res = "bool"
        if tajp == type(None):
            res = "nil"
        operands[0].setVarValue(res)

def funclabel(operands):
    pass

def funcjump(operands):
    global curr_index
    global label_indexes
    curr_index = label_indexes.get(operands[0].getValue())
    if curr_index == None:
        sys.exit(52)

def funcjumpifeq(operands):
    global curr_index
    global label_indexes
    if (type(operands[1].getValue()) == type(operands[2].getValue())) or (type(operands[1].getValue()) == None) or (type(operands[2].getValue()) == None):
        if (operands[1].getValue() == operands[2].getValue()):
            curr_index = label_indexes.get(operands[0].getValue())
            if curr_index == None:
                sys.exit(52)
    else:
        sys.exit(53)

def funcjumpifneq(operands):
    global curr_index
    global label_indexes
    if (type(operands[1].getValue()) == type(operands[2].getValue())) or (type(operands[1].getValue()) == None) or (type(operands[2].getValue()) == None):
        if (operands[1].getValue() != operands[2].getValue()):
            curr_index = label_indexes.get(operands[0].getValue())
            if curr_index == None:
                sys.exit(52)
    else:
        sys.exit(53)

def funcexit(operands):
    val = operands[0].getValue()
    if (type(val) != int):
        sys.exit(53)
    if not (0 <= val <= 49):
        sys.exit(57)
    sys.exit(val)

def funcdprint(operands):
    text = operands[0].getValue()
    print(text, file=sys.stderr, end="")

def funcbreak(operands):
    print(curr_index, file=sys.stderr)
    print(frames, file=sys.stderr)
    print(instr_calls, file=sys.stderr)

def funcdiv(operands):
    if ((type(operands[1].getValue()) != float) or (type(operands[2].getValue()) != float)):
        sys.exit(53)

    if operands[2].getValue() == 0:
        sys.exit(57)

    operands[0].setVarValue(operands[1].getValue() / operands[2].getValue())

def funcfloat2int(operands):
    if (type(operands[1].getValue()) != float):
        sys.exit(53)

    res = operands[1].getValue()

    try:
        res = int(res)
    except:
        sys.exit(58)

    operands[0].setVarValue(res)

def funcint2float(operands):
    if (type(operands[1].getValue()) != int):
        sys.exit(53)

    res = operands[1].getValue()

    try:
        res = float(res)
    except:
        sys.exit(58)

    operands[0].setVarValue(res)

# ==========================================
# Dictionary with pointers to functions
INSTRUCTS = {
    "MOVE":         ([parseVar, parseSymb], funcmove),
    "DEFVAR":       ([parseVar], funcdefvar),
    "CREATEFRAME":  ([], funccreateframe),
    "PUSHFRAME":    ([], funcpushframe),
    "POPFRAME":     ([], funcpopframe),
    "CALL":         ([parseLabel], funccall),
    "RETURN":       ([], funcreturn),
    "PUSHS":        ([parseSymb], funcpushs),
    "POPS":         ([parseVar], funcpops),
    "ADD":          ([parseVar, parseSymb, parseSymb], funcadd),
    "SUB":          ([parseVar, parseSymb, parseSymb], funcsub),
    "MUL":          ([parseVar, parseSymb, parseSymb], funcmul),
    "IDIV":         ([parseVar, parseSymb, parseSymb], funcidiv),
    "LT":           ([parseVar, parseSymb, parseSymb], funclt),
    "GT":           ([parseVar, parseSymb, parseSymb], funcgt),
    "EQ":           ([parseVar, parseSymb, parseSymb], funceq),
    "AND":          ([parseVar, parseSymb, parseSymb], funcand),
    "OR":           ([parseVar, parseSymb, parseSymb], funcor),
    "NOT":          ([parseVar, parseSymb], funcnot),
    "INT2CHAR":     ([parseVar, parseSymb], funcint2char),
    "STRI2INT":     ([parseVar, parseSymb, parseSymb], funcstri2int),
    "READ":         ([parseVar, parseType], funcread),
    "WRITE":        ([parseSymb], funcwrite),
    "CONCAT":       ([parseVar, parseSymb, parseSymb], funcconcat),
    "STRLEN":       ([parseVar, parseSymb], funcstrlen),
    "GETCHAR":      ([parseVar, parseSymb, parseSymb], funcgetchar),
    "SETCHAR":      ([parseVar, parseSymb, parseSymb], funcsetchar),
    "TYPE":         ([parseVar, parseSymb], functype),
    "LABEL":        ([parseLabel], funclabel),
    "JUMP":         ([parseLabel], funcjump),
    "JUMPIFEQ":     ([parseLabel, parseSymb, parseSymb], funcjumpifeq),
    "JUMPIFNEQ":    ([parseLabel, parseSymb, parseSymb], funcjumpifneq),
    "EXIT":         ([parseSymb], funcexit),
    "DPRINT":       ([parseSymb], funcdprint),
    "BREAK":        ([], funcbreak),

    # # FLOAT EXTENSION
    "INT2FLOAT":    ([parseVar, parseSymb], funcint2float),
    "FLOAT2INT":    ([parseVar, parseSymb], funcfloat2int),
    "DIV":          ([parseVar, parseSymb, parseSymb], funcdiv)
}

if __name__ == "__main__":
    main()
