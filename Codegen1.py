
import csv

from wdlib1 import wdstd

import codegen_helper
from codegen_helper import extract_placeholders

# Replace 'your_file.csv' with the path to your actual CSV file
filename = 'your_file.csv'
filename = wdstd.get_valid_filename('your proc csv filename', filename)

# Read CSV and store data in a list of lists
# encoding='ansi' for csv from Excel
proclist = []
with open(filename, newline='', encoding='ansi') as csvfile:
    reader = csv.reader(csvfile, delimiter=';' )
    for row in reader:
        proclist.append(row)

loop_ix_begin = 0
loop_is_running = False
loop_param = ''

datadict = []
datadict_ix = 0
datarow = []
data_sequ = 0
data_col_dataset = 2
data_col_datatype = 2

proc_col_stmt = 2
proc_col_param = 3
proc_col_template = 4
proc_is_running = True
proc_ix = 0

line_prepared = ''
line_is_prepared = False

variablesdict = {}

filename = 'your_file.csv'
filename = wdstd.get_valid_filename('your data csv filename', filename)

with open(filename, newline='', encoding='ansi') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    headers = reader.fieldnames
    print("Headers:", headers)
    for row in reader:
        datadict.append(row)


def datadict_getfirst():
    global datadict_ix
    global datarow
    global data_sequ
    datadict_ix = 0
    while True:
        datadict_ix += 1
        if datadict_ix >= len(datadict):
            datadict_ix = 0
            break
        datarow = datadict[datadict_ix]
        if datarow['cd'] and datarow['cd'] in 'cx*':
            continue
        if datarow ['dataset'] == loop_param or \
            loop_param == '':
            data_sequ += 1
            break
    return


def datadict_getnext():
    global datadict_ix
    global datarow
    global data_sequ
    while True:
        datadict_ix += 1
        if datadict_ix >= len(datadict):
            datadict_ix = 0
            break
        datarow = datadict[datadict_ix]
        if datarow['cd'] and datarow['cd'] in 'cx*':
            continue
        if datarow['dataset'] == loop_param or \
                loop_param == '':
            data_sequ += 1
            break
    return


def textrow_replace(templateline):
    placeholders = extract_placeholders(templateline)
    for holder in placeholders:
        if holder.startswith('sys-'):
            match holder:
                case 'sys-fieldsequ':
                    textvalue = f"{data_sequ:04d}"
                    templateline = templateline.replace('%' + holder + '%', textvalue)
                case 'test':
                    templateline = templateline.replace('%' + holder + '%', 'something')
                case _: pass
        if holder.startswith('var-'):
            textvalue = variablesdict[holder]
            templateline = templateline.replace('%' + holder + '%', textvalue)
    return templateline


def datarow_replace(templateline, datarow):
    placeholders = extract_placeholders(templateline)
    for holder in placeholders:
        if holder.startswith('col-'):
            datacol = holder.removeprefix('col-')
            templateline = templateline.replace('%' + holder + '%',datarow[datacol])
    return templateline

# overlays line_part on line_prepared
# line_prepared : this is my line
# line_part     :                  next part
# returns       : this is my line  next part
def overlay(line_prepared, line_part):
    pos = len(line_part) - len(line_part.lstrip())

    if pos > len(line_prepared):
        line_prepared += " " * (pos - len(line_prepared)) + line_part.lstrip()
    else:
        line_prepared += " " + line_part.lstrip()

    return line_prepared


def proc_datarow (procrow, datarow):
    global line_is_prepared
    global line_prepared
    templateline = procrow[proc_col_template]
    templateline = textrow_replace(templateline)
    data_datatype = datarow['datatype']
    proc_datatype = procrow[proc_col_param]
    if (proc_datatype == '' or proc_datatype == 'all') or \
        proc_datatype == 'any' and data_datatype != '' or \
        proc_datatype == data_datatype:
        line_part = datarow_replace(templateline, datarow)
        proc_stmt = procrow[proc_col_stmt]
        if proc_stmt == "part":
            if line_is_prepared:
                line_prepared = overlay(line_prepared, line_part)
            else:
                line_is_prepared = True
                line_prepared = line_part
        else:
            if line_is_prepared:
                line_prepared = overlay(line_prepared, line_part)
                line_is_prepared = False
            else:
                line_prepared = line_part
            print (line_prepared)
    return


while proc_is_running:
    proc_ix += 1
    if proc_ix >= len(proclist):
        break
    procrow = proclist[proc_ix]
    proc_stmt = procrow [proc_col_stmt]
    if procrow[0] and procrow[0] in 'cx*':
        if procrow[0] == '':
            print('aber hallo')
        continue
    if proc_stmt == 'loop-begin':
        loop_ix_begin = proc_ix
        loop_is_running = True
        loop_param = procrow[proc_col_param]
        datadict_getfirst()
        # at the end of data we set the proc_ix to the looop-end
        if datadict_ix == 0:
            loop_ix_begin = 0
            loop_is_running = False
            while True:
                proc_ix += 1
                procrow = proclist[proc_ix]
                proc_stmt = procrow[proc_col_stmt]
                if proc_stmt == 'loop-end':
                    break
        continue
    if proc_stmt == 'loop-end':
        datadict_getnext()
        if datadict_ix == 0:
            loop_ix_begin = 0
            loop_is_running = False
        else:
            proc_ix = loop_ix_begin
        continue
    if proc_stmt == '' or proc_stmt == 'part':
        if loop_is_running:
            proc_datarow(procrow, datarow)
        else:
            templateline = procrow[proc_col_template]
            templateline = textrow_replace(templateline)
            print(textrow_replace(templateline))
        continue
    if proc_stmt == "setstr":
        proc_param = procrow[proc_col_param]
        codegen_helper.process_defstr(variablesdict,proc_param)
        continue
    print("wrong statement")