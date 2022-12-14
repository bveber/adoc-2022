# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit

today = datetime.datetime(year=2022, month=12, day=3)
puzzle = Puzzle(year=today.year, day=today.day)

# %%
rucksacks = [
    [val[: int(len(val) / 2)], val[int(len(val) / 2) :]]
    for val in puzzle.input_data.split("\n")
]
print(rucksacks[:5])


# %%
def get_piece_priority(piece):
    adder = 0
    if piece.isupper():
        adder = 26
    return ord(piece) % 32 + adder


def find_shared_piece(pieces):
    intersection = set(pieces[0])
    for piece in pieces[1:]:
        intersection = intersection.intersection(piece)
    return "".join(intersection)


# %%
my_answer_a = sum(
    [get_piece_priority(find_shared_piece(rucksack)) for rucksack in rucksacks]
)
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)

# %%
full_rucksacks = [val for val in puzzle.input_data.split("\n")]
counter = 0
group_rucksacks = []
temp_rucksacks = []
for rucksack in full_rucksacks:
    temp_rucksacks.append(rucksack)
    counter += 1
    if counter % 3 == 0:
        group_rucksacks.append(temp_rucksacks)
        temp_rucksacks = []

print(group_rucksacks[:3])
# %%
my_answer_b = sum(
    [get_piece_priority(find_shared_piece(rucks)) for rucks in group_rucksacks]
)
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
