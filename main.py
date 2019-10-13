# -*— coding: utf-8 *-*
from myQueue import myQueue
import copy
from random import randrange

op = {
    "+": [1,0],
    "-": [0,0],
    "x": [1,1],
    "=": [0,1]}
op_cand = ["+", "-", "x"]

# op_change:
## type1: with stick number change
op_switch_stick_change_add = {"-": ["+", "="]}
op_switch_stick_change_sub = {"+": "-", "=": "-"} 
# - <-> = (only possible in situation with 2 or more sticks moved || A-B=C <-> A=B-C)
## type2: with stable stick number
op_switch_stick_stable = {"+": "=", "=": "+"}
# + <-> = (only possible in situation with 2 or more sticks moved || A=B=C <-> A+B=C or A=B+C)

# op_constrain:
# must include one and only one "="
# every "+""-""x": each side of the operator should have 2 numbers

"""
# number encoding order with:
 —— 0
| 1 | 2
 —— 3
| 4 | 5
 —— 6
"""

num = {
    "0": [1,1,1,0,1,1,1],
    "1": [0,0,1,0,0,1,0],
    "2": [1,0,1,1,1,0,1],
    "3": [1,0,1,1,0,1,1],
    "4": [0,1,1,1,0,1,0],
    "5": [1,1,0,1,0,1,1],
    "6": [1,1,0,1,1,1,1],
    "7": [1,0,1,0,0,1,0],
    "8": [1,1,1,1,1,1,1],
    "9": [1,1,1,1,0,1,1],
    "None" : [0,0,0,0,0,0,0]
}

# num_change:
## type1: with stick number change
num_switch_stick_change_add = {
                            "0": "8", 
                            "1": "7", 
                            "3": "9", 
                            "5": ["6","9"], 
                            "6": "8", 
                            "9": "8"}

num_switch_stick_change_sub = {
                            "6": "5",
                            "7": "1",
                            "8": ["0", "6", "9"], 
                            "9": ["3", "5"]}

## type2: with stable stick number
num_switch_stick_stable = {
                            "0": ["6", "9"],
                            "2": "3",
                            "3": ["2", "5"],
                            "5": "3",
                            "6": ["0", "9"],
                            "9": ["0", "6"]}

# if with 2 sticks can be changed:
## idea1: list all possible
## idea2: add constrain on the second step which should to be number or None (2 digit with the first one to be None)

# How to input? (not support number <-> operator)
# [int] [op_list] [int] [op_list] [int]

def equation_satisfy(equation):
    if not equation_legal(equation):
        return False
    else:
        if equation_hold(equation):
            return True
        return False

def equation_legal(equation):
    if '=' not in [equation[1], equation[3]]:
        return False
    elif '=' == equation[1] and '=' == equation[3]:
        return False
    else:
        return True

def equation_hold(equation):
    if '=' == equation[1]:
        ans = int(equation[0])
        num_1 = int(equation[2])
        num_2 = int(equation[4])
        op = equation[3]
    else:
        ans = int(equation[4])
        num_1 = int(equation[0])
        num_2 = int(equation[2])
        op = equation[1]
    if op == '+':
        if ans == num_1 + num_2:
            return True
    if op == '-':
        if ans == num_1 - num_2:
            return True
    if op == 'x':
        if ans == num_1 * num_2:
            return True
    return False

def state_switch(switch_list, switch_type, cur_state, element_idx, queue, op = None, digits = None, digit_idx = None):
    
    def num_state_create(digits, digit_idx, cur_state, element_idx, num_switch, switch_type):
        next_digits = copy.deepcopy(digits)
        next_digits[digit_idx] = int(num_switch)
        next_state = copy.deepcopy(cur_state)
        next_state[element_idx] = str(digit_2_num(next_digits))
        next_state[-1] = switch_type
        return next_state

    def op_state_create(cur_state, element_idx, op_switch, switch_type):
        next_state = copy.deepcopy(cur_state)
        next_state[element_idx] = op_switch
        next_state[-1] = switch_type
        return next_state

    if digits:
        try:
            num_switch_list = switch_list[str(digits[digit_idx])]
            if isinstance(num_switch_list, list):
                for num_switch in num_switch_list:
                    queue.inqueue(num_state_create(digits, digit_idx, cur_state, element_idx, num_switch, switch_type))
            else:
                queue.inqueue(num_state_create(digits, digit_idx, cur_state, element_idx, num_switch_list, switch_type))
        except KeyError as Error:
            pass
    else:
        try:
            op_switch_list = switch_list[op]
            if isinstance(op_switch_list, list):
                for op_switch in op_switch_list:
                    queue.inqueue(op_state_create(cur_state, element_idx, op_switch, switch_type))
            else:
                queue.inqueue(op_state_create(cur_state, element_idx, op_switch_list, switch_type))
        except KeyError as Error:
            pass
    return queue

def num_2_digit(num):
    digits = []
    while num // 10:
        next_num = num // 10
        digits.append(num - 10 * next_num)
        num = next_num
    digits.append(num)
    return digits[::-1]

