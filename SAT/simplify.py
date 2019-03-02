import backtrack

def simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
             rules_before_split, literals_dict_before_split, truth_values_before_split, back_track):
    new_truth_values = set()
    temp_set = set()
    back_track = False
    for literal in truth_values:
        positions = literals_dict[abs(literal)][1]
        for i in positions:
            if rules.get(i) is not None:
                if literal in [*rules[i].keys()]:
                    del rules[i]
                else:
                    rules[i][-literal] = '0'
                    keys = [*rules[i].keys()]
                    values = [*rules[i].values()]
                    zeros = values.count('0')
                    unknowns = values.count('?')
                    if unknowns == 1:
                        statement = keys[values.index('?')]
                        temp_set = temp_set.union(truth_values, new_truth_values)
                        if (statement in temp_set) and (-statement not in temp_set):
                            new_truth_values.add(statement)
                            if statement > 0:
                                literals_dict[statement][0] = '1'
                            else:
                                literals_dict[-statement][0] = '0'
                            del rules[i]
                        elif -statement in temp_set:
                            # BackTrack
                            rules, literals_dict, truth_values, split_choice, neg_literal, \
                            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                                backtrack.backtrack(rules, literals_dict, truth_values, split_choice, neg_literal,
                                                    rules_before_split, literals_dict_before_split,
                                                    truth_values_before_split)
                            back_track = True
                            break
                        else:
                            new_truth_values.add(statement)
                            if statement > 0:
                                literals_dict[statement][0] = '1'
                            else:
                                literals_dict[-statement][0] = '0'
                            del rules[i]
        if back_track == True:
            return rules, literals_dict, truth_values, split_choice, neg_literal,\
                   rules_before_split, literals_dict_before_split, truth_values_before_split, back_track
    if truth_values != {}:
        truth_values = truth_values.union(new_truth_values)
    # else:
    #     truth_values = new_truth_values
    return rules, literals_dict, truth_values, split_choice, neg_literal,\
           rules_before_split, literals_dict_before_split, truth_values_before_split, back_track