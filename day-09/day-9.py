# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import os

today = datetime(year=2022, month=12, day=9)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
input_data = puzzle.input_data.split("\n")
# input_data = """R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20""".split(
#     "\n"
# )
# input_data = """R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2""".split(
#     "\n"
# )
input_data = [row.split() for row in input_data]
print(input_data)
# %%
def move_head_one(direction, head_location):
    if direction == "L":
        return (head_location[0] - 1, head_location[1])
    if direction == "R":
        return (head_location[0] + 1, head_location[1])
    if direction == "U":
        return (head_location[0], head_location[1] + 1)
    if direction == "D":
        return (head_location[0], head_location[1] - 1)


def move_tail_follow(head_location, tail_location):
    distance_x = head_location[0] - tail_location[0]
    distance_y = head_location[1] - tail_location[1]
    # print(f"distance_x: {distance_x}, distance_y: {distance_y}")
    if abs(distance_x) == 2 and abs(distance_y) == 2:
        return (
            head_location[0] - distance_x / abs(distance_x),
            head_location[1] - distance_y / abs(distance_y),
        )
    if abs(distance_x) <= 1 and abs(distance_y) <= 1:
        return tail_location
    if abs(distance_x) >= 2 and distance_y == 0:
        return (head_location[0] - distance_x / abs(distance_x), tail_location[1])
    if abs(distance_x) >= 2 and abs(distance_y) > 0:
        return (head_location[0] - distance_x / abs(distance_x), head_location[1])
    if abs(distance_y) >= 2 and distance_x == 0:
        return (tail_location[0], head_location[1] - distance_y / abs(distance_y))
    if abs(distance_y) >= 2 and abs(distance_x) > 0:
        return (head_location[0], head_location[1] - distance_y / abs(distance_y))


def move_one(direction, head_location, tail_location):
    head_location = move_head_one(direction, head_location)
    tail_location = move_tail_follow(head_location, tail_location)
    return head_location, tail_location


start = head = tail = (0, 0)
head_visited = [start]
tail_visited = [start]
# print(f"head: {head}, tail: {tail}")
for entry in input_data:
    direction, length = entry
    for i in range(1, int(length) + 1):
        head, tail = move_one(direction, head, tail)
        head_visited.append(head)
        tail_visited.append(tail)
        # print(direction, head, tail)
for i in range(len(head_visited)):
    print(i, "head: ", head_visited[i], "tail: ", tail_visited[i])

# %%
my_answer_a = len(set(tail_visited))
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
start = (0, 0)
num_knots = 10
positions = {i: start for i in range(num_knots)}
# tails = {i+1 for i in range(10)}
pairs = [(i, i + 1) for i in range(num_knots - 1)]
visited = {i: [start] for i in range(10)}
# print(f"head: {head}, tail: {tail}")
for entry in input_data:
    direction, length = entry
    print(direction, length)
    for i in range(1, int(length) + 1):
        for j, pair in enumerate(pairs):
            # print(pair)

            head_index = pair[0]
            tail_index = pair[1]
            head = positions[head_index]
            tail = positions[tail_index]
            if j == 0:
                head, tail = move_one(direction, head, tail)
                positions[head_index] = head
                visited[head_index].append(head)
            else:
                tail = move_tail_follow(head, tail)
            positions[tail_index] = tail
            visited[tail_index].append(tail)
            # print(direction, head, tail)
        print(positions)

for i in range(len(visited[0])):
    print(i, [visited[k][i] for k in visited])
# %%
my_answer_b = len(set(visited[9]))
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)

# %%
