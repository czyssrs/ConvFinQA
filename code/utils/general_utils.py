import argparse
import collections
import json
import os
import re
import string
import sys
import random
import math
import numpy as np
from sympy import simplify

const_list = [
    "const_1",
    "const_2",
    "const_3",
    "const_4",
    "const_5",
    "const_6",
    "const_7",
    "const_8",
    "const_9",
    "const_10",
    "const_100",
    "const_1000",
    "const_10000",
    "const_100000",
    "const_1000000",
    "const_10000000",
    "const_1000000000",
    "const_m1",
    "none",
    "#0",
    "#1",
    "#2",
    "#3",
    "#4",
    "#5"
]

op_list = ["add(", "subtract(", "multiply(", "divide(", "exp(", "greater(", ")"]
all_ops = ["add", "subtract", "multiply", "divide", "exp", "greater", "table_max",
           "table_min", "table_sum", "table_average"]


def remove_space(text_in):
    res = []

    for tmp in text_in.split(" "):
        if tmp != "":
            res.append(tmp)

    return " ".join(res)


def table_row_to_text(header, row):
    '''
    use templates to convert table row to text
    '''
    res = ""
    
    if header[0]:
        res += (header[0] + " ")

    for head, cell in zip(header[1:], row[1:]):
        res += ("the " + row[0] + " of " + head + " is " + cell + " ; ")
    
    res = remove_space(res)
    return res.strip()

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def str_to_num(text):

    text = text.replace(",", "")
    try:
        num = float(text)
    except ValueError:
        if "%" in text:
            text = text.replace("%", "")
            try:
                num = float(text)
                num = num / 100.0
            except ValueError:
                num = "n/a"
        elif "const_" in text:
            text = text.replace("const_", "")
            if text == "m1":
                text = "-1"
            num = float(text)
        else:
            num = "n/a"
    return num


def process_row(row_in):

    row_out = []
    invalid_flag = 0

    for num in row_in:
        num = num.replace("$", "").strip()
        num = num.split("(")[0].strip()

        num = str_to_num(num)

        if num == "n/a":
            invalid_flag = 1
            break

        row_out.append(num)

    if invalid_flag:
        return "n/a"

    return row_out


def reprog_to_seq(prog_in, is_gold):
    '''
    predicted recursive program to list program
    ["divide(", "72", "multiply(", "6", "210", ")", ")"]
    ["multiply(", "6", "210", ")", "divide(", "72", "#0", ")"]
    '''

    st = []
    res = []

    try:
        num = 0
        for tok in prog_in:
            if tok != ")":
                st.append(tok)
            else:
                this_step_vec = [")"]
                for _ in range(3):
                    this_step_vec.append(st[-1])
                    st = st[:-1]
                res.extend(this_step_vec[::-1])
                st.append("#" + str(num))
                num += 1
    except:
        if is_gold:
            raise ValueError

    return res


def eval_program(program, table):
    '''
    calculate the numerical results of the program
    '''

    invalid_flag = 0
    this_res = "n/a"

    try:
        program = program[:-1]  # remove EOF
        # single number
        if len(program) == 1:
            return 0, round(float(str_to_num(program[0])), 5)
        # check structure
        for ind, token in enumerate(program):
            if ind % 4 == 0:
                if token.strip("(") not in all_ops:
                    return 1, "n/a"
            if (ind + 1) % 4 == 0:
                if token != ")":
                    return 1, "n/a"

        program = "|".join(program)
        steps = program.split(")")[:-1]

        res_dict = {}

        for ind, step in enumerate(steps):
            step = step.strip()

            if len(step.split("(")) > 2:
                invalid_flag = 1
                break
            op = step.split("(")[0].strip("|").strip()
            args = step.split("(")[1].strip("|").strip()

            arg1 = args.split("|")[0].strip()
            arg2 = args.split("|")[1].strip()

            if op == "add" or op == "subtract" or op == "multiply" or op == "divide" or op == "exp" or op == "greater":

                if "#" in arg1:
                    arg1 = res_dict[int(arg1.replace("#", ""))]
                else:
                    arg1 = str_to_num(arg1)
                    if arg1 == "n/a":
                        invalid_flag = 1
                        break

                if "#" in arg2:
                    arg2 = res_dict[int(arg2.replace("#", ""))]
                else:
                    arg2 = str_to_num(arg2)
                    if arg2 == "n/a":
                        invalid_flag = 1
                        break

                if op == "add":
                    this_res = arg1 + arg2
                elif op == "subtract":
                    this_res = arg1 - arg2
                elif op == "multiply":
                    this_res = arg1 * arg2
                elif op == "divide":
                    this_res = arg1 / arg2
                elif op == "exp":
                    this_res = arg1 ** arg2
                elif op == "greater":
                    this_res = "yes" if arg1 > arg2 else "no"

                res_dict[ind] = this_res

            elif "table" in op:
                table_dict = {}
                for row in table:
                    table_dict[row[0]] = row[1:]

                if "#" in arg1:
                    arg1 = res_dict[int(arg1.replace("#", ""))]
                else:
                    if arg1 not in table_dict:
                        invalid_flag = 1
                        break

                    cal_row = table_dict[arg1]
                    num_row = process_row(cal_row)

                if num_row == "n/a":
                    invalid_flag = 1
                    break
                if op == "table_max":
                    this_res = max(num_row)
                elif op == "table_min":
                    this_res = min(num_row)
                elif op == "table_sum":
                    this_res = sum(num_row)
                elif op == "table_average":
                    this_res = sum(num_row) / len(num_row)

                res_dict[ind] = this_res
        if this_res != "yes" and this_res != "no" and this_res != "n/a":

            this_res = round(this_res, 5)

    except:
        invalid_flag = 1

    return invalid_flag, this_res


