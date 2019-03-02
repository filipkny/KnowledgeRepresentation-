########################## READ TXT IN DIMACS ##########################
def read_DIMACS_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        # Remove '\n', zeroes, last char and make a list out of it
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()[0:-1].split(" ")
            del lines[i][-1]
    return lines

def init_database(rules):
    # pop the element with 'p' and 'cnf' values
    if rules[0][0] == 'p':
        rules.pop(0)
    rules_dict, disjunction, literals_dict = {}, {}, {}
    truth_values = set()
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
        if len(disjunction) == 1:
            truth_values.add(literal)
            if literal > 0:
                literals_dict[literal][0] = '1'
            else:
                literals_dict[-literal][0] = '0'
        rules_dict[idx] = disjunction
        disjunction = dict()
    return rules_dict, literals_dict, truth_values

############################# READ SUDOKU IN DIMACS #################################

def read_sudoku_DIMACS_file(file):
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