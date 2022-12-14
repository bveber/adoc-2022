# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import os

today = datetime(year=2022, month=12, day=8)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
input_data = puzzle.input_data.split("\n")
# input_data = """30373
# 25512
# 65332
# 33549
# 35390""".split('\n')
input_data
# %%
tree_heights = []
for row in input_data:
    tree_heights.append([int(height) for height in row])
pprint(tree_heights)
# %%
outer_tree_count = len(tree_heights) * 2 + len(tree_heights[0]) * 2 - 4
outer_tree_count
# %%
def check_lr(all_rows, row_index, col_index):
    max_left = max(all_rows[row_index][:col_index])
    max_right = max(all_rows[row_index][col_index + 1 :])

    return (
        all_rows[row_index][col_index] > max_left
        or all_rows[row_index][col_index] > max_right
    )


def check_ud(all_rows, row_index, col_index):
    max_up = max([all_rows[i][col_index] for i in range(row_index)])
    max_down = max(
        [all_rows[i][col_index] for i in range(row_index + 1, len(all_rows))]
    )
    return (
        all_rows[row_index][col_index] > max_up
        or all_rows[row_index][col_index] > max_down
    )


inner_visible_count = 0
for i, row in enumerate(tree_heights[:]):
    if i not in (0, len(tree_heights) - 1):
        print(i, row)
        for j, col in enumerate(row):
            if j not in (0, len(tree_heights[0]) - 1):
                print(
                    i, j
                )  # , check_lr(tree_heights, i, j), check_ud(tree_heights, i, j))
                if check_lr(tree_heights, i, j) or check_ud(tree_heights, i, j):
                    inner_visible_count += 1
print(inner_visible_count)
# %%
my_answer_a = inner_visible_count + outer_tree_count
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
def check_l(all_rows, row_index, col_index):
    for i, idx in enumerate(range(col_index - 1, -1, -1)):
        if all_rows[row_index][idx] >= all_rows[row_index][col_index]:
            return i + 1
    return i + 1


def check_r(all_rows, row_index, col_index):
    for i, idx in enumerate(range(col_index + 1, len(all_rows[0]))):
        if all_rows[row_index][idx] >= all_rows[row_index][col_index]:
            return i + 1
    return i + 1


def check_u(all_rows, row_index, col_index):
    for i, idx in enumerate(range(row_index - 1, -1, -1)):
        if all_rows[idx][col_index] >= all_rows[row_index][col_index]:
            return i + 1
    return i + 1


def check_d(all_rows, row_index, col_index):
    for i, idx in enumerate(range(row_index + 1, len(all_rows))):
        if all_rows[idx][col_index] >= all_rows[row_index][col_index]:
            return i + 1
    return i + 1


# %%
tree_scores = []
for i, row in enumerate(tree_heights[:]):
    if i not in (0, len(tree_heights) - 1):
        for j, col in enumerate(row):
            if j not in (0, len(tree_heights[0]) - 1):
                print(
                    i, j, tree_heights[i][j]
                )  # , check_lr(tree_heights, i, j), check_ud(tree_heights, i, j))
                # if check_l(tree_heights, i, j) or check_ud(tree_heights, i, j):
                left = check_l(tree_heights, i, j)
                right = check_r(tree_heights, i, j)
                up = check_u(tree_heights, i, j)
                down = check_d(tree_heights, i, j)
                score = left * right * up * down
                print(left, right, up, down, score)
                tree_scores.append(score)
sorted(tree_scores)[::-1]
# %%
my_answer_b = sorted(tree_scores)[-1]
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
