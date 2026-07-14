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
  electricity_and_heat_co2_emissions: Optional[float]
  electricity_and_heat_co2_emissions_per_capita: Optional[float]
  energy_co2_emissions: Optional[float]
  energy_co2_emissions_per_capita: Optional[float]
  total_co2_emissions_excluding_lucf: Optional[float]
  total_co2_emissions_excluding_lucf_per_capita: Optional[float]

# Linked list of Row objects
@dataclass(frozen=True)
class RLNode:
  first: Row
  rest: Optional['RLNode']

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
     electricity_and_heat_co2_emissions = parse_float_or_none(line[2]),
     electricity_and_heat_co2_emissions_per_capita = parse_float_or_none(line[3]),
     energy_co2_emissions = parse_float_or_none(line[4]),
     energy_co2_emissions_per_capita = parse_float_or_none(line[5]),
     total_co2_emissions_excluding_lucf = parse_float_or_none(line[6]),
     total_co2_emissions_excluding_lucf_per_capita = parse_float_or_none(line[7])
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

# Accepts 'lst' and calculates length
def listlen(lst: RowList) -> int:   
    if lst is None:
       return 0
    return 1 + listlen(lst.rest)

# Helper function that evaluates single Row and returns bool
#  if specified field satisfies comparison
def keep_row(row: Row, 
             field: Literal['country','year',
                                        'electricity_and_heat_co2_emissions',
                                        'electricity_and_heat_co2_emissions_per_capita',
                                        'energy_co2_emissions',
                                        'energy_co2_emissions_per_capita',
                                        'total_co2_emissions_excluding_lucf',
                                        'total_co2_emissions_excluding_lucf_per_capita'], compare_type: 
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
#When field is 'country' compare_type can only be equal
#When field is any of the CO2 emissions the compare_type should only be 
#less_than or greater_than
def filter(lst: RowList, 
           field: Literal['country',
                          'year',
                          'electricity_and_heat_co2_emissions',
                          'electricity_and_heat_co2_emissions_per_capita',
                          'energy_co2_emissions',
                          'energy_co2_emissions_per_capita',
                          'total_co2_emissions_excluding_lucf',
                          'total_co2_emissions_excluding_lucf_per_capita'], 
           compare_type: Literal["less_than", "equal", "greater_than"], 
           compare_val: Any) -> RowList:
  
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

#Checked and 1990 US row has no empty values
def answer_3(lst: RowList) -> RowList:
   correct_year_lst : RowList = filter(lst,'year','equal',1990)
   us_correct_year_rate : Optional[int] = getattr(filter(correct_year_lst,'country',
                                                     'equal','United States'),
                                                     'total_co2_emissions_excluding_lucf_per_capita')
   return filter(correct_year_lst,"total_co2_emissions_excluding_lucf_per_capita",
                 "greater_than", us_correct_year_rate)

def answer_4(lst: RowList) -> RowList:
   correct_year_lst : RowList = filter(lst,'year','equal',2020)
   us_correct_year_rate : Optional[int] = getattr(filter(correct_year_lst,'country',
                                                     'equal','United States').first,
                                                     'total_co2_emissions_excluding_lucf_per_capita')
   return filter(correct_year_lst,"total_co2_emissions_excluding_lucf_per_capita",
                 "greater_than", us_correct_year_rate)

def answer_5(lst: RowList) -> float:
   country_data : RowList = filter(filter(lst,'year','equal',2014),'country','equal','Luxembourg')
   emissions : float = getattr(country_data.first,"electricity_and_heat_co2_emissions")
   emissions_per_capita : float = getattr(country_data.first,'electricity_and_heat_co2_emissions_per_capita')
   return (emissions/emissions_per_capita)*1000000

def answer_6(lst: RowList) -> float:
   pass

def answer_7(lst: RowList) -> float:
   pass


class Tests(unittest.TestCase):
  def test_parse_float_or_none(self):
     self.assertEqual(None, parse_float_or_none(''))
     self.assertEqual(None, parse_float_or_none('  '))
     self.assertEqual(37.9, parse_float_or_none(' 37.9'))
     self.assertEqual(-37.9, parse_float_or_none(' -37.9'))
     self.assertEqual(0.0, parse_float_or_none(' 0.0 '))
  
  def test_lists_to_row(self):
     self.assertEqual(lists_to_row(['abc','2940','0.0','','0.0','','0.0','']),
                      Row('abc',2940,0.0,None,0.0,None,0.0,None))
     self.assertEqual(lists_to_row(['jklasd',"40",'','0.0','','0.0','','0.0']), 
                      Row('jklasd',40,None,0.0,None,0.0,None,0.0))
     self.assertEqual(lists_to_row(['abc','2940','43905.09','2489.7','1.4','0.98',
                                    '4.9','8.0']), 
                      Row('abc',2940,43905.09,2489.7,1.4,0.98,4.9,8.0))
  
 # def test_read_csv_lines(self):
#     self.assertEqual()
  
  def test_listlen(self):
     self.assertEqual(0,listlen(None))
     self.assertEqual(2, listlen(RLNode(Row('abc',2940,43905.09,2489.7,1.4,0.98,4.9,8.0),
                                        RLNode(Row('jdksl',2940,5.09,9.7,1.4,0.98,4.9,8.0),
                                               None))))
     self.assertEqual(3,listlen(RLNode(Row('abc',2940,0.0,None,0.0,None,0.0,None),
                                       RLNode(Row('jklasd',40,None,0.0,None,0.0,None,0.0),
                                              RLNode(Row('a',3,None,None,None,None,None,None),None)))))

  def test_keep_row(self):
     self.assertEqual(True,keep_row(Row('abc',2940,43905.09,2489.7,1.4,0.98,
                                         4.9,8.0),'year','less_than',290000))
     self.assertEqual(False,keep_row(Row('abc',2940,43905.09,2489.7,1.4,0.98,
                                         4.9,8.0),'country','equal',"bc"))
     self.assertEqual(True,keep_row(Row('abc',2940,43905.09,2489.7,1.4,0.98,
                                         4.9,8.0),'total_co2_emissions_excluding_lucf',
                                         'greater_than',0.0))
     self.assertEqual(True,keep_row(Row('abc',2940,43905.09,2489.7,1.4,0.98,
                                         None,8.0),'total_co2_emissions_excluding_lucf'
                                         ,'greater_than',0.0))



  #def test_fillter(self):
     #self.assertEqual()


if __name__ == '__main__':
    unittest.main()