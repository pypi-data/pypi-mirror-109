
# Nonogram Cracker

## Takes in a nonogram puzzle and returns its solution

---

## Usage

```python
from nonogram_cracker import solve
print(solve(sample_input))
```

---

### Sample Input
```json
{
  "name": "turtle",
  "rows": [
    [1, 1, 1],
    [5],
    [3],
    [5],
    [1, 1]
  ],
  "cols": [
    [2, 2],
    [3],
    [4],
    [3],
    [2, 2]
  ]
}
```

### Sample Output
```json
{
  "name": "turtle",
  "solution": [
    "█ █ █",
    "█████",
    " ███ ",
    "█████",
    "█   █"
  ]
}
```







