import read_files, split, simplify, pretty_print, time

sudokus_1000 = read_files.read_sudokus_file("1000_sudokus.txt")

start_time = time.time()

# Choose heuristic: 0 = Basic DPLL (random), 1 = Jeroslow-Wang method, 2 = Heuristic 2
which_method = 1
print_heuristic = ['Basic DPLL (random)', 'Jeroslow-Wang method ', 'Heuristic 2']
print('Heuristic: ', print_heuristic[which_method])

for i in range(1, 2):
    truth_values = sudokus_1000[i]

    rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
    split_choice, neg_literal = [], []

    rules = read_files.read_DIMACS_file("sudoku-rules.txt")
    rules, literals_dict = read_files.init_database(rules)

    old_len = len(rules)
    print('Initial number of clauses:', len(rules))

    finish = False
    while finish == False:
        # Simplify
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                        rules_before_split, literals_dict_before_split, truth_values_before_split)
        new_len = len(rules)
        print(new_len)
        if new_len == 0 :
            # Solution
            pretty_print.solution(truth_values)
            finish = True
            print("--- %s seconds ---" % (time.time() - start_time))
        elif old_len == new_len:
            # Split
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                  rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
        old_len = new_len