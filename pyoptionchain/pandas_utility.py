import xlwt
from tempfile import TemporaryFile
from pandas import DataFrame

EXCEL_INITIAL_FILENAME = "option_chain.xls"

def pickColumns(dictData):

    df = DataFrame(dictData)
    finalCols = df.ix[:,['strike','p','c','b','a','vol','oi']]

    return finalCols.values

def writeToExcel(listData, fullpath):

    xlsWorkBook = xlwt.Workbook()
    sheet = xlsWorkBook.add_sheet("option chain")

    for ind, l in enumerate(listData):
        for ind2, col in enumerate(l):
            sheet.write(ind, ind2, col)

    xlsWorkBook.save(fullpath)
    xlsWorkBook.save(TemporaryFile())