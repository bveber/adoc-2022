# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import os

today = datetime(year=2022, month=12, day=10)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
input_data = puzzle.input_data.split("\n")
# input_data = """addx 15
# addx -11
# addx 6
# addx -3
# addx 5
# addx -1
# addx -8
# addx 13
# addx 4
# noop
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx -35
# addx 1
# addx 24
# addx -19
# addx 1
# addx 16
# addx -11
# noop
# noop
# addx 21
# addx -15
# noop
# noop
# addx -3
# addx 9
# addx 1
# addx -3
# addx 8
# addx 1
# addx 5
# noop
# noop
# noop
# noop
# noop
# addx -36
# noop
# addx 1
# addx 7
# noop
# noop
# noop
# addx 2
# addx 6
# noop
# noop
# noop
# noop
# noop
# addx 1
# noop
# noop
# addx 7
# addx 1
# noop
# addx -13
# addx 13
# addx 7
# noop
# addx 1
# addx -33
# noop
# noop
# noop
# addx 2
# noop
# noop
# noop
# addx 8
# noop
# addx -1
# addx 2
# addx 1
# noop
# addx 17
# addx -9
# addx 1
# addx 1
# addx -3
# addx 11
# noop
# noop
# addx 1
# noop
# addx 1
# noop
# noop
# addx -13
# addx -19
# addx 1
# addx 3
# addx 26
# addx -30
# addx 12
# addx -1
# addx 3
# addx 1
# noop
# noop
# noop
# addx -9
# addx 18
# addx 1
# addx 2
# noop
# noop
# addx 9
# noop
# noop
# noop
# addx -1
# addx 2
# addx -37
# addx 1
# addx 3
# noop
# addx 15
# addx -21
# addx 22
# addx -6
# addx 1
# noop
# addx 2
# addx 1
# noop
# addx -10
# noop
# noop
# addx 20
# addx 1
# addx 2
# addx 2
# addx -6
# addx -11
# noop
# noop
# noop""".split('\n')
print(input_data[:5])
# %%
x = 1
x_values = []
for command in input_data:
    x_values.append(x)
    if command == "noop":
        continue
    else:
        adder = int(command.split()[-1])
        x_values.append(x)
        x += adder
print(x_values)
print(x)
# %%
def calc_signal_strength(x_values):
    strength = 0
    idx_0 = 20
    if len(x_values) < idx_0:
        return strength
    if len(x_values) >= idx_0:
        strength += idx_0 * x_values[idx_0 - 1]
    for idx in range(60, len(x_values), 40):
        strength += idx * x_values[idx - 1]
    return strength


my_answer_a = calc_signal_strength(x_values)
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
x = 1
display = []
for i, x_value in enumerate(x_values):
    col_idx = i % 40
    if abs(col_idx - x_value) > 1:
        draw = "."
    else:
        draw = "#"
    if col_idx == 0:
        display.append([draw])
    else:
        display[-1].append(draw)
for row in display:
    print(" ".join(row))
# %%
len(display[0])
# %%
