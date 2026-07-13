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
    cleaned = value.strip()
    if cleaned == "":
       return None
    return float(cleaned)

# Turns string list from CSV to structured Row object
def lists_to_row(line: List[str]) -> Row:
  return Row(
     country = line[0],
     year = int(line[1]),
     electricity_and_heat_total = parse_float_or_none(line[2]),
     electricity_and_heat_per_capita = parse_float_or_none(line[3]),
     energy_total = parse_float_or_none(line[4]),
     energy_per_capita = parse_float_or_none(line[5]),
     total_excluding_land_use_total = parse_float_or_none(line[6]),
     total_excluding_land_use_per_capita = parse_float_or_none(line[7])
  )

# Reads a CSV file and created a linked list of Row Objects
def read_csv_lines(filename: str) -> RowList:
   head: RowList = None
   with open(filename, newline = "", encoding = "utf-8") as csvfile:
       reader = csv.reader(csvfile)
       try:
          next(reader)
       except StopIteration:
          return None
       for line in reader:
          row_data = lists_to_row(line)
          head = RLNode(row_data, head)
   return head

# Accepts linked list of Row objects and calculates length
def listlen(lst: RowList) -> int:   
    if lst is None:
       return 0
    return 1 + listlen(lst.rest)

# Helper function that evaluates single Row and returns bool
#  if specified field satisfies comparison
def keep_row(row: Row, field: str, compare_type: 
             Literal["less_than", "equal", "greater_than"], 
             compare_val: Any) -> bool:
   val = getattr(row, field)
   if val is None:
      return False
   
   if compare_type == "equal":
      return val == compare_val
   
   elif compare_type == "less_than":
      return val < compare_val
   
   elif compare_type == "greater_than":
      return val > compare_val
   
   else:
      raise ValueError(f"Invalid comparison type: {compare_type}")
      
# Filters linked list based on name and compares
def filter(lst: RowList, 
                field: str, compare_type: str, compare_val: Any) -> RowList:
  
  if lst is None:
     return None
  
  if keep_row(lst.first, field, compare_type, compare_val):
     return RLNode(lst.first, filter(lst.rest, field, 
                                     compare_type, compare_val))
  
  else:
     return filter(lst.rest, field, compare_type, compare_val)
  
# Questions 1 through 7
def answer_1(lst: RowList) -> int:
   year_2020_data = filter(lst, "year", "equal", 2020)
   return listlen(year_2020_data)

def answer_2(lst: RowList) -> RowList:
   return filter(lst, "country", "equal", "Mexico")

def answer_3(lst: RowList) -> RowList:
   pass

def answer_4(lst: RowList) -> RowList:
   pass

def answer_5(lst: RowList) -> float:
   pass

def answer_6(lst: RowList) -> float:
   pass

def answer_7(lst: RowList) -> float:
   pass


class Tests(unittest.TestCase):


if __name__ == '__main__':
    unittest.main()