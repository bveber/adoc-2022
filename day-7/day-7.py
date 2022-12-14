# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
import os

today = datetime(year=2022, month=12, day=7)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
# %%
input_data = puzzle.input_data
# input_data = """
# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k
# """
# %%
from pprint import pprint

pprint(input_data)

# %%
pprint(input_data.split("$ ")[1:10])
# %%
dir_dict = {}
current_directory = ""
for selection in input_data.split("$ ")[1:]:
    # print(selection)
    if "cd " in selection:
        directory = selection.replace("cd ", "").strip()
        print("parsed directory: ", directory)
        # print('parent directory: ', parent_directory)
        if directory == "..":
            # move up one level
            current_directory = "/".join(current_directory.split("/")[:-1])
            print("move down one level ", current_directory)
        elif directory == "/" or "":
            # move to parent
            current_directory = "/"
        else:
            # move down one level
            current_directory = os.path.join(current_directory, directory)
        if current_directory == "":
            current_directory = "/"

        print("current directory: ", current_directory)
        # if current_directory not in dir_dict:
        #     dir_dict[current_directory] = []
        dir_split = current_directory.split("/")[1:-1]
        print("dir split: ", dir_split)
    else:
        for row in selection.rstrip().split("\n")[1:]:
            # print(row)
            if "dir " in row or row == "ls":
                continue
            try:
                size, filename = row.split()
                size = int(size)
                if current_directory not in dir_dict:
                    dir_dict[current_directory] = [(size, filename)]
                else:
                    dir_dict[current_directory].append((size, filename))
                if current_directory != "/":
                    dir_dict["/"].append((size, filename))
                for i in range(len(dir_split)):
                    if i == 0:
                        dir_split_filtered = dir_split
                    else:
                        dir_split_filtered = dir_split[:-i]
                    print("for loop dir_split: ", dir_split_filtered)
                    lower_directory = "/" + "/".join(dir_split_filtered)
                    print("lower directory: ", lower_directory)
                    if lower_directory == "/":
                        print("skipping")
                        continue
                    else:
                        # print(lower_directory)
                        if lower_directory not in dir_dict:
                            dir_dict[lower_directory] = [(size, filename)]
                        else:
                            dir_dict[lower_directory].append((size, filename))
                        print("lower: ", lower_directory)
                        pprint(dir_dict[lower_directory])
                print("current: ", current_directory)
                pprint(dir_dict[current_directory])

            except TypeError:
                continue
    # pprint(dir_dict)
    print("current directory: ", current_directory)
    print("---end selection---")

pprint(dir_dict)

# %%

sum_dict = {k: sum([val[0] for val in dir_dict[k]]) for k in dir_dict}
pprint(sum_dict)
# %%
max_size = 100000
my_answer_a = sum([sum_dict[k] for k in sum_dict if sum_dict[k] <= max_size])
print(my_answer_a)
# %%
submit(
    my_answer_a,
    part="a",
    day=today.day,
    year=today.year,
)
# %%
total_size = 70000000
used_size = sum_dict["/"]
unused_size = total_size - used_size
size_needed = 30000000
folders_to_delete = sorted(
    [
        (unused_size + sum_dict[k])
        for k in sum_dict
        if (unused_size + sum_dict[k]) >= size_needed
    ]
)
folders_to_delete
# %%
unused_size
# %%
my_answer_b = folders_to_delete[0] - unused_size
print(my_answer_b)
# %%
submit(
    my_answer_b,
    part="b",
    day=today.day,
    year=today.year,
)
# %%
