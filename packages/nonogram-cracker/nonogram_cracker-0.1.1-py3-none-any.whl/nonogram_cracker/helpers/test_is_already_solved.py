from nonogram_cracker.helpers.is_already_solved import is_already_solved

def test_is_already_solved_false_1():
  assert not is_already_solved('     ')
def test_is_already_solved_false_2():
  assert not is_already_solved('xxxx ')
def test_is_already_solved_false_3():
  assert not is_already_solved('xgxg ')
def test_is_already_solved_false_4():
  assert not is_already_solved(' gggg')

def test_is_already_solved_true1():
  assert is_already_solved('ggggg')
def test_is_already_solved_true2():
  assert is_already_solved('xxxxx')
def test_is_already_solved_true3():
  assert is_already_solved('xgxgx')