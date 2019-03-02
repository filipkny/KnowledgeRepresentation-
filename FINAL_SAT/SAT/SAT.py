import read_files, split, simplify, pretty_print, check_sudoku
import time, sys


def solve(heuristic, file):
    start = time.time()
    heuristics = {
        0: "Random",
        1: "Jeroslaw",
        2: "MOMs"
    }

    print("Solving using {} heuristic".format(heuristics[int(heuristic)]))

    #truth_values = sudokus[sdk] # {} when we submit
    rules = read_files.read_DIMACS_file(file)
    truth_values = set()
    to_remove = []
    for rule in rules:
        if len(rule) == 1:
            truth_values.add(int(rule[0]))

    for rule in to_remove:
        rules.remove(rule)

    which_method = int(heuristic)

    # List for data analysis EXCEL
    # [#unit_clauses, %of reduction from first simplify, #splits, #backtrackings, #time]
    results = [0, 0, 100., 0, 0, 0]
    results[1] = len(truth_values)
    split_count = 0
    back_track_count = 0
    problem_start_time = time.time()
    rules = read_files.read_DIMACS_file("sdks/sudoku-rules.txt")
    rules, literals_dict, temp = read_files.init_database(rules)
    old_clauses_count = len(rules)
    done = False
    rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
    split_choice, neg_literal = [], []

    while done == False:
        back_track = False
        # Simplify
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split, back_track = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                              rules_before_split, literals_dict_before_split, truth_values_before_split, back_track)
        new_clauses_count = len(rules)
        if split_count > 2000:
            break

        if back_track:
            back_track_count += 1

        if new_clauses_count == 0:
            pretty_print.solution(truth_values)
            results[3] = split_count
            results[4] = back_track_count
            results[5] = float("{0:.2f}".format(time.time() - problem_start_time))
            print("Solved in {0:.2f}s".format(time.time() - problem_start_time))
            print("# splits {}".format(split_count))
            done = True


        elif old_clauses_count == new_clauses_count and back_track == False:
            split_count += 1
            # Split
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                            rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
        old_clauses_count = new_clauses_count

heuristic = sys.argv[1][2]
file = sys.argv[2]
solve(heuristic,file)