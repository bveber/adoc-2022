# %%
from datetime import datetime
from aocd.models import Puzzle
from aocd import submit
from pprint import pprint
import numpy as np

today = datetime(year=2022, month=12, day=13)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
