import read_files, split, simplify, pretty_print, check_sudoku
import time, sys


def solve(heuristic, file):
    start = time.time()

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
    results = [1 ,0, 100., 0, 0, 0, 0]
    split_count = 0
    # Position 0: get the #unit_clauses
    results[1] = len(truth_values)

    rules_before_split, literals_dict_before_split, truth_values_before_split= {}, {}, {}
    split_choice, neg_literal = [], []

    rules, literals_dict = read_files.init_database(rules)

    clauses = len(rules)
    variables = len(truth_values)
    old_len = len(rules)
    print('   Initial number of rules:', len(rules), '\n')

    # We need it for data analysis
    init_len_clauses = len(rules)

    finish = False
    while finish == False:
        # Simplify
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split, results[4] = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                        rules_before_split, literals_dict_before_split, truth_values_before_split, results[4])
        new_len = len(rules)
        print('    #clauses: after simplify:', new_len, end='\r')
        if new_len == 0 :
            # Solution
            if not check_sudoku.check_sudoku(sorted(list([val for val in truth_values if val > 0]))):
                print(list(truth_values))
                print(type(list(truth_values)[0]))

                pretty_print.solution(truth_values)
                quit()

            pretty_print.solution(truth_values)
            finish = True

            # get the solution time
            results[5] = float("{0:.2f}".format(time.time() - start))
            print("Runtime: %.2f seconds " % (time.time() - start))
            print("Initial #unit clauses :",results[1] )
            print("Reduction from first simplify: ", results[2], '%')
            print("#splits :",results[3] )
            print("#backtrackings :",results[4] )
            print("clauses: {}, variables: {}, ratio {}".format(clauses,variables,float(clauses)/float(variables)))
            print('=====================================\n')

            results[6] = float(clauses)/float(variables)

        elif old_len == new_len:
            # update #splits
            results[3] = results[3] + 1

            # %of reduction from first simplify
            if results[3] == 1:
                results[2] = float("{0:.2f}".format(100*(init_len_clauses - new_len)/(init_len_clauses + new_len)))

            # Split
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                  rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)

        old_len = new_len

heuristic = sys.argv[1][2]
file = sys.argv[2]
print(heuristic,file)
solve(heuristic,file)