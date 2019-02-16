import random
import copy
import time

start_time = time.time()


#### READ FILE ####
def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        # Remove '\n', zeroes, last char and make a list out of it
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip().replace("0", "")[0:-1].split(" ")
    return lines

#### CREATE THE DATABASE ####
def init_database(rules):
    """
    :return:
    rules_dict: {0: {-111: '?', -112: '?'}, 1: {-111: '?', -113: '?'}}
    it has every clause with unic index and the literals with their assignment: '?', '0' or '1'

    literals_dict: {111: ['?', {0, 1, 6, ..., 8991}], , 112: ['?', {0, 1, 9, 10,...}]
    it has ONLY non-negative literals (111 and -111 are the same). Motivation: find the position of both easy
    followed by assignment and a set of their position on the rules
    """
    # pop the element with 'p' and 'cnf' values
    if rules[0][0] == 'p':
        rules.pop(0)
        rules_dict, disjunction, literals_dict = {}, {}, {}
    temp_set = set()
    assign = '?' # we are going to make them all unknowns initially
    for idx, clause in enumerate(rules):
        for unknowns, literal in enumerate(clause):
            temp_set = set()
            literal = int(literal)
            disjunction[literal] = assign
            literal = abs(literal)  # get and the negative position
            try:  # if it was already in the dictionary
                assign, temp_set = literals_dict[literal]
                temp_set.add(idx)
            except:  # if it was not, put it
                temp_set.add(idx)
                literals_dict[literal] = [assign, temp_set]
        rules_dict[idx] = disjunction
        disjunction = dict()
    return rules_dict, literals_dict

### GET THE SAMPLE DATABASE (UNIT CLAUSES) ###
def read_sudoku_DIMACS_file(file):
    '''
    :return: {225, 961, 419, -732, -828, ...}
    Set of ground truth values
    '''
    truth_values = set()
    with open(file, 'r') as f:
        lines = f.readlines()
        # Remove '\n', zeroes, last char and make a list out of it
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip().replace("0", "")[0:-1].split(" ")
            truth_values.add(int(lines[i][0]))
    return truth_values


### SIMPLIFY THE RULES ###
def simlify(rules, literals_dict, truth_values, split_choice, neg_literal, rules_before_split,
            literals_dict_before_split, truth_values_before_split):
    '''
    Given the truth_values, simplify all the rules that that you are able to
    '''
    rules_copy = copy.deepcopy(rules)
    literals_dict_copy = copy.deepcopy(literals_dict)
    new_truth_values = set()
    back_track = False
    for literal in truth_values:
        if literal > 0:  # check if the literal is non-negative
            literals_dict[literal][0] = '1'  # add it to the literals_dict
        else:  # if literal = -111, add the -literal to the literals_dict (literals_dict has non-negative rules)
            literals_dict[-literal][0] = '0'
        positions = literals_dict_copy[abs(literal)][1]  # get its positions of the + and - literal of the rules
        for i in positions:
            try:  # try to see if the clause is there
                clause = rules_copy[i]  # get the clause at position i
                if literal in [*clause.keys()]:
                    del rules[i]  # if the literal is True, the hole clause is true, so remove it
                else:  # if the -literal is in the clause
                    clause[-literal] = '0'  # because literal = True => -literal = True
                    keys = [*clause.keys()]  # get the keys in a list
                    values = [*clause.values()]  # get the values in a list
                    zeros = values.count('0')  # how many False literal there are at this clause
                    unknowns = values.count('?')  # how many Unknown literal there are at this clause
                    if len(clause) == zeros:  # it will make the hole thing False
                        print('------ BACKTRACK -----')
                        rules, literals_dict, truth_values, neg_literal, split_choice, \
                        rules_before_split, literals_dict_before_split, truth_values_before_split = \
                            backtrack(literals_dict, truth_values, split_choice, neg_literal, rules_before_split,
                                      literals_dict_before_split, truth_values_before_split)
                        back_track = True
                        # now if we made a backtrack, we have to continue
                        continue
                    elif unknowns == 1:  # if we have (false or false or... or false or ?) => the ? must be true
                        statement = keys[values.index('?')]  # the literal who must be true
                        new_truth_values.add(statement)  ### truth_values HAVE BOTH NEGATIVE AND NON_NEGATIVE literals
                        if statement > 0:  # but because literals_dict has only non-negative, we have to check
                            literals_dict[statement][0] = '1'  # add it to the literals_dict
                        else:
                            literals_dict[-statement][0] = '0'  # add it to the literals_dict
                        del rules[i]

                    elif len(clause) == 1 and unknowns == 1:  # unit clause
                        statement = keys[0]
                        new_truth_values.add(statement)
                        if statement > 0:
                            literals_dict[statement][0] = '1'
                        else:
                            literals_dict[-statement][0] = '0'
                        del rules[i]
            except:
                continue
            if back_track == True:
                continue
        if back_track == True:
            continue
    if back_track != True:
        truth_values = truth_values.union(new_truth_values)  # join two sets
    return rules, literals_dict, truth_values  # , new_truth_values


