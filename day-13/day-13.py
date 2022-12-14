# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import numpy as np
import ast

today = datetime(year=2022, month=12, day=13)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
raw_input_data = puzzle.input_data
# raw_input_data = """[1,1,3,1,1]
# [1,1,5,1,1]

# [[1],[2,3,4]]
# [[1],4]

# [9]
# [[8,7,6]]

# [[4,4],4,4]
# [[4,4],4,4,4]

# [7,7,7,7]
# [7,7,7]

# []
# [3]

# [[[]]]
# [[]]

# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]"""
pairs = []
for pair in raw_input_data.split("\n\n"):
    pairs.append(
        [ast.literal_eval(pair.split("\n")[0]), ast.literal_eval(pair.split("\n")[1])]
    )
# %%
def calculate_pair(a, b):
    # print("input: ", type(a), type(b), a, b)
    if type(a) == type(b) and type(a) == list:
        for index in range(min([len(a), len(b)])):
            # print("two lists: ", a[index], b[index])
            ret = calculate_pair(a[index], b[index])
            if ret is not None:
                return ret
        if len(a) > len(b):
            return False

    if type(a) != type(b):
        # print("different types")
        if type(a) != list:
            a = [a]
        else:
            b = [b]
        return calculate_pair(a, b)

    if type(a) == list:
        if len(a) < len(b):
            return True
        if len(a) > len(b):
            return False
    else:
        # print("two ints: ", a, b)
        if a < b:
            return True
        if a > b:
            return False


pair_right_order = []
for pair in pairs:
    right_order = calculate_pair(pair[0], pair[1])
    pair_right_order.append(right_order)


# %%
my_answer_a = sum([x + 1 for x in np.where(pair_right_order)[0]])
my_answer_a
# %%
# submit(
#     my_answer_a,
#     part="a",
#     day=today.day,
#     year=today.year,
# )

# %%
import itertools

divider_1 = [[2]]
divider_2 = [[6]]
pairs.append([divider_1, divider_2])
individual_packets = []
for pair in pairs:
    individual_packets.append(pair[0])
    individual_packets.append(pair[1])

combinations = list(itertools.combinations(individual_packets, 2))
combination_right_order = []
for combination in combinations:
    print("combo: ", combination)
    right_order = calculate_pair(combination[0], combination[1])
    combination_right_order.append(right_order)

print("sum combos: ", sum(combination_right_order))
# %%
right_order_dict = {str(key): 0 for key in individual_packets}
for i, combo in enumerate(combinations):
    if combination_right_order[i]:
        right_order_dict[str(combo[0])] += 1
    else:
        right_order_dict[str(combo[1])] += 1
sorted_packets = sorted(right_order_dict.items(), key=lambda x: x[1], reverse=True)
# sorted_packets[:5]
sorted_packets_list = np.array([packet[0] for packet in sorted_packets])
sorted_packets_list
# %%
# print(sorted_packets_list)
# print(str(divider_1))
# print(np.where(sorted_packets_list == str(divider_1))[0][0])
my_answer_b = (np.where(sorted_packets_list == str(divider_1))[0][0] + 1) * (
    np.where(sorted_packets_list == str(divider_2))[0][0] + 1
)
my_answer_b

# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
