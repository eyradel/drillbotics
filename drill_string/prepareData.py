import openpyxl
from fractions import Fraction

# Open the Excel file
def parse(val: str, col: str):
    val_ = val
    cols = ['A', 'E', 'F', 'G', 'H']
    types_ = [float, int]
    if col in cols:
        if type(val) not in types_:
            if val is not None:
                if val[1:2] == ' ':
                    val_ = float(val[0]) + float(val[2:])
                else:
                    if val == '-' or val == 'null':
                        val_ = None
                    else:
                        val_ = float(val)
                
    return val_

workbook = openpyxl.load_workbook('drillstring/saved_Api.xlsx')

# Select the active sheet
sheet = workbook.active
# Iterate through each cell in the sheet
row = 1
while row < 400:
    column = 'A'
    while column < 'O':
        # Check the cell value can be converted to float
        if row > 1:
            sheet[column+str(row)] = parse(sheet[column+str(row)].value, column)
        else:
            sheet[column+str(row)] = sheet[column+str(row)].value

        column = chr(ord(column) + 1)
    row += 1

workbook.save('modified_file.xlsx')