def split(rules, literals_dict, truth_values, split_choice, neg_literal, rules_before_split,
          literals_dict_before_split, truth_values_before_split):
    print('------- SPLIT -------')
    condition = False
    temp_lst_unknows = []
    for temp_literal in [*literals_dict.keys()]:
        if literals_dict[temp_literal][0] == '?':
            temp_lst_unknows.append(temp_literal)
            rand_literal = random.choice(temp_lst_unknows)

            # add it to the dict of split_choices; it is equal to all the changes in the literals that is will cause
            split_choice.append(rand_literal)
            neg_literal.append(False)

            # keep the rules, literals_dict and truth_values before the split
            rules_before_split[rand_literal] = copy.deepcopy(rules)
            literals_dict_before_split[rand_literal] = copy.deepcopy(literals_dict)
            truth_values_before_split[rand_literal] = copy.deepcopy(truth_values)

            # update the literals_dict and truth_values with the new literal
            literals_dict[rand_literal][0] = '1'
            truth_values.add(rand_literal)  # rand_literal will always be non-negative

            break


    return rules, literals_dict, truth_values, split_choice, neg_literal, rules_before_split, \
           literals_dict_before_split, truth_values_before_split


def backtrack(literals_dict, truth_values, split_choice, neg_literal, rules_before_split,
              literals_dict_before_split, truth_values_before_split):
    if neg_literal[-1] == False:  # if we haven't tried to set it to '0'
        # find literal
        literal_choice = split_choice[-1]
        neg_literal[-1] = True

        # go back to the old rules of the literal
        rules = copy.deepcopy(rules_before_split[literal_choice])
        literals_dict = copy.deepcopy(literals_dict_before_split[literal_choice])
        truth_values = copy.deepcopy(truth_values_before_split[literal_choice])

        # assign the literal with '0'
        literals_dict[literal_choice][0] = '0'
        truth_values.add(-literal_choice)
    else:  # if we tried to set it to '0', we have to go back
        for i in range(len(neg_literal) - 1, -1, -1):
            if neg_literal[i] == False:
                literal_choice = split_choice[i]
                neg_literal[i] = True
                condition = True
                break
        if condition == True:
            # go back to the old rules
            rules = copy.deepcopy(rules_before_split[literal_choice])
            literals_dict = copy.deepcopy(literals_dict_before_split[literal_choice])
            truth_values = copy.deepcopy(truth_values_before_split[literal_choice])

            # we have to remove all the literals that were produced by literal_choice
            for j in range(len(neg_literal) - 1, i - 1, -1):
                del rules_before_split[split_choice[j]]
                del literals_dict_before_split[split_choice[j]]
                del truth_values_before_split[split_choice[j]]
                split_choice.pop(j)
                neg_literal.pop(j)

            # assign the literal with '0'
            literals_dict[literal_choice][0] = '0'
            truth_values.add(-literal_choice)

        else:
            # the problem can not be solved
            print('the problem can not be solved???')

    return rules, literals_dict, truth_values, neg_literal, split_choice, rules_before_split, \
           literals_dict_before_split, truth_values_before_split



def print_sudoku(board):
    print("+" + "---+" * 9)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |" * 3).format(*[x % 10 if x != 0 else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+" * 9)


def solution():
    print("--- %s seconds ---" % (time.time() - start_time))
    print('')
    print('-------------- Solution -------------')
    solutions = []
    for solution in truth_values:
        if solution > 0:
            solutions.append(solution)
    solution_grid = []
    for i in range(0, 81, 9):
        solution_grid.append(solutions[i:i + 9])
    print_sudoku(solution_grid)
    return True



### Get the values ###
rules = read_file("sudoku-rules.txt")
truth_values = read_sudoku_DIMACS_file("sudoku-example.txt")

rules, literals_dict = init_database(rules)
split_choice, neg_literal = [], []
rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}

print(len(rules))
old_len = len(rules)
new_truth_values = set()
ending = False

while ending == False:
    rules, literals_dict, truth_values = \
        simlify(rules, literals_dict, truth_values, split_choice, neg_literal, rules_before_split,
                literals_dict_before_split, truth_values_before_split)

    new_len = len(rules)
    print(len(rules))
    if new_len == 0:
        ending = solution()

    elif old_len - new_len == 0:

        rules, literals_dict, truth_values, split_choice, neg_literal, rules_before_split, \
        literals_dict_before_split, truth_values_before_split = \
            split(rules, literals_dict, truth_values, split_choice, neg_literal, rules_before_split,
                  literals_dict_before_split, truth_values_before_split)
    else:
        old_len = new_len