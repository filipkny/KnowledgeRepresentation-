import read_files, split, simplify, pretty_print

rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
split_choice, neg_literal = [], []

# SDKS
# easy_sdk = "sdks/1000_sudokus.txt"
# hard_sdk = 'sdks/damnhard.sdk.txt'
# sdk_rules = "sdks/sudoku-rules.txt"
# sudokus = read_files.read_sudokus_file(hard_sdk)
# truth_values = sudokus[27]
# rules = read_files.read_DIMACS_file(sdk_rules)
# rules, literals_dict = read_files.init_database(rules)

# SAT
sat = 'sat/uf20/uf20-06.txt'
DIMACS = read_files.read_DIMACS_file('sudoku.txt')
rules, literals_dict, truth_values = read_files.init_database(DIMACS)

# Choose heuristic: 0 = Basic DPLL (random), 1 = Jeroslow-Wang method, 2 = MOMs method
which_method = 1

print('============ SAT Solver =============')
print_heuristic = ['Basic DPLL (random)', 'Jeroslow-Wang method ', 'MOMs method']
print('    Heuristic: ', print_heuristic[which_method])
print('=====================================\n')

old_clauses_count = len(rules)
while True:
    back_track = False
    # Simplify
    rules, literals_dict, truth_values, split_choice, neg_literal, \
    rules_before_split, literals_dict_before_split, truth_values_before_split, back_track = \
        simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                          rules_before_split, literals_dict_before_split, truth_values_before_split,back_track)
    new_clauses_count = len(rules)

    if new_clauses_count == 0:
        pretty_print.solution(truth_values)
        print(truth_values)
        print(len(truth_values))
        quit()

    elif old_clauses_count == new_clauses_count and back_track == False:
        # Split
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split = \
            split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                        rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
    old_clauses_count = new_clauses_count