import read_files, split, simplify, pretty_print, time

sudokus_1000 = read_files.read_sudokus_file("damnhard.sdk.txt")

start_time = time.time()

for i in range(1, len(sudokus_1000)):
    truth_values = sudokus_1000[i]

    rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
    split_choice, neg_literal = [], []

    rules = read_files.read_DIMACS_file("sudoku-rules.txt")
    rules, literals_dict = read_files.init_database(rules)

    old_len = len(rules)
    print(len(rules))

    # Simplify
    done = False
    while done == False:
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                        rules_before_split, literals_dict_before_split, truth_values_before_split)
        new_len = len(rules)
        print(new_len)
        if new_len == 0 :
            pretty_print.solution(truth_values)
            done = True
            print("--- %s seconds ---" % (time.time() - start_time))
        elif old_len == new_len:
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                  rules_before_split, literals_dict_before_split, truth_values_before_split)
        old_len = new_len






