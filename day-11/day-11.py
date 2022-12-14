# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import math

today = datetime(year=2022, month=12, day=11)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
input_data = puzzle.input_data.split("\n\n")
input_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".split(
    "\n\n"
)
print(input_data)
# %%
def parse_test(test):
    div_by = test[0].split()[-1]
    true_cond = test[1][-1]
    false_cond = test[2][-1]
    return div_by, true_cond, false_cond


def parse_input(input_data):
    monkies = {}
    for monkey in input_data:
        monkey_split = monkey.split("\n")
        key = monkey_split[0][:-1]
        items = monkey_split[1][18:].split(", ")
        operation = monkey_split[2][19:]
        test = parse_test(monkey_split[3:])

        monkies[key] = {
            "items": items,
            "operation": operation,
            "test": test,
            "items_counted": 0,
        }
    return monkies


monkies = parse_input(input_data)
monkies
# %%
for i in range(20):
    for monkey in sorted(monkies):
        items = monkies[monkey]["items"]
        for item in items:
            old = int(item)
            new = int(eval(monkies[monkey]["operation"]))
            new = math.floor(new / 3)
            if new % int(monkies[monkey]["test"][0]) == 0:
                monkies["Monkey " + monkies[monkey]["test"][1]]["items"].append(new)
            else:
                monkies["Monkey " + monkies[monkey]["test"][2]]["items"].append(new)
            monkies[monkey]["items"] = []
            monkies[monkey]["items_counted"] += 1
print(monkies)
# %%
top2 = sorted([monkies[monkey]["items_counted"] for monkey in monkies])[-2:]
my_answer_a = top2[0] * top2[1]
my_answer_a
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
input_data = puzzle.input_data.split("\n\n")
# input_data = """Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1""".split(
#     "\n\n"
# )
print(input_data)
monkies = parse_input(input_data)
monkies
# %%
vals = [int(monkies[monkey]["test"][0]) for monkey in monkies]
mod = 1
for val in vals:
    mod *= val
print(mod)
for i in range(10000):
    print(i)
    for monkey in sorted(monkies):
        # print(monkey)
        items = monkies[monkey]["items"]
        for item in items:
            # print(item)
            old = int(item)
            new = int(eval(monkies[monkey]["operation"])) % mod
            # print("new: ", new)
            # new = math.floor(new / 3)
            if new % int(monkies[monkey]["test"][0]) == 0:
                monkies["Monkey " + monkies[monkey]["test"][1]]["items"].append(new)
            else:
                monkies["Monkey " + monkies[monkey]["test"][2]]["items"].append(new)
            monkies[monkey]["items"] = []
            monkies[monkey]["items_counted"] += 1
print(monkies)
top2 = sorted([monkies[monkey]["items_counted"] for monkey in monkies])[-2:]
my_answer_b = top2[0] * top2[1]
my_answer_b
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)

# %%
