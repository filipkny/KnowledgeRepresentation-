import copy
import math
from collections import defaultdict
import random

def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
            lines[i] = lines[i].replace("0","")
            lines[i] = lines[i][0:-1]
            lines[i] = lines[i].split(" ")

    return lines


example = read_file("sudoku-example.txt")
rules = read_file("sudoku-rules.txt")

class SAT():
    def __init__(self,board,rules,size = 4):
        self.board = board
        self.rules = rules
        self.size = size
        self.index_dict = {
            "square" : 2,
            "row" : 1,
            "column" : 0
        }
        self.truth_values = defaultdict(lambda : False)
        for assignment in board:
            self.truth_values[str(assignment[0])] = True

        self.ground_truth_cnf = []

    def get_constraints(self, assignment, type):
        if type == "box":
            return self.get_box_constraint(assignment)

        result = []
        index = self.index_dict[type]
        split_assignment = list(assignment)
        value, pos = self.split_on_index(split_assignment, index)

        possible_values = list(range(1,self.size+1))
        possible_values.remove(value)

        for possible_value in possible_values:
            implication = copy.copy(pos)
            implication.insert(index, str(possible_value))
            result.append("-"+ "".join(implication))

        return result

    def get_box_constraint(self, assignment):
        result = []
        split_assignment = list(assignment)
        constant = split_assignment[-1]
        first_possible_values = list(range(1, int(math.sqrt(self.size)) + 1))
        second_possible_values = list(range(1, int(math.sqrt(self.size)) + 1))

        import itertools
        combos = list(itertools.product(first_possible_values, second_possible_values))
        for combo in combos:
            implication = [str(combo[0]),str(combo[1])] + [str(constant)]
            print(implication)
            result.append("-" + "".join(implication))

        return result

    def split_on_index(self, assigment, index):
        change = assigment[index]
        keep = copy.copy(assigment)
        keep.remove(change)

        return int(change), keep

    def init_ground_truth_cnf(self):
        self.ground_truth_cnf = copy.copy(self.rules)
        print("Length of board rules: {}".format(len(self.ground_truth_cnf)))

        self.ground_truth_cnf.extend(self.board)
        self.ground_truth_cnf.pop(0)
        print("Length of board rules + rules: {}".format(len(self.ground_truth_cnf)))

    def join_cnf(self):
        self.init_ground_truth_cnf()

        self.set_unit_clause()
        print("Length after removing unit clauses {}".format(len(self.ground_truth_cnf)))

        old_len = len(self.ground_truth_cnf)
        new_len = len(self.ground_truth_cnf) +1
        while old_len != new_len:
            self.ground_truth_cnf, self.truth_values = self.update_cnf(self.truth_values, self.ground_truth_cnf)
            print("Length after updating cnf {}".format(len(self.ground_truth_cnf)))
            old_len = new_len
            new_len = len(self.ground_truth_cnf)

        # # Split
        # split_choice = self.split()
        #
        # temp_truth_vals = copy.copy(self.truth_values)
        # temp_truth_vals[split_choice] = True
        # temp_cnf = copy.copy(self.ground_truth_cnf)
        # new_cnf, new_truth_values = self.update_cnf(temp_truth_vals, temp_cnf)
        # print("Length after updating cnf {}".format(len(temp_cnf)))

    def set_unit_clause(self):
        unit_clauses = [clause for clause in self.ground_truth_cnf if len(clause) == 1]
        for clause in unit_clauses:
            proposition = clause[0]
            self.truth_values[proposition] = True

        self.remove_clauses(unit_clauses, self.ground_truth_cnf)

    def update_cnf(self, truth_values, cnf):
        temp_dict = defaultdict(lambda : False)
        clauses_to_remove = []
        for assignment, value in truth_values.items():
            if value:
                for clause in cnf:
                    if len(clause) == 2:
                        for element in clause:
                            if assignment in element:
                                other = copy.copy(clause)
                                other = [ x for x in other if assignment not in x ]
                                proposition = other[0]
                                temp_dict[proposition] = True
                                clauses_to_remove.append(clause)

        truth_values = {**truth_values, **temp_dict}
        cnf = self.remove_clauses(clauses_to_remove, cnf)

        return cnf,truth_values

    def remove_clauses(self,clauses, cnf):
        for clause in clauses:
            try:
                cnf.remove(clause)
            except ValueError:
                continue

        return cnf

    def split(self, heuristic = "rand"):
        all_assigments = [item for sublist in self.ground_truth_cnf for item in sublist]
        choice = random.choice(all_assigments)
        choice = choice.replace("-","")
        return choice


sat = SAT(example, rules)
# test = "111"
# print("For assignment : " + test)
# print(sat.get_constraints(test,"box"))
sat.join_cnf()
