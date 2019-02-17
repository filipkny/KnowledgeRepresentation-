import random
import copy

def split(rules, literals_dict, truth_values, split_choice, neg_literal,
           rules_before_split, literals_dict_before_split, truth_values_before_split):
    print('------- SPLIT -------')
    temp_lst_unknows = []
    for temp_literal in [*literals_dict.keys()]:
        if literals_dict[temp_literal][0] == '?':
            temp_lst_unknows.append(temp_literal)

    # random choice
    rand_literal = random.choice(temp_lst_unknows)

    # keep the rules, literals_dict and truth_values before the split
    rules_before_split[rand_literal] = copy.deepcopy(rules)
    literals_dict_before_split[rand_literal] = copy.deepcopy(literals_dict)
    truth_values_before_split[rand_literal] = copy.deepcopy(truth_values)

    # add it to the dict of split_choices; it is equal to all the changes in the literals that is will cause
    split_choice.append(rand_literal)
    neg_literal.append(False)

    # update the literals_dict and truth_values with the new literal
    truth_values.add(rand_literal)  # rand_literal will always be non-negative

    return rules, literals_dict, truth_values, split_choice, neg_literal, \
           rules_before_split, literals_dict_before_split, truth_values_before_split