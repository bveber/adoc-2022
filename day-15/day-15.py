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
distances = []
for i, reading in enumerate(readings):
    print(reading)
    sensor_x, sensor_y, nearest_beacon_x, nearest_beacon_y = list(
        map(int, re.findall("\-*\d+", reading))
    )
    nearest_beacon = Beacon(x=nearest_beacon_x, y=nearest_beacon_y)
    beacons.add(nearest_beacon)
    sensor = Sensor(x=sensor_x, y=sensor_y, nearest_beacon=nearest_beacon)
    sensors.add(sensor)
    distance = abs(sensor.x - nearest_beacon.x) + abs(sensor.y - nearest_beacon.y)
    distances.append(distance)
    print(f"distance: {distance}")
    if sensor_x > max_x or nearest_beacon_x > max_x:
        max_x = max((sensor_x, nearest_beacon_x))
    if sensor_y > max_y or nearest_beacon_y > max_y:
        max_y = max((sensor_y, nearest_beacon_y))
    if sensor_x < min_x or nearest_beacon_x < min_x:
        min_x = min((sensor_x, nearest_beacon_x))
    if sensor_y < min_y or nearest_beacon_y < min_y:
        min_y = min((sensor_y, nearest_beacon_y))
print((min_x, max_x), (min_y, max_y))
print(min(distances))
# %%
distances
# gcd(*distances[:2])
# %%
min_x = min_y = 0
max_x = max_y = 4000000
print(np.ceil(max_x/min(distances)))
for i in rang
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
my_answer_a

# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
x = set([(0, 0)])
x.update([(1, 1), (1, 1)])
x
# %%


transformed_sensors = 

# %%
def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

def rotate(x, y):
    return x+y, x-y

def unrotate(rotated_x, rotated_y):
    return int(rotated_x / 2 + rotated_y / 2), int(rotated_y / 2 - rotated_x / 2)

def create_rotated_square(point):
    Square = namedtuple("Square", "top_right bottom_right top_left bottom_left")
    x_min = point.x - point.distance
    x_max = point.x + point.distance
    rotated_x_min = x_min - point.y
    rotated_y_min = x_min + point.y
    rotated_x_max = x_max - point.y
    rotated_y_max = x_max + point.y
    return Square(rotated_x_min, rotated_y_min, rotated_x_max, rotated_y_max)


Sensor = namedtuple("Sensor", "x y distance")

sensors = set()
rotated_squares = []
for i, reading in enumerate(readings):
    # print(reading)
    sensor_x, sensor_y, nearest_beacon_x, nearest_beacon_y = list(
        map(int, re.findall("\-*\d+", reading))
    )
    distance = manhattan_distance((sensor_x, sensor_y), (nearest_beacon_x, nearest_beacon_y))

    sensor = Sensor(x=sensor_x, y=sensor_y, distance=distance)
    rotated_square = create_rotated_square(sensor)
    rotated_squares.append(rotated_square)
    sensors.add(sensor)

# print(rotated_squares)
rotated_x_vertices = set(
    square.top_right for square in rotated_squares
)
rotated_x_vertices.update(
    square.top_left for square in rotated_squares
)
boundary_x_values = set()
for val in rotated_x_vertices:
    boundary_x_values.add(val+1)
    boundary_x_values.add(val-1)
rotated_x_vertices = sorted(rotated_x_vertices | boundary_x_values)
# print(rotated_x_vertices)

rotated_x_ranges = {k: [] for k in rotated_x_vertices}
for i, rotated_square in enumerate(rotated_squares):
    for x_vertex in rotated_x_vertices:
        if rotated_square.top_right > rotated_square.top_left:
            if rotated_square.top_left <= x_vertex <= rotated_square.top_right:
                rotated_x_ranges[x_vertex].append(i)
        else:
            if rotated_square.top_right <= x_vertex <= rotated_square.top_left:
                rotated_x_ranges[x_vertex].append(i)

rotated_y_ranges = {}
for rotated_x, square_indices in rotated_x_ranges.items():
    ranges = []
    for square_index in square_indices:
        square = rotated_squares[square_index]
        if square.bottom_right > square.bottom_left:
            rng = [square.bottom_left, square.bottom_right]
        else:
            rng = [square.bottom_right, square.bottom_left]
        ranges.append(rng)
    ranges.sort()
    stack = []
    if len(ranges) > 0:
        stack.append(ranges[0])
        for r in ranges[1:]:
            if stack[-1][0] <= r[0] <= stack[-1][1]:
                stack[-1][1] = max(stack[-1][1], r[1])
            else:
                stack.append(r)
    rotated_y_ranges[rotated_x] = stack

rotated_y_ranges
multiplier = 4000000
for rotated_x, rotated_y_range in rotated_y_ranges.items():
    print(rotated_x, rotated_y_range)
    if len(rotated_y_range) == 2:
        rotated_y = rotated_y_range[0][1] + 1
        x, y = unrotate(rotated_x, rotated_y)
        my_answer_b = (x * multiplier + y)
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
