# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit

today = datetime(year=2022, month=12, day=6)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
puzzle.input_data
# %%
def find_index(input, num_unique):
    unique_counter = 0
    last_letters = []
    for i, letter in enumerate(input):
        print(i, letter, unique_counter, last_letters)
        if letter not in last_letters:
            unique_counter += 1
            last_letters.append(letter)
        else:
            for j, last_letter in enumerate(last_letters):
                if last_letter == letter:
                    last_letters = last_letters[j + 1 :]
                    break
            unique_counter = len(last_letters)
            last_letters = last_letters + [letter]
        if unique_counter == num_unique:
            return i


# %%
my_answer_a = find_index(puzzle.input_data, 4)
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
def find_index_b(input, num_unique):
    unique_counter = 0
    last_letters = []
    for i, letter in enumerate(input):
        print(i, letter, unique_counter, last_letters)
        if letter not in last_letters:
            unique_counter += 1
            last_letters.append(letter)
        else:
            for j, last_letter in enumerate(last_letters):
                if last_letter == letter:
                    last_letters = last_letters[j + 1 :]
                    print("break")
                    break

            last_letters = last_letters + [letter]
            unique_counter = len(last_letters)
        if unique_counter == num_unique:
            return i + 1


# %%
my_answer_b = find_index_b(puzzle.input_data, 14)
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
"mjqjpqmgbljsphdztnvjfqwrcgsmlb"[19]
# %%
