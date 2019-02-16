import copy
import random


class DB():
    def __init__(self):
        self.original = []
        self.clauses_left = []
        self.truth_values = set()
        self.rules_dict = {}
        self.literals_dict = {}
        self.backtrack = False
        self.saved = False
        self.reversed = False
        self.split_list = []
        self.states = {}

    def init_database(self):
        """
        :return:
        rules_dict: {0: {-111: '?', -112: '?'}, 1: {-111: '?', -113: '?'}}
        it has every clause with unic index and the literals with their assignment: '?', '0' or '1'

        literals_dict: {111: ['?', {0, 1, 6, ..., 8991}], , 112: ['?', {0, 1, 9, 10,...}]
        it has ONLY non-negative literals (111 and -111 are the same). Motivation: find the position of both easy
        followed by assignment and a set of their position on the rules
        """

        rules_dict, literals_dict = {}, {}
        assign = '?'
        self.clauses_left = []
        for idx, clause in enumerate(self.original):
            disjunction = dict()
            self.clauses_left.append(idx)
            for unknowns, literal in enumerate(clause):
                temp_set = set()
                literal = int(literal)
                disjunction[literal] = assign
                literal = abs(literal)  # get and the negative position
                try:
                    temp_set = literals_dict[literal]
                    temp_set.add(idx)
                except:
                    temp_set.add(idx)
                    literals_dict[literal] = temp_set

            rules_dict[idx] = disjunction

        self.rules_dict = rules_dict
        self.literals_dict = literals_dict

    def read_file(self,file):
        with open(file, 'r') as f:
            lines = f.readlines()
            # Remove '\n', zeroes, last char and make a list out of it
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip().replace("0", "")[0:-1].split(" ")

        if len(self.original) == 0:
            self.original = lines
        else:
            self.original.extend(lines)

        self.original = [ele for ele in self.original if 'p' not in ele]

    def init_truth_vals(self):
        for clause in self.original:
            if len(clause) == 1:
                self.update_one_rules_dict(int(clause[0]))

    def update_one_rules_dict(self, new_truth_val):
        clauses = self.literals_dict[abs(new_truth_val)]
        self.truth_values.add(new_truth_val)
        for clause_id in clauses:
            clause = self.rules_dict[clause_id]

            if not self.backtrack:
                if new_truth_val in [*clause.keys()]:
                    clause[new_truth_val] = True
                    self.remove_clause(clause_id)
                else:
                    clause[-new_truth_val] = False
                    self.check_clause(clause_id)
            else:
                return

    def remove_clause(self, clause_id):
        try:
            self.clauses_left.remove(clause_id)
        except ValueError:
            return

    def check_clause(self, clause_id):
        clause = self.rules_dict[clause_id]
        backtrack = False
        to_add = None
        try:
            keys = [*clause.keys()]  # get the keys in a list
            values = [*clause.values()]  # get the values in a list]
            zeros = values.count(False)  # how many False literal there are at this clause
            unknowns = values.count('?')  # how many Unknown literal there are at this clause

            if len(values) == zeros:
                self.backtrack = True
                print("INCONSISTENT")
                return

            elif len(clause) == 2 and len(clause.keys()) != zeros:
                key_to_change = [key for key in clause.keys() if clause[key] == '?'][0]
                truth_val = [val for val in clause.values() if val != '?'][0]
                if not truth_val:
                    to_add = key_to_change

                self.remove_clause(clause_id)

            elif unknowns == 1 and True not in [*clause.values()]:
                to_add = keys[values.index('?')]

        except:
            return

        if not backtrack and to_add is not None:
            self.truth_values.add(to_add)

    def simplify(self):
        truth_vals_copy = copy.deepcopy(self.truth_values)
        for truth_val in truth_vals_copy:
            if not self.backtrack:
                self.update_one_rules_dict(truth_val)
            else:
                return

    def check_all_clauses(self):
        for id, clause in self.rules_dict.items():
            self.check_clause(id)

    def print_clauses_left(self, printing):
        if printing:
            print("{} clauses left".format(len(self.clauses_left)))
        return len(self.clauses_left)

    def split(self, rand_literal = None, value = None):
        # choose at random
        if rand_literal is None and value is None:
            unks = self.calc_unkowns()
            rand_literal = random.choice(unks)
            value = True if random.random() < 0.5 else False

        print("Splitting on {} with value {}".format(rand_literal, value))
        return rand_literal, value

    def save_state(self, literal, value):
        if self.check_inconsistency():
            state = [
                copy.deepcopy(self.truth_values),
                copy.deepcopy(self.clauses_left),
                copy.deepcopy(self.rules_dict),
                copy.deepcopy(self.literals_dict)
            ]
            self.states[(literal, value)] = state
            self.split_list.append((literal, value))
        else:
            last_state = self.split_list[-1]
            literal = last_state[0]
            value = last_state[1]
            self.restore_state(literal, value)

    def restore_state(self, literal, value):
        print("--- Restoring state from literal {} with val {} ----".format(literal, value))
        state = self.states[(literal, value)]
        self.truth_values ,self.clauses_left, self.rules_dict, self.literals_dict =  state

    def calc_unkowns(self):
        return [unk for unk in [*self.literals_dict] if unk not in self.truth_values and -unk not in self.truth_values]

    def check_inconsistency(self):
        consistent = True
        for clause_id, clause in self.rules_dict.items():
            if len(clause) == [*clause.values()].count(False):
                print("----- INCONSISTENT ------")
                print(clause_id, clause)
                consistent = False

        return consistent
    def simplify_to_end(self, current_clause_left):
        while self.print_clauses_left(False) != current_clause_left:
            current_clause_left = self.print_clauses_left(False)
            self.simplify()
            self.print_clauses_left(True)

        return True

    def davis_putnam(self):
        self.init_database()
        self.init_truth_vals()
        num_clauses = self.print_clauses_left(True)

        while num_clauses > 0:
            # Simplify
            split = self.simplify_to_end(num_clauses + 1)
            num_clauses_left_new = self.print_clauses_left(False)

            # 1. Backtrack
            if self.backtrack:
                print("---- Backtracking ----")
                last_state = self.split_list[-1]
                literal = last_state[0]
                value = last_state[1]
                self.restore_state(literal, value)
                self.split_list.remove((literal, value))
                print("Going into a new split now")
                split = True

                if self.print_clauses_left(False)  == 0:
                    break

            # 2. Split
            if split:

                self.backtrack = False
                print("---- Split -----")

                if self.print_clauses_left(False)  == 0:
                    break

                rand_literal, value = self.split()
                self.save_state(rand_literal, value)

                if value is True:
                    self.update_one_rules_dict(rand_literal)
                else:
                    self.update_one_rules_dict(-rand_literal)


                self.simplify_to_end(num_clauses)

                print(" should reverse now")
                if self.backtrack:
                    print("--- Reversing ----")
                    self.backtrack = False
                    self.restore_state(rand_literal, value)

                    if value is True:
                        print("Setting {} to {}".format(rand_literal, False))
                        self.update_one_rules_dict(-rand_literal)
                    else:
                        print("Setting {} to {}".format(rand_literal, True))
                        self.update_one_rules_dict(rand_literal)

                    self.simplify()

                    if self.backtrack:
                        continue
                    else:
                        if self.print_clauses_left(False) == 0:
                            break
                        else:
                            continue


            num_clauses = num_clauses_left_new

import pprint
def print_sudoku(board):
    print("+" + "---+" * 9)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |" * 3).format(*[x % 10 if x != 0 else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+" * 9)

def print_sol(sol):
    solution_grid = []
    for i in range(0, 81, 9):
        solution_grid.append(sol[i:i + 9])
    print_sudoku(solution_grid)

# Init all
while True:
    db = DB()
    db.read_file("sudoku-example.txt")
    db.read_file("sudoku-rules.txt")
    db.davis_putnam()
    assignment = [val for val in db.truth_values if val > 0]
    consistent = db.check_inconsistency()
    print(assignment)
    print_sol(assignment)
    # if not consistent:
    #     print(pprint.pprint(db.literals_dict))
    #     print(pprint.pprint(db.rules_dict))
    assert len(assignment) == 81, "Length of assignment is {} and not 81".format(len(assignment))


