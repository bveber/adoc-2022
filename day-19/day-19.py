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

today = datetime(year=2022, month=12, day=19)
puzzle = Puzzle(year=today.year, day=today.day)
# %%
