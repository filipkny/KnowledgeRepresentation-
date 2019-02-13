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

# Terminology: '1' = True, '0' = False, '?' = Unknown

# pop the element with 'p' and 'cnf' values
if rules[0][0]=='p':
    rules.pop(0)

def rules2dict(rules, str):
    """
    Let A,B and C are the list of rules. Then:
    [[A , B , C] , [D]] = [{A , B , C} , {D}] = {{A or B or C} and {D}}
    where A has the value of the 'str': A = 'str', str = '0', '1', '?'
    """
    clauses = {}
    disjunction = {}
    for idx, clause in enumerate(rules):
        for rule in clause:
            disjunction[int(rule)] = str #int make them integers
        clauses[idx] = disjunction
        disjunction = dict()
    return clauses

# we will assing every rule with '?' because we do not know if it is True or False
rules = rules2dict(rules, '?')

# and every element of the example is True, so we will make a new list 'truth_values',
# that contains only true values
truth_values = set()
for value in example:
    truth_values.add(int(value[0]))

# # Step 1: Assing 1 and 0 to the elements of rules that are in the truth_values
def fill_values(rules, truth_values):
    for idx, clause in rules.items():
        for statement in truth_values:
                if statement in [*clause.keys()]:
                    rules[idx][statement] = '1'
                elif -statement in [*clause.keys()]:
                    rules[idx][-statement] = '0'
    return rules


# Step 2: Simplicity fanction
def simplicity(rules, truth_values):
    rules_copy = rules.copy()
    for idx, clause in rules.items():
        keys = [*clause.keys()]
        values = [*clause.values()]
        ones = values.count('1')
        zeros = values.count('0')
        unknowns = values.count('?')

        if ones>0:
            del rules_copy[idx]

        elif len(clause) == 2 and unknowns == 1:
            if zeros>0:
                statement = keys[values.index('?')]
                rules_copy[idx][statement] = '1'
                truth_values.add(statement)
                del rules_copy[idx]
            else:
                del rules_copy[idx]

        elif len(clause) == 1 and unknowns==1 :
            statement = keys[0]
            rules_copy[idx][statement] = '1'
            truth_values.add(statement)
            del rules_copy[idx]

        elif len(clause) == zeros-1:        # captures the form (false or false or ... or false or ?) -> ? must be true
            statement = keys[values.index('?')]
            rules_copy[idx][statement] = '1'  # rules[idx][statement] = '1'
            del rules_copy[idx]
    return rules_copy, truth_values

def split(rules, truth_values):
    print('----- splitting -------')
    condition = False
    while condition == False:
        rand_idx = random.choice([*rules.keys()])
        rand_clause = rules[rand_idx]
        keys = [*rand_clause.keys()]
        values = [*rand_clause.values()]
        if '?' in values:
            statement = keys[values.index('?')]
            if statement>0:
                truth_values.add(statement)
                condition = True
            else:
                truth_values.add(-statement)
                condition = True
    return truth_values

print(len(rules))

old_len = len(rules)
condition = False
i=1
while condition == False:
    rules = fill_values(rules, truth_values)
    rules, truth_values = simplicity(rules, truth_values)
    new_len = len(rules)
    print(new_len)
    if new_len - old_len == 0:
        truth_values = split(rules, truth_values)
    else:
        old_len = new_len
    if new_len < 100:
        break
    # if i==3:
    #     for idx, clause in rules.items():
    #         print([*clause.values()])
    # i+=1
#
# for idx, clause in rules.items():
#     print([*clause.values()])
# print(len(rules))
#
# rules = fill_values(rules, truth_values)
# rules, truth_values = simplicity(rules, truth_values)
#
# print(len(rules))
# #
# # for idx, clause in rules.items():
# #     print([*clause.values()])
#
# truth_values = split(rules, truth_values)


