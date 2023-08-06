from nonogram_cracker.helpers.identifiers import is_group, is_cross

def is_already_solved(cells_str):
  return all([is_group(x) or is_cross(x) for x in cells_str])
