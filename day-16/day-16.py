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

today = datetime(year=2022, month=12, day=16)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
raw_input_data = puzzle.input_data
# raw_input_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II"""
input_data = raw_input_data.split("\n")
print(len(input_data))
# %%
def bfs_sp(graph, start, end):
    visited, stack = set(), [[start]]
    while stack:
        path = stack.pop(0)
        node = path[-1]
        if node not in visited:
            visited.add(node)

            neighbors = graph[node]

            # Loop to iterate over the
            # neighbors of the node
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                # stack.extend(graph[path] - visited)
                stack.append(new_path)

                # Condition to check if the
                # neighbor node is the goal
                if neighbor == end:
                    # print("Shortest path = ", *new_path)
                    return new_path
            visited.add(node)
    return visited


# %%
valves = {}
for input_valve_text in input_data:
    text_split = input_valve_text.split()
    name = text_split[1]
    rate = int(re.search(r"\d+", text_split[4]).group())
    neighbor_valves_names = "".join(text_split[9:]).split(",")
    valves[name] = {
        "rate": rate,
        "neighbor_valves": neighbor_valves_names,
        "open": False,
    }
steps = {
    x: {y: 1 if y in valves[x]["neighbor_valves"] else float("inf") for y in valves}
    for x in valves
}
# Floyd-Warshall Algorithm for steps between nodes (valves)
for k in steps:
    for i in steps:
        for j in steps:
            steps[i][j] = min(steps[i][j], steps[i][k] + steps[k][j])


def calculate_remaining_score(valves, unopened, time_remaining):
    sorted_unopened_rates = sorted(
        valve["rate"] for name, valve in valves.items() if name in unopened
    )[::-1]
    remaining_score = 0
    for i, time_multiplier in enumerate(range(time_remaining - 2, 0, -2)):
        if i == len(sorted_unopened_rates):
            break
        remaining_score += sorted_unopened_rates[i] * time_multiplier
    return remaining_score


def get_paths(valves, start_valve="AA", max_time=30):
    adjacency_list = {key: val["neighbor_valves"] for key, val in valves.items()}

    Path = namedtuple("Path", "time score unopened complete_path")
    unopened_valves = set(
        valve_name
        for valve_name, valve in valves.items()
        if valve["rate"] > 0 and not valve["open"]
    )
    paths = [Path(0, 0, unopened_valves, [start_valve])]
    completed_paths = []
    max_score = 0
    timer = 0
    while len(paths) > 0:
        path = paths.pop(-1)
        if path.score > max_score:
            max_score = path.score
            max_path = path
        if len(path.unopened) == 0:
            completed_paths.append(path)

        for unopened_valve in path.unopened:
            shortest_path = bfs_sp(
                adjacency_list, path.complete_path[-1], unopened_valve
            )
            new_time = path.time + len(shortest_path)
            if new_time > max_time:
                completed_paths.append(path)
                continue
            potential_path = Path(
                new_time,
                path.score + valves[unopened_valve]["rate"] * (max_time - new_time),
                path.unopened - set([unopened_valve]),
                path.complete_path + shortest_path,
            )
            remaining_score = calculate_remaining_score(
                valves, potential_path.unopened, max_time - new_time
            )
            if potential_path.score + remaining_score > max_score:
                paths.append(potential_path)
    return completed_paths


possible_paths = get_paths(valves)
my_answer_a = max([path.score for path in possible_paths])
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)


# %%
def traveler(
    valves, steps, last_valve, time_remaining, state_machine, state, flow, answer
):
    answer[state] = max(answer.get(state, 0), flow)
    for valve in valves:
        minutes = time_remaining - steps[last_valve][valve] - 1
        # Bitmasking for state. Each bit represents valve
        if (state_machine[valve] & state) or (minutes <= 0):
            continue
        # recursion - add this valve to the state. Add this valve to the flow
        traveler(
            valves,
            steps,
            valve,
            minutes,
            state_machine,
            state | state_machine[valve],
            flow + (minutes * valves[valve]["rate"]),
            answer,
        )
    return answer


valves_b = {name: valve for (name, valve) in valves.items() if valve["rate"] > 0}
state_machine = {v: 1 << i for i, v in enumerate(valves_b)}
last_valve = "AA"
starting_state = 0
starting_flow = 0
paths = traveler(
    valves_b, steps, last_valve, 26, state_machine, starting_state, starting_flow, {}
)
total_flow = max(
    my_val + el_val
    for k1, my_val in paths.items()
    for k2, el_val in paths.items()
    if not k1 & k2
)
# %%
my_answer_b = total_flow
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
