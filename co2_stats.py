import csv
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

# Single parsed line of the gas emissions data
@dataclass(frozen=True)
class Row:
  country: str
  year: int
  electricity_and_heat_total: Optional[float]
  electricity_and_heat_per_capita: Optional[float]
  energy_total: Optional[float]
  energy_per_capita: Optional[float]
  total_excluding_land_use_total: Optional[float]
  total_excluding_land_use_per_capita: Optional[float]

# Linked list of Row objects
@dataclass(frozen=True)
class RLNode:
  first: Row
  rest: 'RLNode'

RowList = Optional[RLNode]

# Helper function to convert CSV strings to a float or None
def parse_float_or_none(value: str) -> Optional[float]:
  pass

# Turns string list from CSV to structured Row
def lists_to_row(line: List[str]) -> Row:
  pass

# Accepts the name of CSV file, reads it, and makes linked list of Row objects
def read_csv_lines(filename: str) -> RowList:
  pass

# Accepts linked list of Row objects and calculates length
def list_length(list: RowList) -> int:
  pass

# Filters linked list based on name and compares
def filter_rows(list: RowList, field: str, compare_type: str, compare_val: Any) -> RowList:
  pass

class Tests(unittest.TestCase):
  pass
if (__name__ == '__main__'):
  unittest.main()