def equal_program(program1, program2):
    '''
    symbolic program if equal
    program1: gold
    program2: pred
    '''

    sym_map = {}

    program1 = program1[:-1]  # remove EOF

    ### single number program
    if len(program1) == 1:
        if len(program2) == 2 and program1[0] == program2[0]:
            return True
        else:
            return False

    program1 = "|".join(program1)
    steps = program1.split(")")[:-1]

    invalid_flag = 0
    sym_ind = 0
    step_dict_1 = {}

    # symbolic map
    for ind, step in enumerate(steps):

        step = step.strip()

        assert len(step.split("(")) <= 2

        op = step.split("(")[0].strip("|").strip()
        args = step.split("(")[1].strip("|").strip()

        arg1 = args.split("|")[0].strip()
        arg2 = args.split("|")[1].strip()

        step_dict_1[ind] = step

        if "table" in op:
            if step not in sym_map:
                sym_map[step] = "a" + str(sym_ind)
                sym_ind += 1

        else:
            if "#" not in arg1:
                if arg1 not in sym_map:
                    sym_map[arg1] = "a" + str(sym_ind)
                    sym_ind += 1

            if "#" not in arg2:
                if arg2 not in sym_map:
                    sym_map[arg2] = "a" + str(sym_ind)
                    sym_ind += 1

    # check program 2
    step_dict_2 = {}
    try:
        program2 = program2[:-1]  # remove EOF
        # check structure
        for ind, token in enumerate(program2):
            if ind % 4 == 0:
                if token.strip("(") not in all_ops:
                    # print("structure error")
                    return False
            if (ind + 1) % 4 == 0:
                if token != ")":
                    # print("structure error")
                    return False

        program2 = "|".join(program2)
        steps = program2.split(")")[:-1]

        for ind, step in enumerate(steps):
            step = step.strip()

            if len(step.split("(")) > 2:
                return False
            op = step.split("(")[0].strip("|").strip()
            args = step.split("(")[1].strip("|").strip()

            arg1 = args.split("|")[0].strip()
            arg2 = args.split("|")[1].strip()

            step_dict_2[ind] = step

            if "table" in op:
                if step not in sym_map:
                    return False

            else:
                if "#" not in arg1:
                    if arg1 not in sym_map:
                        return False
                else:
                    if int(arg1.strip("#")) >= ind:
                        return False

                if "#" not in arg2:
                    if arg2 not in sym_map:
                        return False
                else:
                    if int(arg2.strip("#")) >= ind:
                        return False
    except:
        return False

    def symbol_recur(step, step_dict):

        step = step.strip()
        op = step.split("(")[0].strip("|").strip()
        args = step.split("(")[1].strip("|").strip()

        arg1 = args.split("|")[0].strip()
        arg2 = args.split("|")[1].strip()

        if "table" in op:
            # as var
            return sym_map[step]

        if "#" in arg1:
            arg1_ind = int(arg1.replace("#", ""))
            arg1_part = symbol_recur(step_dict[arg1_ind], step_dict)
        else:
            arg1_part = sym_map[arg1]

        if "#" in arg2:
            arg2_ind = int(arg2.replace("#", ""))
            arg2_part = symbol_recur(step_dict[arg2_ind], step_dict)
        else:
            arg2_part = sym_map[arg2]

        if op == "add":
            return "( " + arg1_part + " + " + arg2_part + " )"
        elif op == "subtract":
            return "( " + arg1_part + " - " + arg2_part + " )"
        elif op == "multiply":
            return "( " + arg1_part + " * " + arg2_part + " )"
        elif op == "divide":
            return "( " + arg1_part + " / " + arg2_part + " )"
        elif op == "exp":
            return "( " + arg1_part + " ** " + arg2_part + " )"
        elif op == "greater":
            return "( " + arg1_part + " > " + arg2_part + " )"

    # # derive symbolic program 1
    steps = program1.split(")")[:-1]
    sym_prog1 = symbol_recur(steps[-1], step_dict_1)
    sym_prog1 = simplify(sym_prog1, evaluate=False)

    try:
        # derive symbolic program 2
        steps = program2.split(")")[:-1]
        sym_prog2 = symbol_recur(steps[-1], step_dict_2)
        sym_prog2 = simplify(sym_prog2, evaluate=False)
    except:
        return False

    # print(sym_prog1)
    # print(sym_prog2)
    return sym_prog1 == sym_prog2


