# read a csv file,
# put it in a list of lists
# access a specified cell

import csv

from wdlib1 import wdstd

# Replace 'your_file.csv' with the path to your actual CSV file
filename = 'your_file.csv'
filename = wdstd.get_valid_filename('your csv filename', filename)

# Read CSV and store data in a list of lists
# encoding='ansi' for csv from Excel
data = []
with open(filename, newline='', encoding='ansi') as csvfile:
    reader = csv.reader(csvfile, delimiter=';' )
    for row in reader:
        data.append(row)
        print(row)

print ('read csv in list of dictionaries')
datadict = []
with open(filename, newline='', encoding='ansi') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    headers = reader.fieldnames
    print("Headers:", headers)

    for row in reader:
        datadict.append(row)
        print(row)

# Access cell in column 3 of row 11
try:
    cell_value = data[10][2]  # row 11 is index 10, column 3 is index 2
    print(f"Value at row 11, column 3: {cell_value}")
    cell_value = data[10][4]  # row 11 is index 10, column 3 is index 2
    print(f"Value at row 11, column 3: {cell_value}", "of type", type(cell_value))
except IndexError:
    print("The specified cell is out of range.")

# we determine the type of col 1
rownum = 0;
for row in data:
    cell_value = row[1]
    float_value = 'nofloat'
    if wdstd.is_float_de(cell_value):
        float_value = wdstd.get_float_de(cell_value)
    int_value = 'noint'
    if wdstd.is_int(cell_value):
        int_value = wdstd.get_int(cell_value)
    print (rownum, "\"", cell_value, "\"", "istype", type(cell_value), "float", float_value, "int", int_value)
    rownum = rownum + 1

for row in datadict:
    print (rownum, row)
    print (row['%fieldname%'])