import copy
import math
from collections import defaultdict
import random
import itertools


def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()

        # Remove '\n', zeroes, last char and make a list out of it
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip().replace("0","")[0:-1].split(" ")

    return lines


example = read_file("sudoku-example.txt")
rules = read_file("sudoku-rules.txt")

print(example)
print(rules)

class SAT():
    def __init__(self,board,rules,size = 9):
        self.board = board
        self.rules = rules
        self.size = size
        self.change_index_dict = {
            "square" : 2,
            "row" : 1,
            "column" : 0
        }
        self.truth_values = defaultdict(lambda : None)
        for assignment in board:
            self.truth_values[str(assignment[0])] = True

        self.ground_truth_cnf = []

    def get_constraints(self, assignment, type):
        if type == "box":
            return self.get_box_constraint(assignment)

        result = []

        # Select which index to change (eg. 111, index 0 -> 211,311,411...)
        change_index = self.change_index_dict[type]

        # Split the assignment on the selected index
        change, keep= self.split_on_index(list(assignment), change_index)

        # Possible values of change index are all integers between 1 and size of the board, besides the current value
        possible_values = list(range(1,self.size+1))
        possible_values.remove(change)

        # Go over all possible values and insert them in the right location. Append results
        for possible_value in possible_values:
            implication = copy.copy(keep)
            implication.insert(change_index, str(possible_value))
            result.append("-" + "".join(implication))

        return result

    def get_box_constraint(self, assignment):
        result = []
        constant = list(assignment)[-1]

        possible_values = list(range(1, int(math.sqrt(self.size)) + 1))

        all_combos = list(itertools.product(possible_values, possible_values))

        for combo in all_combos:
            implication = [str(combo[0]),str(combo[1])] + [str(constant)]
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
        # Find all unit clauses
        unit_clauses = [clause for clause in self.ground_truth_cnf if len(clause) == 1]

        # Set each unit clause values to True
        for clause in unit_clauses:
            proposition = clause[0]
            self.truth_values[proposition] = True

        self.remove_clauses(unit_clauses, self.ground_truth_cnf)

    def update_cnf(self, truth_values, cnf):
        temp_dict = defaultdict(lambda : None)

        clauses_to_remove = []


        for assignment, value in truth_values.items():      # For all truth values
            if value:                                       # If the value is true
                for clause in cnf:                          # For every clause in the cnf
                    if len(clause) == 2:                    # If the clause has length 2
                        for literal in clause:              # Go over each literal of the clause
                            if assignment in literal:       # If the literal is the same as the truth assignment

                                other_literal = copy.copy(clause)
                                other_literal = [ x for x in other_literal if assignment not in x ] # Get the other literal
                                proposition = other_literal[0] # Get it out of the list
                                temp_dict[proposition] = True  # Set the value of this literal to true
                                clauses_to_remove.append(clause) # Put it in the list of clauses to remove

        truth_values = {**truth_values, **temp_dict} # Join the old truth value dictionary with the new one
        cnf = self.remove_clauses(clauses_to_remove, cnf) # Remove the clauses from the current cnf

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
# sat.join_cnf()
print(sat.get_constraints('111','row'))
