import random
import copy
import time

start_time = time.time()

def print_sudoku(board):
    print("+" + "---+"*9)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x%10 if x != 0 else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+"*9)

#### CREAT DATABASE FOR RULES
def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        # Remove '\n', zeroes, last char and make a list out of it
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip().replace("0", "")[0:-1].split(" ")
    return lines


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
    assign = '?'
    for idx, clause in enumerate(rules):
        for unknowns, literal in enumerate(clause):
            temp_set = set()
            literal = int(literal)
            disjunction[literal] = assign
            literal = abs(literal)  # get and the negative position
            try:
                assign, temp_set = literals_dict[literal]
                temp_set.add(idx)
            except:
                temp_set.add(idx)
                literals_dict[literal] = [assign, temp_set]
        # temp = [idx, unknowns+1]
        # clauses[tuple(temp)] = disjunction
        rules_dict[idx] = disjunction
        disjunction = dict()
    return rules_dict, literals_dict


### CREAT DATABASE FOR SUDOKU
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


### Get the values ###
rules = read_file("sudoku-rules.txt")
truth_values = read_sudoku_DIMACS_file("sudoku-example.txt")

rules, literals_dict = init_database(rules)


### Step 1: Simplify ###
def simlify(rules, literals_dict, truth_values):
    rules_copy = copy.deepcopy(rules)
    literals_dict_copy = copy.deepcopy(literals_dict)
    new_truth_values = set()
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
                    if len(clause) == zeros:  # it will make the hole think False
                        print('FATALITY: BACKTRACK :/')
                        raise SystemExit
                    elif unknowns == 1:  # if we have (false or false or... or false or ?) => the ? must be true
                        statement = keys[values.index('?')]  # the literal who must be true
                        new_truth_values.add(statement)  ### truth_values HAVE BOTH NEGATIVE AND NON_NEGATIVE literals
                        if statement > 0:  # but because literals_dict has only non-negative, we have to check
                            literals_dict[statement][0] = '1'  # add it to the literals_dict
                            literals_dict[statement][1].remove(i)  # remove position from literals_dict
                        else:
                            literals_dict[-statement][0] = '0'  # add it to the literals_dict
                            literals_dict[-statement][1].remove(i)  # remove position from literals_dict
                        del rules[i]

                    elif len(clause) == 1 and unknowns == 1:  # unit clause
                        statement = keys[0]
                        new_truth_values.add(statement)
                        if statement > 0:
                            literals_dict[statement][0] = '1'  # add it to the literals_dict
                            literals_dict[statement][1].remove(i)  # remove position from literals_dict
                        else:
                            literals_dict[-statement][0] = '0'  # add it to the literals_dict
                            literals_dict[-statement][1].remove(i)  # remove position from literals_dict
                        del rules[i]
            except:
                continue
    truth_values = truth_values.union(new_truth_values)  # join two sets
    return rules, literals_dict, truth_values  # , new_truth_values


def split(literals_dict, truth_values):
    print('------- splitting -------')

    condition = False
    while condition == False:
        rand_literal = random.choice([*literals_dict.keys()])  # random literal
        if literals_dict[rand_literal][0] == '?':
            condition = True
            literals_dict[rand_literal][0] = '1'
            truth_values.add(rand_literal)  # rand_literal will always be non-negative
    return literals_dict, truth_values


print(len(rules))
old_len = len(rules)
new_truth_values = set()
condit = False
while condit == False:
    rules, literals_dict, truth_values = simlify(rules, literals_dict, truth_values)
    print(len(rules))
    new_len = len(rules)
    if new_len == 0:
        print('---------- Solutions ----------')
        solutions = []
        i=0
        for solution in truth_values:
            if solution>0:
                solutions.append(solution)
        solution_grid = []
        for i in range(0, 81, 9):
            solution_grid.append(solutions[i:i + 9])
        print_sudoku(solution_grid)
        print('Solutions are #', i)
        condit = True
    elif old_len - new_len == 0:
        literals_dict, truth_values = split(literals_dict, truth_values)
    else:
        old_len = new_len


print("--- %s seconds ---" % (time.time() - start_time))