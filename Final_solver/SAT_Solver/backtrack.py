import copy

def backtrack(rules, literals_dict, truth_values, split_choice, neg_literal,
              rules_before_split, literals_dict_before_split, truth_values_before_split):
    print('-------------- BACKTRACK ------------')
    exists = False
    for i in range(len(neg_literal)-1, -1, -1):
        if neg_literal[i] == False:
            literal_choice = split_choice[i]
            neg_literal[i] = True
            exists = True
            break
    if exists == True:
        # go back to the old rules
        rules = copy.deepcopy(rules_before_split[literal_choice])
        literals_dict = copy.deepcopy(literals_dict_before_split[literal_choice])
        truth_values = copy.deepcopy(truth_values_before_split[literal_choice])

        # we have to remove all the literals that were produced by literal_choice
        for j in range(len(neg_literal)-1, i - 1, -1):
            del rules_before_split[split_choice[j]]
            del literals_dict_before_split[split_choice[j]]
            del truth_values_before_split[split_choice[j]]
            split_choice.pop(j)
            neg_literal.pop(j)

        # assign the literal with '0'
        truth_values.add(-literal_choice)
    else:
        # the problem can not be solved
        print('The problem can not be solved')
        quit()
    return rules, literals_dict, truth_values, split_choice, neg_literal, \
           rules_before_split, literals_dict_before_split, truth_values_before_split