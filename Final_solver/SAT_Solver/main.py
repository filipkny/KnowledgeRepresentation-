import read_files, split, simplify, pretty_print, time

sudokus = read_files.read_sudokus_file("1000_sudokus.txt")

start_time = time.time()

# Choose heuristic: 0 = Basic DPLL (random), 1 = Jeroslow-Wang method, 2 = Heuristic 2
which_method = 0

print('============ SAT Solver =============')
print_heuristic = ['Basic DPLL (random)', 'Jeroslow-Wang method ', 'Heuristic 2']
print('Heuristic: ', print_heuristic[which_method])
print('=====================================\n')

for i in range(1, 2):
    problem_start_time = time.time()

    truth_values = sudokus[i]

    rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
    split_choice, neg_literal = [], []

    rules = read_files.read_DIMACS_file("sudoku-rules.txt")
    rules, literals_dict = read_files.init_database(rules)

    print('======== SAT Problem: {}/{} ========'.format(i, len(sudokus)))
    old_len = len(rules)
    print('   Initial number of rules:', len(rules), '\n')

    finish = False
    while finish == False:
        # Simplify
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                        rules_before_split, literals_dict_before_split, truth_values_before_split)

        new_len = len(rules)
        print('   #clauses: after simplify:', new_len, end='\r')

        if new_len == 0 :
            # Solution
            pretty_print.solution(truth_values)
            finish = True
            print("\nTime:    %.2f seconds " % (time.time() - problem_start_time))
            print("Runtime: %.2f seconds " % (time.time() - start_time))
            print('=====================================\n')
        elif old_len == new_len:
            # Split
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                  rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
        old_len = new_len