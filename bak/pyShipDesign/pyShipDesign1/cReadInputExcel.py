import math as mth
import xlrd
import xlsxwriter

class ReadInputExcel:
    def __init__(self, BookName, SheetName):
        self.BookName = BookName
        self.SheetName = SheetName
        self.wb = xlrd.open_workbook(self.BookName)
        self.ws = self.wb.sheet_by_name(self.SheetName)
   
    def read_input_column(self, nrow, row_start, i_col):
        self.data = []
        for i in range(0, nrow):
            self.data.append(self.ws.cell(i+row_start-1,i_col-1).value)
        return self.data
    
    def read_input_col_row(self, ncol, nrow, col_start, row_start):
        self.data = []
        for i in range(0, ncol):
            self.data.append([])
            for j in range(row_start, row_start + nrow):
                self.data[i].append(self.ws.cell(j-1, i + col_start-1).value)
        return self.data
       
rie = ReadInputExcel('Colorado_Summary.xlsx', "DeckLoading")

deck_name = rie.read_input_column(5, 4, 1)
deck_loc = rie.read_input_column(5, 4, 2)
deck_sw = rie.read_input_column(5, 4, 3)
lc_name = rie.read_input_column(11, 13, 1)
tlc = rie.read_input_column(11,13,2)
GM = rie.read_input_column(11,13,3)
kr = rie.read_input_column(11,13,4)
mc = rie.read_input_col_row(11, 5, 2, 35)

print(mc)

"""
print(deck_name)
print(deck_loc)
print(deck_sw)
print(lc_name)
print(GM)
print(kr)
"""