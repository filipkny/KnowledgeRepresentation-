import read_files, split, simplify, pretty_print
import time, xlsxwriter

file = 'damnhard.sdk.txt'
sudokus = read_files.read_sudokus_file(file)

start_time = time.time()

# Choose heuristic: 0 = Basic DPLL (random), 1 = Jeroslow-Wang method, 2 = Heuristic 2
which_method = 1

print('============ SAT Solver =============')
print_heuristic = ['Basic DPLL (random)', 'Jeroslow-Wang method ', 'Heuristic 2']
print('    Heuristic: ', print_heuristic[which_method])
print('=====================================\n')

# csv output
workbook_file = str(file.split('.')[0] + '-' + print_heuristic[which_method] + '.xlsx')
workbook = xlsxwriter.Workbook(workbook_file)
worksheet = workbook.add_worksheet()
head_lst = ['No. Sudoku', 'Unit Clauses', 'First simplify reduction (%)', 'Splits', 'Backtrackings', 'Time (sec)']
for cell in range(6):
    worksheet.write(0, cell, head_lst[cell])


for sdk in range(1, len(sudokus)+1):
    problem_start_time = time.time()

    truth_values = sudokus[sdk] # {} when we submit

    # List for data analysis EXCEL
    # [#unit_clauses, %of reduction from first simplify, #splits, #backtrackings, #time]
    results = [sdk ,0, 100., 0, 0, 0]

    # Position 0: get the #unit_clauses
    results[1] = len(truth_values)

    rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
    split_choice, neg_literal = [], []

    rules = read_files.read_DIMACS_file("sudoku-rules.txt")
    rules, literals_dict = read_files.init_database(rules)

    print('======== SAT Problem: {}/{} ========'.format(sdk, len(sudokus)))
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
            pretty_print.solution(truth_values)
            finish = True

            # get the solution time
            results[5] = float("{0:.2f}".format(time.time() - problem_start_time))
            print("\nTime:    %.2f seconds " % (time.time() - problem_start_time))
            print("Runtime: %.2f seconds " % (time.time() - start_time))
            print("Initial #unit clauses :",results[1] )
            print("Reduction from first simplify: ", results[2], '%')
            print("#splits :",results[3] )
            print("#backtrackings :",results[4] )
            print('=====================================\n')

            # CSV OUTPUT
            for i in range(len(results)):
                worksheet.write(sdk, i, results[i])
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
workbook.close()
