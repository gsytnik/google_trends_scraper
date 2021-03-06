#!/usr/bin/env python3
import csv
from glob import glob

def handle_int_float_csv(d):
  if not d:
      return d
  try:
      f = float(d)
      i = int(f)
      return i if f == i else f
  except ValueError:
      return d


# Get all the CSV file in the directory
for file in glob('*.csv'):
  with open(file) as f:
    # this will remove _countries attatched from CSV file name, returning just the term
    term = file[0:-7]
    print(f'\n------------{file}---------\n')
    r = csv.reader(f)
    next(r)   
    for row in r:
        row = row[2:]
        row.append(term)
        row = tuple(list(map(handle_int_float_csv,row)))
        print(row)


