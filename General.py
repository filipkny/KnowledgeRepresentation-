import copy
import random


class DB():
    def __init__(self):
        self.original = []
        self.clauses_left = []
        self.truth_values = set()
        self.backtrack = False
        self.saved = False

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
            if new_truth_val in [*clause.keys()]:
                clause[new_truth_val] = True
                self.remove_clause(clause_id)
            else:
                clause[-new_truth_val] = False
                self.check_clause(clause_id)

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

            if len(clause) == 2:
                key_to_change = [key for key in clause.keys() if clause[key] == '?'][0]
                truth_val = [val for val in clause.values() if val != '?'][0]
                if not truth_val:
                    to_add = key_to_change

                self.remove_clause(clause_id)

            elif unknowns == 1 and True not in [*clause.values()]:
                to_add = keys[values.index('?')]

            elif len(clause)== zeros:
                self.backtrack = True
                return

        except:
            return

        if not backtrack and to_add is not None:
            self.truth_values.add(to_add)

    def check_truth_vals(self):
        truth_vals_copy = copy.copy(self.truth_values)
        for truth_val in truth_vals_copy:
            self.update_one_rules_dict(truth_val)

    def check_all_clauses(self):
        for id, clause in self.rules_dict.items():
            self.check_clause(id)

    def print_clauses_left(self):
        print("{} clauses left".format(len(self.clauses_left)))
        return len(self.clauses_left)

    def split(self):
        unks = self.calc_unkowns()
        rand_literal = random.choice(unks)
        value = True if random.random() < 0.5 else False
        return rand_literal, value

    def save_state(self):
        self.presplit_truth_values = copy.copy(self.truth_values)
        self.presplit_clauses_left = copy.copy(self.clauses_left)
        self.presplit_rules_dict = copy.copy(self.rules_dict)
        self.presplit_literals_dict = copy.copy(self.literals_dict)
        self.saved = True

    def restore_state(self):
        self.truth_values = self.presplit_truth_values
        self.clauses_left = self.presplit_clauses_left
        self.rules_dict = self.presplit_rules_dict
        self.literals_dict = self.presplit_literals_dict
        self.saved = False

    def calc_unkowns(self):
        return [unk for unk in [*self.literals_dict] if unk not in self.truth_values and -unk not in self.truth_values]

    def davis_putnam(self):
        self.init_database()
        self.init_truth_vals()
        num_clauses = self.print_clauses_left()

        while self.print_clauses_left() > 0:
            self.check_truth_vals()
            num_clauses_left_new = self.print_clauses_left()

            # Split
            while num_clauses == num_clauses_left_new:
                print("---- Split -----")
                if not self.saved:
                    self.save_state()

                rand_literal, value = self.split()
                print("Chose random literal {}".format(rand_literal))

                self.update_one_rules_dict(rand_literal)
                self.check_truth_vals()

                num_clauses_left_new = self.print_clauses_left()

                if self.backtrack:
                    self.restore_state()
                else:
                    break


            num_clauses = num_clauses_left_new


# Init all
db = DB()
db.read_file("sudoku-example.txt")
db.read_file("sudoku-rules.txt")
db.davis_putnam()
print(db.truth_values)
