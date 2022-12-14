# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit

today = datetime(year=2022, month=12, day=5)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
initial_stack_raw = puzzle.input_data.split("\n\n")[0].split("\n")
initial_stack_raw
# %%
ids = initial_stack_raw[-1].lstrip().rstrip().split()
ids
# %%
inital_stacks = {id: [] for id in ids}
for row in initial_stack_raw[:-1]:
    for id in ids:
        val = row[int(id) * 4 - 3].strip()
        if val:
            inital_stacks[id].append(val)
print(inital_stacks)
# %%
instructions = initial_stack_raw = puzzle.input_data.split("\n\n")[1].split("\n")
instructions
# %%
def extract_instruction(instruction):
    num_to_move = int(instruction.split()[1])
    from_index = instruction.split()[3]
    to_index = instruction.split()[5]
    return num_to_move, from_index, to_index


extract_instruction(instructions[0])
# %%
stacks_2 = inital_stacks.copy()


def move_pieces(num_to_move, from_index, to_index, stacks):
    print(stacks[to_index])
    print(stacks[from_index])
    for i in range(num_to_move):
        to_move = stacks[from_index].pop(0)
        print(to_move)
        stacks[to_index].insert(0, to_move)
    return stacks


for instruction in instructions:
    print(stacks_2)
    num_to_move, from_index, to_index = extract_instruction(instruction)
    stacks_2 = move_pieces(num_to_move, from_index, to_index, stacks_2)
print(stacks_2)
# %%
my_answer_a = "".join([stacks_2[key][0] for key in stacks_2])
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
def move_pieces_b(num_to_move, from_index, to_index, stacks):
    print(from_index, to_index)
    print(stacks[to_index])
    print(stacks[from_index])
    for i in range(num_to_move):
        print(i, num_to_move)
        to_move = stacks[from_index].pop(num_to_move - i - 1)
        print(to_move)
        stacks[to_index].insert(0, to_move)
    return stacks


stacks_b = inital_stacks.copy()
print(stacks_b)
for instruction in instructions:
    print(instruction)
    num_to_move, from_index, to_index = extract_instruction(instruction)
    stacks_b = move_pieces_b(num_to_move, from_index, to_index, stacks_b)
print(stacks_b)
# %%
my_answer_b = "".join([stacks_b[key][0] for key in stacks_b])
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)

# %%
