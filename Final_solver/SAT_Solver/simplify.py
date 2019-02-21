import backtrack

def simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
             rules_before_split, literals_dict_before_split, truth_values_before_split, count_backtracks):
    new_truth_values = set()
    back_track = False
    for literal in truth_values:
        positions = literals_dict[abs(literal)][1]
        for i in positions:
            if rules.get(i) is not None:
                clause = rules[i]
                if literal in [*clause.keys()]:
                    if literal > 0:
                        literals_dict[literal][0] = '1'
                    else:
                        literals_dict[-literal][0] = '0'

                    del rules[i]
                else:
                    clause[-literal] = '0'
                    keys = [*clause.keys()]
                    values = [*clause.values()]
                    zeros = values.count('0')
                    unknowns = values.count('?')
                    if len(clause) == zeros:
                        # BackTrack
                        rules, literals_dict, truth_values, split_choice, neg_literal, \
                        rules_before_split, literals_dict_before_split, truth_values_before_split = \
                            backtrack.backtrack(rules, literals_dict, truth_values, split_choice, neg_literal,
                            rules_before_split, literals_dict_before_split, truth_values_before_split)
                        back_track = True
                        # update backtrack counter
                        count_backtracks += 1
                        break

                    elif len(clause) == 1 and unknowns == 1:  # unit clause
                        statement = keys[0]
                        new_truth_values.add(statement)
                        del rules[i]

                    elif unknowns == 1:
                        statement = keys[values.index('?')]
                        new_truth_values.add(statement)
                        if statement > 0:
                            literals_dict[statement][0] = '1'
                        else:
                            literals_dict[-statement][0] = '0'
        if back_track == True:
            return rules, literals_dict, truth_values, split_choice, neg_literal,\
                   rules_before_split, literals_dict_before_split, truth_values_before_split, count_backtracks
    if truth_values != {}:
        truth_values = truth_values.union(new_truth_values)
    else:
        truth_values = new_truth_values
    return rules, literals_dict, truth_values, split_choice, neg_literal,\
           rules_before_split, literals_dict_before_split, truth_values_before_split, count_backtracks