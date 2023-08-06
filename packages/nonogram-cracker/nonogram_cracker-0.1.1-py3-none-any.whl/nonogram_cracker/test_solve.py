from nonogram_cracker.solve import solve
import json

def test_solve_puzzle_1():
  puzzle = json.load(open('../../sample_data/puzzle1.json'))
  expected = json.load(open('../../sample_data/puzzle1.solution.json', encoding='utf-8'))
  print(expected)
  actual_solution = solve(puzzle)
  assert actual_solution == expected['solution']
