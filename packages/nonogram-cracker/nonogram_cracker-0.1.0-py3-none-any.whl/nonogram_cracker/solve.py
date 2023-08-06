from solve_seq import solve_seq

def solve(puzzle):
  width = len(puzzle['cols'])
  height = len(puzzle['rows'])

  solution = [' ' * width] * height
  changed = True

  while changed:
    changed = False
    # iterate through rows running solver fn
    for i in range(height):
      row = solution[i]
      row_clues = puzzle['rows'][i]
      next_row = solve_seq(row, row_clues)
      if row != next_row:
        changed = True
        solution[i] = next_row
    # iterate through cols running solver fn
    for i in range(width):
      col = ''.join([solution[j][i] for j in range(height)])
      col_clues =  puzzle['cols'][i]
      next_col = solve_seq(col, col_clues)
      if col != next_col:
        changed = True
        for j in range(height):
          solution[j] = solution[j][:i] + next_col[j] + solution[j][i + 1:]

  return solution
