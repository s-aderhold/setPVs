from csv import DictReader

from epics import caput

input_file = DictReader(open('TableToSetCMNames.csv'))

for row in input_file:
    print(row)
    caput(row['\ufeffPV'], row['SN'])
