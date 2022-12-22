# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
import ast
from pprint import pprint
import re
from collections import namedtuple
import numpy as np
import itertools

today = datetime(year=2022, month=12, day=17)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
shapes_text = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split(
    "\n\n"
)
shapes = []
shape_width = shape_height = 4

for shape in shapes_text:
    rows = shape.splitlines()
    shape_matrix = []
    top_row = len(rows)
    for i in range(top_row, shape_height):
        shape_matrix.append([0] * shape_width)
    for row in rows:
        row_shape = []
        for elem in row:
            if elem == "#":
                row_shape.append(1)
            else:
                row_shape.append(0)
        for i in range(len(row_shape), shape_width):
            row_shape.append(0)
        shape_matrix.append(row_shape)
    shapes.append(np.array(shape_matrix))
shapes = shapes
gas_jets = puzzle.input_data.rstrip()  # .splitlines()[0]
# gas_jets = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
pprint(shapes)
pprint(len(gas_jets))
print(gas_jets[:5], gas_jets[-5:])
# %%
def simulate(num_rocks):
    chamber_map_height_0 = 7
    chamber_map_width = 7
    chamber_map = []
    for i in range(chamber_map_height_0):
        chamber_map.append([0] * chamber_map_width)
    chamber_map.append([1] * chamber_map_width)
    chamber_map = np.array(chamber_map)

    rock_blast_combos = {}
    ctr = 0
    for rock_num in range(num_rocks):
        # print("iteration #: ", i)
        shape = shapes[rock_num % len(shapes)]
        shape_height, shape_width = shape.shape
        fall = True
        row_index = 0
        col_index = 2
        col_mask = np.all(shape == 0, axis=0)
        shape_stripped = shape[:, ~col_mask]
        shape_stripped_height, shape_stripped_width = shape_stripped.shape
        while fall:
            blast = gas_jets[ctr % len(gas_jets)]
            # print(ctr, blast)
            ctr += 1
            # Cycle detection
            if rock_num > 1000:
                rock_blast = (rock_num % len(shapes), ctr % len(gas_jets))
                if rock_blast in rock_blast_combos:
                    last_rock_blast_num, last_rock_blast_height = rock_blast_combos[
                        rock_blast
                    ]
                    interval = rock_num - last_rock_blast_num
                    if rock_num % interval == num_rocks % interval:
                        cycle_height = (
                            len(chamber_map) - row_index - last_rock_blast_height
                        )
                        rocks_leftover = num_rocks - rock_num
                        cycles_leftover = (rocks_leftover // interval) + 1
                        print("found cycle")
                        return (
                            last_rock_blast_height
                            + (cycle_height * cycles_leftover)
                            - 8
                        )
                else:
                    rock_blast_combos[rock_blast] = (
                        rock_num,
                        len(chamber_map) - row_index,
                    )
            # check left right
            if blast == ">":
                temp_col_index = col_index + 1
            else:  # blast == "<"
                temp_col_index = col_index - 1
            if temp_col_index < 0 or temp_col_index > (
                chamber_map_width - shape_stripped_width
            ):
                temp_col_index = col_index
            row_offset = shape_height - shape_stripped_height
            chamber_map_overlay = chamber_map[
                row_index + row_offset : row_index + shape_height,
                temp_col_index : temp_col_index + shape_stripped_width,
            ]
            if (chamber_map_overlay * shape_stripped).sum() == 0:
                col_index = temp_col_index
            temp_row_index = row_index + 1
            chamber_map_overlay = chamber_map[
                temp_row_index + row_offset : temp_row_index + shape_height,
                col_index : col_index + shape_stripped_width,
            ]
            if (chamber_map_overlay * shape_stripped).sum() == 0:
                row_index = temp_row_index
                temp_cm = chamber_map.copy()
                temp_cm[
                    row_index : row_index + shape_height,
                    col_index : col_index + shape_stripped_width,
                ] = shape_stripped
            else:
                row_offset = shape_height - shape_stripped_height
                chamber_map[
                    row_index + row_offset : row_index + shape_height,
                    col_index : col_index + shape_stripped_width,
                ] += shape_stripped
                next_height = (shape_height + 3) - (chamber_map != 0).argmax(
                    axis=0
                ).min()
                for j in range(next_height):
                    chamber_map = np.insert(
                        chamber_map, 0, np.array([0] * chamber_map_width), 0
                    )
                fall = False

    return len(chamber_map) - 8


my_answer_a = simulate(2022)

my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)

# %%
my_answer_b = simulate(1000000000000)
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
