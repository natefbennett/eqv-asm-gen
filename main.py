# Used GoLang reference example: https://github.com/alanvivona/pwnshop/tree/master/src/0x12-SLAE-shellstorm-polymorph/polymorph

from dataclasses import dataclass
import json
import random

@dataclass
class Lex:
    operand: str
    values: list
    abstract_representation: str
    original_string: str


def ParseLine(line, registers):

    # format line
    line = line.rstrip("\n")
    line = line.lower()
    line = line.split(";")[0] # remove comments
    line = line.strip()
    line = line.replace(",", " , ")
    line = line.replace("  ", " ")

    lex = Lex("", [], "", "")
    lex.original_string = line

    if len(line) == 0:
        return lex

    # split line up into essential parts and track abstract value of registers
    line_parts = []
    seen_registers = []

    for part in line.split():

        if len(part) > 0 and part != " " and part != ",":
            line_parts.append(part)
            
            if registers.get(part, False):
                if part not in seen_registers:
                    seen_registers.append(part)

    #  build abstract representation
    abstract_rep = ""
    
    for i, part in enumerate(line_parts):

        # part is a register
        if registers.get(part, False):
            abstract_rep += " ${}".format(seen_registers.index(part)+1)

        # first part, the operand
        elif i == 0:
            abstract_rep = part
            lex.operand = part

        #  every other part type
        else:
            abstract_rep += " " + part

    lex.values = line_parts[1:] # everything except operand
    lex.abstract_representation = abstract_rep

    return lex


def Polymorph(lexer, morph_rules):

    # look up equivalences of abstract representation
    equivalences = morph_rules.get(lexer.abstract_representation, "empty")

    # if no equivalences exist, return original line
    if equivalences == "empty":
        return [ lexer.original_string ]

    # choose and equivlence at random
    equiv_choice = random.choice(equivalences)

    # replace placeholders with values
    result = []

    for part in equiv_choice:
        result.append(part)

    for i, value in enumerate(lexer.values):
        for j, part in enumerate(result):
            result[j] = part.replace( "$"+str(i+1), value )
            
    return result

if __name__ == "__main__":
    
    # asm_filename = input("== Target ASM File: ")
    asm_filename = "test.nasm"

    #  load register data and polymorphic rules from json files to dictionary
    reg_filename = "architecture-registers.json"
    rul_filename = "polymorphic-rules.json"

    reg_file, rul_file = open(reg_filename), open(rul_filename)

    # conversion data dictionaries
    registers = json.load(reg_file)
    morph_rules = json.load(rul_file)

    reg_file.close()
    rul_file.close()

    with open(asm_filename) as lines:

        # loop thourgh lines in original assembly file
        for line_orig in lines:

            # parse assembly line to generate metadata
            lexer = ParseLine(line_orig, registers)
            
            # use line metadata to lookup equivalent expression
            converted = Polymorph(lexer, morph_rules)

            # equivalent expression may contain multiple lines
            for line_conv in converted:
                print(line_conv)

