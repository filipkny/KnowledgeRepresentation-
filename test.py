import copy
import random


class DB():
    def __init__(self):
        self.original = []
        self.clauses_left = []
        self.truth_values = set()
        self.rules_dict = {}
        self.literals_dict = {}
        self.inconsistent = False
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

    def set_unit_clauses(self):
        new_truths = set()
        for clause in self.original:
            if len(clause) == 1:
                new_truths.add(int(clause[0]))

        self.truth_values = self.truth_values.union(new_truths)

    def check_clause(self, clause_id):
        clause = self.rules_dict[clause_id]

        keys = [*clause.keys()]  # get the keys in a list
        values = [*clause.values()]  # get the values in a list]
        zeros = values.count(False)  # how many False literal there are at this clause
        unknowns = values.count('?')  # how many Unknown literal there are at this clause

        new_truth = None

        if len(values) == zeros:
            self.inconsistent = True
            print("INCONSISTENT")
            return None

        elif len(clause) == 2 :
            key_to_change = [key for key in clause.keys() if clause[key] == '?'][0]
            truth_val = [val for val in clause.values() if val != '?'][0]
            if not truth_val:
                new_truth = key_to_change

        elif unknowns == 1 and True not in [*clause.values()]:
            new_truth = keys[values.index('?')]

        return new_truth

    def remove_clause(self, clause_id):
        literals = [*self.rules_dict[clause_id].keys()]
        for literal in literals:
            self.literals_dict[abs(literal)].remove(clause_id)

        try:
            del self.rules_dict[clause_id]
        except ValueError:
            return

    def simplify(self):
        new_truths = set()
        for val in self.truth_values:
            clauses_containing = list(self.literals_dict[abs(val)])
            for clause_id in clauses_containing:
                clause = self.rules_dict[clause_id]
                if val in [*clause.keys()]:
                    self.remove_clause(clause_id)
                if -val in [*clause.keys()]:
                    clause[-val] = False
                    new_truth = self.check_clause(clause_id)
                    if new_truth:
                        new_truths.add(new_truth)

        return new_truths

    def simplify_until_end(self):
        current_len = len(self.rules_dict)
        old_len = current_len + 1
        while current_len != old_len:
            new_truths = self.simplify()
            self.truth_values = self.truth_values.union(new_truths)
            old_len = current_len
            current_len = len(self.rules_dict)
            print(current_len)

    def calc_unkowns(self):
        return [unk for unk in [*self.literals_dict.keys()] if unk not in self.truth_values and -unk not in self.truth_values]

    def split(self, strat = 'rand'):
        # choose at random
        if strat is 'rand':
            unks = self.calc_unkowns()
            print(len(self.literals_dict))
            print(len(self.truth_values))
            rand_literal = random.choice(unks)
            value = True if random.random() < 0.5 else False

            print("Splitting on {} with value {}".format(rand_literal, value))

        return rand_literal, value

    def save_state(self, literal, value):
        state = [
            copy.deepcopy(self.truth_values),
            copy.deepcopy(self.rules_dict),
            copy.deepcopy(self.literals_dict),
            copy.deepcopy(self.split_list)
        ]
        self.states[(literal, value)] = state
        self.split_list.append((literal, value))

    def restore_state(self, literal, value):
        print("--- Restoring state from literal {} with val {} ----".format(literal, value))
        state = self.states[(literal, value)]
        self.truth_values , self.rules_dict, self.literals_dict,self.split_list =  state

    def verify_and_retry(self):
        solution = [val for val in self.truth_values if val > 0]
        if len(solution) != 81:
            print(" RETRYING ")
            self.restore_last_state()
            self.davis_putna()
            return
        else:
            return

    def restore_last_state(self):
        try:
            print(self.split_list)
            (last_literal, last_val) = self.split_list.pop(-1)
            print(" Restored literal {} with val {} and current length {}".format(last_literal, last_val,len(self.rules_dict)))
            self.inconsistent = False
            self.restore_state(last_literal, last_val)
        except:
            print(" EMPTY SPLIT LIST ")
            states = [*self.states.keys()]
            last_literal, last_val = states[-1]
            print(" Restored literal {} with val {} and current length {}".format(last_literal, last_val,len(self.rules_dict)))
            self.inconsistent = False
            self.restore_state(last_literal, last_val)

    def davis_putna(self):
        self.init_database()
        self.set_unit_clauses()
        while len(self.rules_dict) > 0:
            # Simplify
            self.simplify_until_end()


            # Split
            literal, val = self.split()
            self.save_state(literal, val)


            if val:
                self.truth_values.add(literal)
            else:
                self.truth_values.add(-literal)

            self.simplify_until_end()

            # Backtrack
            if self.inconsistent:
                print("---- REVERSING -----")
                self.restore_state(literal, val)

                if val:
                    self.truth_values.add(-literal)
                else:
                    self.truth_values.add(literal)

                self.simplify_until_end()

                if self.inconsistent:
                    print(" ---- BACKTRACKING -----")
                    self.restore_state(literal, val)
                    continue

        self.verify_and_retry()

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
import time
while True:
    db = DB()
    db.read_file("sudoku-example.txt")
    db.read_file("sudoku-rules.txt")
    db.init_database()
    db.set_unit_clauses()
    db.simplify_until_end()
    db.davis_putna()
    print(db.truth_values)
    assignment = [val for val in db.truth_values if val > 0]
    assert len(assignment) == 81, "Length of assignment is {} and not 81".format(len(assignment))
    # consistent = db.check_inconsistency()
    print(assignment)
    print_sol(assignment)
    time.sleep(1)
    # if not consistent:
    #     print(pprint.pprint(db.literals_dict))
    #     print(pprint.pprint(db.rules_dict))


