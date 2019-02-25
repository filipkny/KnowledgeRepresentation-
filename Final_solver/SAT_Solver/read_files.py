########################## READ TXT IN DIMACS ##########################
def read_DIMACS_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        # Remove '\n', zeroes, last char and make a list out of it
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip().replace("0", "")[0:-1].split(" ")
    return lines

def init_database(rules):
    """
    Creat initial databace for CNF
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

############################# READ SUDOKU IN DIMACS #################################

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

############################# READ SUDOKU IN TXT (DOTS) #############################

def read_sudokus_file(file):
    '''
    :return: {1:{225, 961, 419, -732, -828, ...}, 2:{...}}
    Set of ground truth values of sudoku 1, 2, ...
    '''
    truth_values = set()
    with open(file, 'r') as f:
        truth_values = dict()
        truth_values[1] = set()
        lines = f.readlines()
        # Remove '\n', zeroes, last char and make a list out of it
        k = 1 # no. of sudoku
        for i in range(len(lines)):
            truth_values[k] = set()
            sudoku = lines[i].rstrip()
            i, j = 1, 1
            for literal in sudoku:
                if literal != '.':
                    truth_values[k].add(i*100 + j*10 + int(literal))
                j+=1
                if j == 10:
                    j=1
                    i+=1
            k+=1
        return truth_values
