def print_sudoku(board):
    print("+" + "---+" * 9)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |" * 3).format(*[x % 10 if x != 0 else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+" * 9)


def solution(truth_values):
    print('\n\n------------- SOLUTION --------------')
    solutions = []
    for solution in truth_values:
        if solution > 0:
            solutions.append(solution)
    solution_grid = []
    for i in range(0, 81, 9):
        solution_grid.append(solutions[i:i + 9])
    print_sudoku(solution_grid)
    return True