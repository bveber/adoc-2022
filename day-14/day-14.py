# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import numpy as np
import ast

today = datetime(year=2022, month=12, day=14)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
raw_input_data = puzzle.input_data
# raw_input_data = """498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9"""
wall_instructions = raw_input_data.split("\n")
print(wall_instructions)

# %%
class Map:
    def __init__(self, wall_instructions, x_initial=500):
        self.wall_instructions = wall_instructions
        self.nodes = set()
        self.x_initial = x_initial
        self.min_x = self.max_x = x_initial
        self.min_y = self.max_y = 0
        self.max_y_by_x = {}
        self.particle_counter = 0
        self.build_walls()

    def __repr__(self):
        return f"""
        Number of occupied nodes: {len(self.nodes)}
        Particle_counter: {self.particle_counter}
        min x, y: {(self.min_x, self.min_y)}
        max x, y: {(self.max_x, self.max_y)}
        """

    @staticmethod
    def parse_instruction(instruction):
        return (int(instruction.split(",")[0]), int(instruction.split(",")[1]))

    def build_walls(self):
        for wall in self.wall_instructions:
            instructions = wall.split(" -> ")
            instruction_parsed = self.parse_instruction(instructions[0])
            self.occupy_node(instruction_parsed, is_wall=True)
            for next_instruction in instructions[1:]:
                next_instruction_parsed = self.parse_instruction(next_instruction)
                start_x = instruction_parsed[0]
                end_x = next_instruction_parsed[0]
                if start_x == end_x:
                    x_range = range(0)
                if start_x < end_x:
                    x_range = range(start_x, end_x + 1)
                else:
                    x_range = range(end_x, start_x + 1)
                for x_index in x_range:
                    self.occupy_node(
                        (x_index, next_instruction_parsed[1]), is_wall=True
                    )

                start_y = instruction_parsed[1]
                end_y = next_instruction_parsed[1]
                if start_y == end_y:
                    range(0)
                if start_y < end_y:
                    y_range = range(start_y, end_y + 1)
                else:
                    y_range = range(end_y, start_y + 1)
                for y_index in y_range:
                    self.occupy_node(
                        (next_instruction_parsed[0], y_index), is_wall=True
                    )
                instruction_parsed = next_instruction_parsed

    def occupy_node(self, instruction_parsed, is_wall=False):
        x, y = instruction_parsed
        if x < self.min_x:
            self.min_x = x
        if x > self.max_x:
            self.max_x = x
        if y < self.min_y:
            self.min_y = y
        if y > self.max_y:
            self.max_y = y
        if x not in self.max_y_by_x:
            self.max_y_by_x[x] = y
        if y > self.max_y_by_x[x]:
            self.max_y_by_x[x] = y

        self.nodes.add((x, y))
        if not is_wall:
            self.particle_counter += 1

    def find_starting_point(self):
        start_x = self.x_initial
        start_y = 0
        for y in range(self.min_y, self.max_y + 1):
            if (start_x, y) in self.nodes:
                start_y = y - 1
                return start_x, start_y

    def check_next_particle(self, start_point=None):
        if not start_point:
            start_point = self.find_starting_point()
        left_down = (start_point[0] - 1, start_point[1] + 1)
        if start_point[1] >= self.max_y:
            return "Fallen into the void!"

        if left_down not in self.nodes:
            for y in range(left_down[1], self.max_y):
                if (left_down[0], y + 1) in self.nodes:
                    return self.check_next_particle((left_down[0], y))
            return self.check_next_particle(left_down)

        right_down = (start_point[0] + 1, start_point[1] + 1)
        if right_down not in self.nodes:
            for y in range(right_down[1], self.max_y):
                if (right_down[0], y + 1) in self.nodes:
                    return self.check_next_particle((right_down[0], y))
            return self.check_next_particle(right_down)
        if start_point == (500, 0):
            self.occupy_node((500, 0))
            return "Full"
        return start_point

    def drop_particles(self):
        start_point = self.find_starting_point()
        self.occupy_node(start_point)
        next_particle = self.check_next_particle()
        while next_particle not in ("Fallen into the void!", "Full"):
            self.occupy_node(next_particle)
            next_particle = self.check_next_particle()

    def execute():
        return


map = Map(wall_instructions)
map.drop_particles()

print(map)
# %%
submit(
    map.particle_counter,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
max_y = 0
for wall in wall_instructions:
    instructions = wall.split(" -> ")
    for instruction in instructions:
        y = int(instruction.split(",")[1])
        if y > max_y:
            max_y = y
floor_y = max_y + 2
wall_instructions_b = wall_instructions + [
    f"{500-floor_y},{floor_y} -> {500+floor_y},{floor_y}"
]
print(wall_instructions_b)
map_b = Map(wall_instructions_b)
map_b.drop_particles()

print(map_b)

# %%
submit(
    map_b.particle_counter,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
