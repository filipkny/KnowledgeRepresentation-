import read_files, split, simplify, pretty_print, time, xlsxwriter

rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
split_choice, neg_literal = [], []

# SDKS
easy_sdk = "sdks/1000_sudokus.txt"
hard_sdk = 'sdks/damnhard.sdk.txt'
file = easy_sdk # change only this and the heuristic  <--   HERE       HERE     HERE
sudokus = read_files.read_sudokus_file(file)


# SAT
# # sat = 'sat/uf20/uf20-06.txt'
# DIMACS = read_files.read_DIMACS_file('sudoku_test_3.txt')
# rules, literals_dict, truth_values = read_files.init_database(DIMACS)

# Choose heuristic: 0 = Basic DPLL (random), 1 = Jeroslow-Wang method, 2 = MOMs method
which_method = 0

print('============ SAT Solver =============')
print_heuristic = ['Basic DPLL (random)', 'Jeroslow-Wang method ', 'MOMs method']
print('    Heuristic: ', print_heuristic[which_method])
print('=====================================\n')

start_time = time.time()

xls_file_name = str(file.split('/')[1] ).split('.')[0] + '-' + print_heuristic[which_method] + '_final.xlsx'
workbook_file = xls_file_name
workbook = xlsxwriter.Workbook(workbook_file)
worksheet = workbook.add_worksheet()
head_lst = ['No. Sudoku', 'Unit Clauses', 'First simplify reduction (%)', 'Splits', 'Backtrackings', 'Time (sec)']
for cell in range(6):
    worksheet.write(0, cell, head_lst[cell])

for sdk in range(1, 4): #len(sudokus) + 1
    truth_values = sudokus[sdk]
    # [#unit_clauses, %of reduction fro first simplify, #splits, #backtrackings, #time]
    results = [sdk, 0, 100., 0, 0, 0]
    results[1] = len(truth_values)
    split_count = 0
    back_track_count = 0
    problem_start_time = time.time()
    rules = read_files.read_DIMACS_file("sdks/sudoku-rules.txt")
    rules, literals_dict, temp = read_files.init_database(rules)
    old_clauses_count = len(rules)
    done = False
    while done == False:
        back_track = False
        # Simplify
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split, back_track = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                              rules_before_split, literals_dict_before_split, truth_values_before_split,back_track)
        new_clauses_count = len(rules)

        if back_track:
            back_track_count+=1

        if new_clauses_count == 0:
            pretty_print.solution(truth_values)
            results[3] = split_count
            results[4] = back_track_count
            results[5] = float("{0:.2f}".format(time.time() - problem_start_time))
            # CSV OUTPUT
            for i in range(len(results)):
                worksheet.write(sdk, i, results[i])
            done = True

        elif old_clauses_count == new_clauses_count and back_track == False:
            split_count+=1
            # Split
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                            rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
        old_clauses_count = new_clauses_count
workbook.close()