def digit_2_num(digits):
    assert len(digits)>0, "Error during number creation from digit"
    number = 0
    for dex, digit in enumerate(digits[::-1]):
        number += digit*pow(10, dex)
    return number

def BFS_Move_One(equation, is_generate = False):
    queue = myQueue(equation + ['Init'])
    ans = []
    while queue.length() > 0:
        cur_state = queue.outqueue()
        if cur_state[-1] == 'Init':
            for idx, element in enumerate(cur_state[:-1]):
                try:
                    num = int(element)
                    digits = num_2_digit(num)
                    for digit_idx in range(len(digits)):
                        queue = state_switch(num_switch_stick_stable, 'Done', cur_state, idx, queue, 
                                                op=None, digits=digits, digit_idx=digit_idx)
                        queue = state_switch(num_switch_stick_change_sub, 'Add', cur_state, idx, queue, 
                                                op=None, digits=digits, digit_idx=digit_idx)
                        queue = state_switch(num_switch_stick_change_add, 'Sub', cur_state, idx, queue,
                                                op=None, digits=digits, digit_idx=digit_idx)
                except ValueError as opError:
                    queue = state_switch(op_switch_stick_stable, 'Done', cur_state, idx, queue, op=element)
                    queue = state_switch(op_switch_stick_change_sub, 'Add', cur_state, idx, queue, op=element)
                    queue = state_switch(op_switch_stick_change_add, 'Sub', cur_state, idx, queue, op=element)
        if cur_state[-1] == 'Add':
            for idx, element in enumerate(cur_state[:-1]):
                try:
                    num = int(element)
                    digits = num_2_digit(num)
                    for digit_idx in range(len(digits)):
                        queue = state_switch(num_switch_stick_change_add, 'Done', cur_state, idx, queue, 
                                                op=None, digits=digits, digit_idx=digit_idx)
                except ValueError as opError:
                    queue = state_switch(op_switch_stick_change_add, 'Done', cur_state, idx, queue, op=element)
        if cur_state[-1] == 'Sub':
            for idx, element in enumerate(cur_state[:-1]):
                try:
                    num = int(element)
                    digits = num_2_digit(num)
                    for digit_idx in range(len(digits)):
                        queue = state_switch(num_switch_stick_change_sub, 'Done', cur_state, idx, queue, 
                                                op=None, digits=digits, digit_idx=digit_idx)
                except ValueError as opError:
                    queue = state_switch(op_switch_stick_change_sub, 'Done', cur_state, idx, queue, op=element)
        if cur_state[-1] == 'Done':
            if equation_legal(cur_state[:-1]) and equation_hold(cur_state[:-1]) and not is_generate:
                ans.append(cur_state[:-1])
            if equation_legal(cur_state[:-1]) and not equation_hold(cur_state[:-1]) and is_generate:
                ans.append(cur_state[:-1])
    return ans

def list_filter(ans, keep_digits=False, src_equation=None):

    def digit_number_same(num_1, num_2):
        if int(num_1) >= 10 and int(num_2) >= 10:
            return True
        elif int(num_1) < 10 and int(num_2) < 10:
            return True
        else:
            return False

    ans_filted = []
    for answer in ans:
        if answer not in ans_filted:
            if keep_digits:
                if digit_number_same(src_equation[0], answer[0]) and \
                    digit_number_same(src_equation[2], answer[2]) and \
                    digit_number_same(src_equation[4], answer[4]):
                    ans_filted.append(answer)
            else:
                ans_filted.append(answer)
    return ans_filted


if __name__ == "__main__":
    """
    Search Algorithm Part
    """
    # test case:
    number_1 = "78"
    op_1 = "-"
    number_2 = "8"
    op_2 = "="
    number_3 = "87"
    equation = [number_1, op_1, number_2, op_2, number_3]

    # state: number config & operator config & 
    # initial state: input equation + switch state
    # target state: output equation which is correct + switch finish!
    # state switch: type 2 or add type1 with sub type2

    # Try BFS?
    ans = BFS_Move_One(equation)
    if ans:
        ans = list_filter(ans)
        print(ans)
    else:
        print(" >> No Answer under this situation")
    
    # Question Generation
    equation_true=["100"]
    while int(equation_true[-1]) > 99 or int(equation_true[-1]) < 0:
        op = op_cand[randrange(len(op_cand))]
        if op == '+':
            num_1 = randrange(100)
            num_2 = randrange(100)
            answer = num_1 + num_2
        if op == '-':
            num_1 = randrange(100)
            num_2 = randrange(100)
            answer = num_1 - num_2
        else:
            num_1 = randrange(10)
            num_2 = randrange(10)
            answer = num_1 * num_2
        equation_true = [str(num_1), op, str(num_2), "=", str(answer)]
    questions = BFS_Move_One(equation_true, is_generate=True)
    if questions:
        questions = list_filter(questions, keep_digits = True, src_equation=equation_true)
        print(" >> Questions Generation with Answer: " + str(equation_true))
        print(questions)
    else:
        print(" >> No Question under this situation with Answer: " + str(equation_true))