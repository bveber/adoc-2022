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

today = datetime(year=2022, month=12, day=18)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
raw_input_data = puzzle.input_data
# raw_input_data = """2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5"""
Cube = namedtuple("Cube", "x y z")
cubes = {
    Cube(int(line.split(",")[0]), int(line.split(",")[1]), int(line.split(",")[2]))
    for line in raw_input_data.split("\n")
}
cubes
# %%
sides_blocked = 0
for cube in cubes:
    if Cube(cube.x - 1, cube.y, cube.z) in cubes:
        sides_blocked += 1
    if Cube(cube.x + 1, cube.y, cube.z) in cubes:
        sides_blocked += 1
    if Cube(cube.x, cube.y - 1, cube.z) in cubes:
        sides_blocked += 1
    if Cube(cube.x, cube.y + 1, cube.z) in cubes:
        sides_blocked += 1
    if Cube(cube.x, cube.y, cube.z - 1) in cubes:
        sides_blocked += 1
    if Cube(cube.x, cube.y, cube.z + 1) in cubes:
        sides_blocked += 1
my_answer_a = 6 * len(cubes) - sides_blocked
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)

# %%
x_min, x_max = min([cube.x - 1 for cube in cubes]), max([cube.x + 2 for cube in cubes])
y_min, y_max = min([cube.y - 1 for cube in cubes]), max([cube.y + 2 for cube in cubes])
z_min, z_max = min([cube.z - 1 for cube in cubes]), max([cube.z + 2 for cube in cubes])

possible_cubes = set()
for x in range(x_min, x_max):
    for y in range(y_min, y_max):
        for z in range(z_min, z_max):
            possible_cubes.add(Cube(x, y, z))

cube_queue = [Cube(x_min, y_min, z_min)]
visited = set(Cube(x_min, y_min, z_min))
neighbor_ctr = 0
# depth first search neighboring cubes
while cube_queue:
    cube = cube_queue.pop(-1)
    neighboring_cubes = [
        Cube(cube.x - 1, cube.y, cube.z),
        Cube(cube.x + 1, cube.y, cube.z),
        Cube(cube.x, cube.y - 1, cube.z),
        Cube(cube.x, cube.y + 1, cube.z),
        Cube(cube.x, cube.y, cube.z - 1),
        Cube(cube.x, cube.y, cube.z + 1),
    ]
    for neighbor in neighboring_cubes:
        if neighbor in visited or neighbor not in possible_cubes:
            continue
        if neighbor in cubes:
            neighbor_ctr += 1
        else:
            visited.add(neighbor)
            cube_queue.append(neighbor)
my_answer_b = neighbor_ctr
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
