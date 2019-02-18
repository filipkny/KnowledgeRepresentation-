import random
import copy

def split(rules, literals_dict, truth_values, split_choice, neg_literal,
           rules_before_split, literals_dict_before_split, truth_values_before_split, which_method=0):
    print('-------- SPLIT --------')
    # Basic DPLL method (random)
    if which_method == 0:
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

    # Jeroslow-Wang method
    elif which_method == 1: # Jeroslow-Wang method 
        # Find all the unsigned literals
        temp_lst_unknows = {}
        for temp_literal in [*literals_dict.keys()]:
            if literals_dict[temp_literal][0] == '?':
                # get the clauses that the literal appears in
                idx_literals_clauses = literals_dict[temp_literal][1]
                # for every clause calculate the length of it: w
                w = 0
                for idx_clause in idx_literals_clauses: # problem: some clauses maybe had been deleted
                    if rules.get(idx_clause) is not None:
                        w += 2 ^ (-len(rules))
                # give the literal a score
                temp_lst_unknows[temp_literal] = w

        keys = [*temp_lst_unknows.keys()]
        values = [*temp_lst_unknows.values()]
        # now get the literal with the maximum w
        max_w = max(values)
        # get the literal
        choosen_literal = keys[values.index(max_w)]

        # keep the rules, literals_dict and truth_values before the split
        rules_before_split[choosen_literal] = copy.deepcopy(rules)
        literals_dict_before_split[choosen_literal] = copy.deepcopy(literals_dict)
        truth_values_before_split[choosen_literal] = copy.deepcopy(truth_values)

        # add it to the dict of split_choices; it is equal to all the changes in the literals that is will cause
        split_choice.append(choosen_literal)
        neg_literal.append(False)

        # update the literals_dict and truth_values with the new literal
        truth_values.add(choosen_literal)  # rand_literal will always be non-negative

        return rules, literals_dict, truth_values, split_choice, neg_literal, \
               rules_before_split, literals_dict_before_split, truth_values_before_split

    # Heuristic 2
    elif which_method == 2:
        print('Heuristic 2')