import xlrd


data = xlrd.open_workbook('excelFile.xls')
table = data.sheets()[0]

for i in range(10):
    for y in range(10):
        table.put_cell(i, y, 1, i, 1)

