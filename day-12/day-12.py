# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import numpy as np

today = datetime(year=2022, month=12, day=12)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
raw_input_data = puzzle.input_data
# raw_input_data = """Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi"""
input_data = []
for row in raw_input_data.split("\n"):
    input_data.append([val for val in row])
input_data = np.array(input_data)
print(input_data.shape)
print(raw_input_data)
# %%
class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return f"Node({self.position}, {self.g}, {self.h}, {self.f})"


def path_heuristic(current_position, end):
    return np.sqrt(
        (end[0] - current_position[0]) ** 2
        + (end[1] - current_position[1]) ** 2
        + (end[2] - current_position[2]) ** 2
    )


def get_ord(val):
    if val == "E":
        val = "z"
    if val == "S":
        val = "a"
    return ord(val)


def find_neighbors(map, current_node):
    x, y, z = current_node.position
    current_value = map[y, x]
    neighbors = []
    # print(ord(map[y, x - 1]), ord(current_value))
    if (x - 1) >= 0 and (get_ord(map[y, x - 1]) - get_ord(current_value)) <= 1:
        neighbors.append((x - 1, y, get_ord(map[y, x - 1])))
    if (x + 1) < map.shape[1] and (
        get_ord(map[y, x + 1]) - get_ord(current_value)
    ) <= 1:
        neighbors.append((x + 1, y, get_ord(map[y, x + 1])))
    if (y - 1) >= 0 and (get_ord(map[y - 1, x]) - get_ord(current_value)) <= 1:
        neighbors.append((x, y - 1, get_ord(map[y - 1, x])))
    if (y + 1) < map.shape[0] and (
        get_ord(map[y + 1, x]) - get_ord(current_value)
    ) <= 1:
        neighbors.append((x, y + 1, get_ord(map[y + 1, x])))
    return neighbors


def astar(map, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given map"""

    # Create start and end node
    start_node = Node(None, start)
    print("start_node: ", start_node)
    end_node = Node(None, end)
    print("end_node: ", end_node)

    # Initialize both open and closed list
    open_list = []
    # Using a set instead of a list increased runtime performace > 20x
    closed_list = set()

    # Add the start node
    open_list.append(start_node)
    i = 0
    # Loop until you find the end
    while len(open_list) > 0:
        print(i)
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.add(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for node_position in find_neighbors(map, current_node):  # Adjacent squares
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            if child not in closed_list:
                child.g = current_node.g + 1
                child.h = path_heuristic(child.position, end_node.position)
                child.f = child.g + child.h
                skip = False
                for open_node in open_list:
                    if child == open_node and child.g >= open_node.g:
                        skip = True
                if not skip:
                    open_list.append(child)
        i += 1


# %%
start_position = (
    np.where(input_data == "S")[1][0],
    np.where(input_data == "S")[0][0],
    get_ord("S"),
)
end_position = (
    np.where(input_data == "E")[1][0],
    np.where(input_data == "E")[0][0],
    get_ord("E"),
)
print(start_position, end_position)
path = astar(input_data, start_position, end_position)
# %%
my_answer_a = len(path) - 1
my_answer_a

# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)

# %%
other_starting_positions_ind = np.where(input_data == "a")
other_starting_positions = []
for i in range(len(other_starting_positions_ind[0])):
    other_starting_positions.append(
        (
            other_starting_positions_ind[1][i],
            other_starting_positions_ind[0][i],
            get_ord("a"),
        )
    )

len_paths = [my_answer_a]
for i, start_position in enumerate(other_starting_positions):
    print(i)
    path = astar(input_data, start_position, end_position)
    if path:
        len_paths.append(len(path) - 1)
print(min(len_paths))
# %%
my_answer_b = min(len_paths)
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)

# %%
