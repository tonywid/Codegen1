import sys

print(sys.path) # shows all directories Python searches

from wdlib1 import wdstd
print(wdstd.is_int("abc"))


teststring = ''
if teststring:
    print('ja')
else:
    print('no')
if '' in 'abc':
    print ('ja')
else:
    print ('no')
