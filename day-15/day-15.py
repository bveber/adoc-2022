# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import numpy as np
import ast
import re
from collections import namedtuple
import numpy as np

today = datetime(year=2022, month=12, day=15)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
raw_input_data = puzzle.input_data
# raw_input_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
readings = raw_input_data.split("\n")
# %%
Beacon = namedtuple("Beacon", "x y")
Sensor = namedtuple("Sensor", "x y nearest_beacon")
sensors = set()
beacons = set()
# cant_be_hidden_beacons = set()
min_x = max_x = 0
min_y = max_y = 0
for i, reading in enumerate(readings):
    print(reading)
    sensor_x, sensor_y, nearest_beacon_x, nearest_beacon_y = list(
        map(int, re.findall("\-*\d+", reading))
    )
    nearest_beacon = Beacon(x=nearest_beacon_x, y=nearest_beacon_y)
    beacons.add(nearest_beacon)
    sensor = Sensor(x=sensor_x, y=sensor_y, nearest_beacon=nearest_beacon)
    sensors.add(sensor)
    if sensor_x > max_x or nearest_beacon_x > max_x:
        max_x = max((sensor_x, nearest_beacon_x))
    if sensor_y > max_y or nearest_beacon_y > max_y:
        max_y = max((sensor_y, nearest_beacon_y))
    if sensor_x < min_x or nearest_beacon_x < min_x:
        min_x = min((sensor_x, nearest_beacon_x))
    if sensor_y < min_y or nearest_beacon_y < min_y:
        min_y = min((sensor_y, nearest_beacon_y))
print((min_x, max_x), (min_y, max_y))

# %%
def find_row_beacons(min_x, max_x, y, beacons):
    found_beacons = []
    for x in range(min_x, max_x + 1):
        beacon = Beacon(x, y)
        if beacon in beacons:
            found_beacons.append(beacon)
    return found_beacons


print(find_row_beacons(min_x, max_x, 2000000, beacons))

# %%
len(sensors)
# %%
y = 2000000
cant_be = set()
for i, sensor in enumerate(sensors):
    # print(sensor)
    distance = abs(sensor.x - sensor.nearest_beacon.x) + abs(
        sensor.y - sensor.nearest_beacon.y
    )
    for i in range(distance - abs(sensor.y - y) + 1):
        not_beacon = Beacon(x=sensor.x + i, y=y)
        if not_beacon not in cant_be:
            cant_be.add(not_beacon)
        not_beacon = Beacon(x=sensor.x - i, y=y)
        if not_beacon not in cant_be:
            cant_be.add(not_beacon)
# %%
my_answer_a = len(cant_be) - len(find_row_beacons(min_x, max_x, y, beacons))
print(my_answer_a)

# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def rotate(x, y):
    return x + y, x - y


def unrotate(rotated_x, rotated_y):
    return int(rotated_x / 2 + rotated_y / 2), int(rotated_y / 2 - rotated_x / 2)


def create_rotated_square(point):
    "Rotate the diamonds 45 degrees to make them normal squares"
    Square = namedtuple("Square", "right_x right_y left_x left_y")
    x_min = point.x - point.distance
    x_max = point.x + point.distance
    rotated_x_min = x_min - point.y
    rotated_y_min = x_min + point.y
    rotated_x_max = x_max - point.y
    rotated_y_max = x_max + point.y
    return Square(rotated_x_min, rotated_y_min, rotated_x_max, rotated_y_max)


Sensor = namedtuple("Sensor", "x y distance")
max_x = max_y = 4000000

rotated_squares = []
for i, reading in enumerate(readings):
    # Parse input
    sensor_x, sensor_y, nearest_beacon_x, nearest_beacon_y = list(
        map(int, re.findall("\-*\d+", reading))
    )
    distance = manhattan_distance(
        (sensor_x, sensor_y), (nearest_beacon_x, nearest_beacon_y)
    )
    sensor = Sensor(x=sensor_x, y=sensor_y, distance=distance)
    rotated_square = create_rotated_square(sensor)
    rotated_squares.append(rotated_square)

# Get x vertices of rotated squares
rotated_x_vertices = set(square.right_x for square in rotated_squares)
rotated_x_vertices.update(square.left_x for square in rotated_squares)
# Add boundary points
boundary_x_values = set()
for val in rotated_x_vertices:
    boundary_x_values.add(val + 1)
    boundary_x_values.add(val - 1)
rotated_x_vertices = sorted(rotated_x_vertices | boundary_x_values)

# find potential x values
rotated_x_ranges = {k: [] for k in rotated_x_vertices}
for i, rotated_square in enumerate(rotated_squares):
    for x_vertex in rotated_x_vertices:
        if rotated_square.right_x > rotated_square.left_x:
            if rotated_square.left_x <= x_vertex <= rotated_square.right_x:
                rotated_x_ranges[x_vertex].append(i)
        else:
            if rotated_square.right_x <= x_vertex <= rotated_square.left_x:
                rotated_x_ranges[x_vertex].append(i)

rotated_y_ranges = {}
# Iterate over x values and their associated squares
for rotated_x, square_indices in rotated_x_ranges.items():
    # find y-ranges values for each x_vertex and its square(s)
    y_ranges = []
    for square_index in square_indices:
        square = rotated_squares[square_index]
        if square.right_y > square.left_y:
            rng = [square.left_y, square.right_y]
        else:
            rng = [square.right_y, square.left_y]
        y_ranges.append(rng)
    y_ranges.sort()
    # find if the point is in the intersection of
    range_stack = []
    if len(y_ranges) > 0:
        range_stack.append(y_ranges[0])
        for r in y_ranges[1:]:
            if range_stack[-1][0] <= r[0] <= range_stack[-1][1]:
                range_stack[-1][1] = max(range_stack[-1][1], r[1])
            else:
                range_stack.append(r)
            # If there are two ranges that means it is found to be a possible value in both dimensions.
            # Since there is only one possible spot on the map we can stop looking. Problem Solved!
            if len(range_stack) == 2:
                rotated_y = r[0][1] + 1
                x, y = unrotate(rotated_x, rotated_y)
                my_answer_b = x * multiplier + y
            print(my_answer_b)
            break


# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)

# %%