def evaluate_result(json_in, json_ori, all_res_file, error_file, program_mode):
    '''
    execution acc
    program acc
    '''
    correct = 0

    with open(json_in) as f_in:
        data = json.load(f_in)

    with open(json_ori) as f_in:
        data_ori = json.load(f_in)

    data_dict = {}
    for each_data in data_ori:
        assert each_data["id"] not in data_dict
        data_dict[each_data["id"]] = each_data

    exe_correct = 0
    prog_correct = 0

    res_list = []
    all_res_list = []

    for tmp in data:
        each_data = data[tmp][0]
        each_id = each_data["id"]

        each_ori_data = data_dict[each_id]

        table = each_ori_data["table"]
        gold_res = each_ori_data["annotation"]["exe_ans"]

        pred = each_data["pred_prog"]
        gold = each_data["ref_prog"]

        if program_mode == "nest":
            if pred[-1] == "EOF":
                pred = pred[:-1]
            pred = reprog_to_seq(pred, is_gold=False)
            pred += ["EOF"]
            gold = gold[:-1]
            gold = reprog_to_seq(gold, is_gold=True)
            gold += ["EOF"]

        invalid_flag, exe_res = eval_program(pred, table)

        if invalid_flag == 0:
            if exe_res == gold_res:
                exe_correct += 1

            if equal_program(gold, pred):
                # if exe_res != gold_res:
                #     print(each_id)
                #     print(gold)
                #     print(pred)
                #     print(gold_res)
                #     print(exe_res)
                #     print(each_ori_data["id"])
                assert exe_res == gold_res
                prog_correct += 1
                # if "".join(gold) != "".join(pred):
                #     print(each_id)
                #     print(gold)
                #     print(pred)
                #     print(gold_res)
                #     print(exe_res)
                #     print(each_ori_data["id"])

        each_ori_data["annotation"]["predicted"] = pred

        if exe_res != gold_res:
            res_list.append(each_ori_data)
        all_res_list.append(each_ori_data)

    exe_acc = float(exe_correct) / len(data)
    prog_acc = float(prog_correct) / len(data)

    print("All: ", len(data))
    print("Correct: ", correct)
    print("Exe acc: ", exe_acc)
    print("Prog acc: ", prog_acc)

    with open(error_file, "w") as f:
        json.dump(res_list, f, indent=4)

    with open(all_res_file, "w") as f:
        json.dump(all_res_list, f, indent=4)

    return exe_acc, prog_acc


def program_tokenization(original_program):
    original_program = original_program.split(', ')
    program = []
    for tok in original_program:
        cur_tok = ''
        for c in tok:
            if c == ')':
                if cur_tok != '':
                    program.append(cur_tok)
                    cur_tok = ''
            cur_tok += c
            if c in ['(', ')']:
                program.append(cur_tok)
                cur_tok = ''
        if cur_tok != '':
            program.append(cur_tok)
    program.append('EOF')
    return program



if __name__ == '__main__':

    root = "/mnt/george_bhd/zhiyuchen/FinDial/data/"
    our_data = root + "dataset/"