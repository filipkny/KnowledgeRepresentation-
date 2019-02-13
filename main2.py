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
    [[A , B , C] , [D]] = [{A , B , C} , {D}] = [{A or B or C} and {D}]
    where A has the value of the 'str': A = 'str', str = '0', '1', '?'
    """
    conjuctions = []
    disjunction = {}
    for conjuction in rules:
        for rule in conjuction:
            disjunction[rule] = str
        conjuctions.append(disjunction)
        disjunction = dict()
    return conjuctions

# we will assing every rule with '?' because we do not know if it is True or False
rules = rules2dict(rules, '?')

# and every element of the example is True, so we will make a new list 'truth_values',
# that contains only true values
truth_values = example

# Step 1: Assing 1 and 0 to the elements of rules that are in the truth_values
def fill_values(rules, truth_values):
    ''''
    Fill in the rule dictionary with values: '?' -> '0' or '1'
    '''
    for idx, clause in enumerate(rules):            # for every clause of the rules
        for rule in truth_values:                   # for every true rule in truth_values
            temp_rule = (rule[0] + '.')[:-1]        # copy of the ground-truth rule

            if str('-') in temp_rule:               # check if it is a 'no rule'

                if temp_rule in [*clause.keys()]:   # if this ground-truth rule (temp_rule) appears in the clause
                    rules[idx][temp_rule] = '1'     # assing it to '1', True

                temp_not_rule = temp_rule.translate({ord("-"): None}) # get rid of this '-' to check for the opposite
                if temp_not_rule in [*clause.keys()]:
                    rules[idx][temp_not_rule] = '0'
            else:                                   # if the rule is without '-'
                if temp_rule in [*clause.keys()]:
                    rules[idx][temp_rule] = '1'

                temp_not_rule = ('-'+temp_rule )
                if temp_not_rule in [*clause.keys()]:
                    rules[idx][temp_not_rule] = '0'
    return rules

# Step 2: Simplicity fanction
def simplicity(rules, truth_values):
    '''
    Performs the Simplicity rules
    :return: updated rules, current_rules and truth_vailus
    '''
    for clause in rules:
        keys = [*clause.keys()]
        values = [*clause.values()]
        ones = values.count('1')
        zeros = values.count('0')
        unknowns = values.count('?')

        if len(clause) == 1 and unknowns==1 :   # if it is a unit clause
            clause[keys[0]] = '1'               # make it true and
            truth_values.append([keys[0]])      # append it to the truth values
            rules.remove(clause)                # remove the clause

        elif ones>0:                            # if the clause has a least one true value
            rules.remove(clause)                # it makes the hole clause true, so remove it

        elif len(clause) == 2 and unknowns == 1:
            if zeros>0:                                 # if the clause is in the form (not true or ?)
                clause[keys[values.index('?')]] = '1'   # make '?' -> true
                truth_values.append([keys[values.index('?')]])
                rules.remove(clause)
            else:
                rules.remove(clause)

        elif len(clause) == zeros-1:        # captures the form (false or false or ... or false or ?) -> ? must be true
            clause[keys[values.index('?')]] = '1'
            truth_values.append([keys[values.index('?')]])
            rules.remove(clause)
    return rules, truth_values

# ============================== Test it ====================================
# rules = fill_values(rules, truth_values) # get the filled  rules
#
# print(len(rules))
#
# for clause in rules:        # print the filled up rules
#     print([*clause.values()])
#
# rules, truth_values = simplicity(rules, truth_values) # simplify them
#
# print(len(rules))

# ===========================================================================

# ========================== The loop ==========================
condition = False
old_len = len(rules)
while condition == False:
    rules = fill_values(rules, truth_values)
    rules, truth_values = simplicity(rules, truth_values)
    new_len = len(rules)
    print(new_len)
    if old_len - new_len == 0:
        condition = True
    else:
        old_len = new_len
# ==============================================================
# for clause in rules:        # print the filled up rules
#     print([*clause.values()])