# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit

today = datetime(year=2022, month=12, day=4)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
pairs = [val.split(",") for val in puzzle.input_data.split("\n")]
pairs[:5]
# %%
def get_all_sections(section_str):
    return set(
        range(int(section_str.split("-")[0]), int(section_str.split("-")[1]) + 1)
    )


# %%
get_all_sections("7-96")
# %%
overlap_counter = 0
for pair in pairs:
    sections_0 = get_all_sections(pair[0])
    sections_1 = get_all_sections(pair[1])
    if len(sections_0.intersection(sections_1)) == min(
        [len(sections_0), len(sections_1)]
    ):
        overlap_counter += 1
my_answer_a = overlap_counter
print(my_answer_a)
# %%
len(pairs)
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
overlap_counter = 0
for pair in pairs:
    sections_0 = get_all_sections(pair[0])
    sections_1 = get_all_sections(pair[1])
    if len(sections_0.intersection(sections_1)) > 0:
        overlap_counter += 1
my_answer_b = overlap_counter
print(my_answer_b)
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
