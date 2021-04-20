#!/usr/bin/env python3
# files = ['customers.csv', 'goods.csv', 'items.csv', 'receipts.csv']
import os

filenames=os.listdir('.')
files = list(filter(lambda f: f.endswith('.csv'), filenames))
for file_ in files:
   print(f"------------- {file_} --------------")
   with open(file_) as csv:
       try:
           lines = csv.readlines()
       except:
           continue

   count = 0
   for line in lines:
       if count != 0:
           line = line.strip("\n").split(',')

           line = [record.strip() for record in line]
           for idx in range(1, len(line)):
               try:
                   new = int(line[idx])
                   line[idx] = new
               except:
                   continue

           line = tuple(line)
           if len(line) > 1:
               print(line, ',')
       count+=1

