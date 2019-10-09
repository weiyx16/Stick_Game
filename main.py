# -*— coding: utf-8 *-*

op = {
    "+": [1,0],
    "-": [0,0],
    "x": [1,1],
    "=": [0,1]}

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
                            "8": ["0", "6", "9"] 
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

"""
Search Algorithm Part
"""
# test case:
number_1 = "6"
op_1 = "+"
number_2 = "4"
op_2 = "="
number_3 = "4"

# state: number config & operator config & 
# initial state: input equation
# target state: output equation which is correct
# state switch: type 2 or add type1 with sub type2

