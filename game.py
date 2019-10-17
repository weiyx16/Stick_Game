# -*— coding: utf-8 *-*
from myQueue import myQueue
import copy
from random import randrange

class Stick_game():
    def __init__(self, equation):
        self.equation=equation
        self.op = {
            "+": [1,0],
            "-": [0,0],
            "x": [1,1],
            "=": [0,1]}
        self.op_cand = ["+", "-", "x"]

        # op_change:
        ## type1: with stick number change
        self.op_switch_stick_change_add = {"-": ["+", "="]}
        self.op_switch_stick_change_sub = {"+": "-", "=": "-"} 
        # - <-> = (only possible in situation with 2 or more sticks moved || A-B=C <-> A=B-C)
        ## type2: with stable stick number
        self.op_switch_stick_stable = {"+": "=", "=": "+"}
        # + <-> = (only possible in situation with 2 or more sticks moved || A=B=C <-> A+B=C or A=B+C)

        self.op_switch_stick_stable_two = {"+": ["x", "="], "x": ["+", "="], "=": ["+", "x"]}
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

        self.num = {
            "0": [1,1,1,0,1,1,1],  #6
            "1": [0,0,1,0,0,1,0],  #2
            "2": [1,0,1,1,1,0,1],  #5
            "3": [1,0,1,1,0,1,1],  #5
            "4": [0,1,1,1,0,1,0],  #4
            "5": [1,1,0,1,0,1,1],  #5
            "6": [1,1,0,1,1,1,1],  #6
            "7": [1,0,1,0,0,1,0],  #3
            "8": [1,1,1,1,1,1,1],  #7
            "9": [1,1,1,1,0,1,1],  #6
            "None" : [0,0,0,0,0,0,0]
        }

        # num_change:
        ## type1: with stick number change
        self.num_switch_stick_change_add = {
                                    "0": "8", 
                                    "1": "7", 
                                    "3": "9", 
                                    "5": ["6","9"], 
                                    "6": "8", 
                                    "9": "8"}

        self.num_switch_stick_change_sub = {
                                    "6": "5",
                                    "7": "1",
                                    "8": ["0", "6", "9"], 
                                    "9": ["3", "5"]}

        ## type2: with stable stick number
        self.num_switch_stick_stable = {
                                    "0": ["6", "9"],
                                    "2": "3",
                                    "3": ["2", "5"],
                                    "5": "3",
                                    "6": ["0", "9"],
                                    "9": ["0", "6"]}

        ## type1: with stick number change
        self.num_switch_stick_change_add_stable = {
                                            "2": ["0", "6", "9"],
                                            "3": ["0", "6"],
                                            "4": ["3", "5"],
                                            "5": "0",
                                            "7": "4"}
        self.num_switch_stick_change_sub_stable = {
                                            "0": ["2", "3", "5"],
                                            "3": "4",
                                            "4": "7",
                                            "5": "4",
                                            "6": ["2", "3"],
                                            "9": "2"}
        self.num_switch_stick_change_add_two = {
                                            "1": "4",
                                            "2": "8",
                                            "3": "8",
                                            "4": "9",
                                            "5": "8",
                                            "7": "3"}
        self.num_switch_stick_change_sub_two = {
                                            "3": "7",
                                            "4": "1",
                                            "8": ["2", "3", "5"],
                                            "9": "4"}       
        ## type1: with stick number change
        self.num_switch_stick_stable_two = {
                                        "2": "5",
                                        "5": "2"}
                            
        # if with 2 sticks can be changed:
        ## idea1: list all possible
        ## idea2: add constrain on the second step which should to be number or None (2 digit with the first one to be None)

        # flag and state switch pair
        ## [a, b] stands for a sticks have been operated in the equation. and b sticks is left unput besides
        ## init: [0, 0], target: [2, 0]
        self.state_switch_flag_num = {
            # number part
            "num_switch_stick_change_add": [0, -1],
            "num_switch_stick_change_sub": [1, 1],
            "num_switch_stick_stable": [1, 0],
            "num_switch_stick_change_add_stable": [1, -1],
            "num_switch_stick_change_sub_stable": [2, 1],
            "num_switch_stick_change_add_two": [0, -2],
            "num_switch_stick_change_sub_two": [2, 2],
            "num_switch_stick_stable_two": [2, 0]}
        self.state_switch_flag_op = {
            # operation part
            "op_switch_stick_stable_two": [2, 0],
            "op_switch_stick_change_add": [0, -1],
            "op_switch_stick_change_sub": [1, 1],
            "op_switch_stick_stable": [1, 0]}

        # How to input? (not support number <-> operator)
        # [int] [op_list] [int] [op_list] [int]

    def equation_update(self, equation):
        self.equation = equation

    def equation_satisfy(self, equation):
        if not self.equation_legal(equation):
            return False
        else:
            if self.equation_hold(equation):
                return True
            return False

    def equation_legal(self, equation):
        if '=' not in [equation[1], equation[3]]:
            return False
        elif '=' == equation[1] and '=' == equation[3]:
            return False
        else:
            return True

    def equation_hold(self, equation):
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

    def state_switch(self, switch_list, switch_type, cur_state, element_idx, queue, op = None, digits = None, digit_idx = None):
        
        def num_state_create(digits, digit_idx, cur_state, element_idx, num_switch, switch_type):
            next_digits = copy.deepcopy(digits)
            next_digits[digit_idx] = int(num_switch)
            next_state = copy.deepcopy(cur_state)
            next_state[element_idx] = str(self.digit_2_num(next_digits))
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

    def next_state_search(self, cur_state, is_num = True):
        def list_add(list_1, list_2=cur_state):
            from operator import add
            return list(map(add, list_1, list_2))
        next_state_list = []
        if is_num:
            search_dict = self.state_switch_flag_num
        else:
            search_dict = self.state_switch_flag_op
        for k, v in search_dict.items():
            cand = list_add(v)
            if cand[0] <= 2 and abs(cand[1]) <= 2 and (cand[0] - cand[1]) <= 2: #[1, -2], [2, -1] is impossible
                next_state_list.append(k)
        return next_state_list

    def num_2_digit(self, num):
        digits = []
        while num // 10:
            next_num = num // 10
            digits.append(num - 10 * next_num)
            num = next_num
        digits.append(num)
        return digits[::-1]

    def digit_2_num(self, digits):
        assert len(digits)>0, "Error during number creation from digit"
        number = 0
        for dex, digit in enumerate(digits[::-1]):
            number += digit*pow(10, dex)
        return number

    def BFS_Move_One(self, is_generate = False, equation_true = None):
        if is_generate:
            queue = myQueue(equation_true + ['Init'])
        else:
            queue = myQueue(self.equation + ['Init'])
        ans = []
        while queue.length() > 0:
            cur_state = queue.outqueue()
            if cur_state[-1] == 'Init':
                for idx, element in enumerate(cur_state[:-1]):
                    try:
                        num = int(element)
                        digits = self.num_2_digit(num)
                        for digit_idx in range(len(digits)):
                            queue = self.state_switch(self.num_switch_stick_stable, 'Done', cur_state, idx, queue, 
                                                    op=None, digits=digits, digit_idx=digit_idx)
                            queue = self.state_switch(self.num_switch_stick_change_sub, 'Add', cur_state, idx, queue, 
                                                    op=None, digits=digits, digit_idx=digit_idx)
                            queue = self.state_switch(self.num_switch_stick_change_add, 'Sub', cur_state, idx, queue,
                                                    op=None, digits=digits, digit_idx=digit_idx)
                    except ValueError as opError:
                        queue = self.state_switch(self.op_switch_stick_stable, 'Done', cur_state, idx, queue, op=element)
                        queue = self.state_switch(self.op_switch_stick_change_sub, 'Add', cur_state, idx, queue, op=element)
                        queue = self.state_switch(self.op_switch_stick_change_add, 'Sub', cur_state, idx, queue, op=element)
            if cur_state[-1] == 'Add':
                for idx, element in enumerate(cur_state[:-1]):
                    try:
                        num = int(element)
                        digits = self.num_2_digit(num)
                        for digit_idx in range(len(digits)):
                            queue = self.state_switch(self.num_switch_stick_change_add, 'Done', cur_state, idx, queue, 
                                                    op=None, digits=digits, digit_idx=digit_idx)
                    except ValueError as opError:
                        queue = self.state_switch(self.op_switch_stick_change_add, 'Done', cur_state, idx, queue, op=element)
            if cur_state[-1] == 'Sub':
                for idx, element in enumerate(cur_state[:-1]):
                    try:
                        num = int(element)
                        digits = self.num_2_digit(num)
                        for digit_idx in range(len(digits)):
                            queue = self.state_switch(self.num_switch_stick_change_sub, 'Done', cur_state, idx, queue, 
                                                    op=None, digits=digits, digit_idx=digit_idx)
                    except ValueError as opError:
                        queue = self.state_switch(self.op_switch_stick_change_sub, 'Done', cur_state, idx, queue, op=element)
            if cur_state[-1] == 'Done':
                if self.equation_legal(cur_state[:-1]) and self.equation_hold(cur_state[:-1]) and not is_generate:
                    ans.append(cur_state[:-1])
                if self.equation_legal(cur_state[:-1]) and not self.equation_hold(cur_state[:-1]) and is_generate:
                    ans.append(cur_state[:-1])
        return ans

    def BFS_Move_Two(self, move_one_ok = False, is_generate = False, equation_true = None):
        
        def list_add(list_1):
            list_2 = cur_state[-1]
            from operator import add
            return list(map(add, list_1, list_2))
        # state_switch_flag_num
        # state_switch_flag_op
        if is_generate:
            queue = myQueue(equation_true + [[0, 0]])
        else:
            queue = myQueue(self.equation + [[0, 0]])
        ans = []
        while queue.length() > 0:
            # queue.show()
            cur_state = queue.outqueue()
            if cur_state[-1] != [2, 0]:
                state_switch_list_num = self.next_state_search(cur_state[-1], is_num=True)
                state_switch_list_op = self.next_state_search(cur_state[-1], is_num=False)
                for idx, element in enumerate(cur_state[:-1]):
                    try:
                        num = int(element)
                        digits = self.num_2_digit(num)
                        for digit_idx in range(len(digits)):
                            for state_pos in state_switch_list_num:
                                queue = self.state_switch(getattr(self, state_pos), list_add(self.state_switch_flag_num[state_pos]), 
                                                    cur_state, idx, queue, op=None, digits=digits, digit_idx=digit_idx)                       
                    except ValueError as opError:
                        for state_pos in state_switch_list_op:
                            queue = self.state_switch(getattr(self, state_pos), list_add(self.state_switch_flag_op[state_pos]), 
                                                cur_state, idx, queue, op=element)
            
            if (move_one_ok and cur_state[-1] == [1, 0]) or (not move_one_ok and cur_state[-1] == [2, 0]):

                if self.equation_legal(cur_state[:-1]) and self.equation_hold(cur_state[:-1]) and not is_generate:
                    ans.append(cur_state[:-1])
                if self.equation_legal(cur_state[:-1]) and not self.equation_hold(cur_state[:-1]) and is_generate:
                    ans.append(cur_state[:-1])
        return ans

    def list_filter(self, ans, keep_digits=False, src_equation=None):

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

    def question_generate(self, is_generate_two = False):
            # Question Generation
        equation_true=["100"]
        while int(equation_true[-1]) > 99 or int(equation_true[-1]) < 0:
            op = play.op_cand[randrange(len(self.op_cand))]
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
        if is_generate_two:
            questions = self.BFS_Move_Two(move_one_ok=False, is_generate=True, equation_true=equation_true)
        else:
            questions = self.BFS_Move_One(is_generate=True, equation_true=equation_true)
        if questions:
            questions = self.list_filter(questions, keep_digits = True, src_equation=equation_true)
            print(" >> Questions Generation with Answer: " + str(equation_true))
            print(questions)
        else:
            print(" >> No Question under this situation with Answer: " + str(equation_true))

    def One_Stick(self):
        ans = self.BFS_Move_One()
        if ans:
            ans = self.list_filter(ans)
            print(ans)
        else:
            print(" >> No Answer under this situation")
    
    def Two_Stick(self, move_one_ok=False):
        ans = self.BFS_Move_Two(move_one_ok)
        if ans:
            ans = self.list_filter(ans)
            if not move_one_ok:
                ans_one = self.BFS_Move_One()
                ans_one = self.list_filter(ans_one)
                ans_tmp = []
                for ans_ in ans:
                    if ans_ not in ans_one:
                        ans_tmp.append(ans_)
                ans = ans_tmp
            print(ans)
        else:
            print(" >> No Answer under this situation")

if __name__ == "__main__":
    """
    Search Algorithm Part
    """
    # test case:
    number_1 = "79"
    op_1 = "+"
    number_2 = "7"
    op_2 = "="
    number_3 = "71"
    equation = [number_1, op_1, number_2, op_2, number_3]
    play = Stick_game(equation) 
    # state: number config & operator config & 
    # initial state: input equation + switch state
    # target state: output equation which is correct + switch finish!
    # state switch: type 2 or add type1 with sub type2
    play.One_Stick()
    play.Two_Stick(False)  # in move one: there's a bug: e.g 79->70->76 (2,0) but in fact from 79 to 76 only 1 stick moved.
    play.question_generate(False)
    play.question_generate(True)