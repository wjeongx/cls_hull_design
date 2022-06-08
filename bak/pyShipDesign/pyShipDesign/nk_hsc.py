from math import *
import xlrd


class nk_hsc:
    g0 = 9.81

    def __init__(self, BookName, SheetName):
        self.BookName = BookName
        self.SheetName = SheetName

        wb = xlrd.open_workbook(BookName)
        sht = wb.sheet_by_name(SheetName)    

        self.shiptype = sht.cell(0,2).value
        self.sociaty = sht.cell(1,2).value
        if self.sociaty == "NK":
            self.Analysis_Type = sht.cell(2,2).value
            self.ServiceNotation = sht.cell(3,2).value
            self.BK = sht.cell(4,2).value
        
        self.Ls = sht.cell(5,2).value
        self.B = sht.cell(6,2).value
        self.D = sht.cell(7,2).value
        self.Ts = sht.cell(8,2).value
        self.Cb = sht.cell(9,2).value
        self.Vs = sht.cell(10,2).value

        self.GM = sht.cell(11,2).value
        self.kr = sht.cell(12,2).value

 
class design_loads(nk_hsc):
# 1.2.3 Range of Strengthened Bottom Forward 
    def Range_Strengthened_Bottom_Forward(self):
        fwd_rng = 0.1*self.Ls*(4+self.Vmax/pow(10*W,1/6))
        
        return fwd_rng
    
# 1.5.2 Minimum Thickness
    def min_thickness(self):
        
        t_min = g * sqrt(self.Ls)
        
        return t_min
        
    def value_of_gamma(self, fy):

        fs = sqrt(235/fy)
        fa = sqrt(128/fy)
        
        print("====== Welcome to NK HSC Code ============")
        print()
        
        pos_code = input ("""
            '0 : Bottom shell plating',
            '1 : Side shell plating',
            '2 : Exposed deck plating',
            '3 : Cargo/car deck plating',
            '4 : Other deck plating',
            '5 : Watertight bulkhead plating',
            '6 : Deep Tank Bulkhead plating' """ 
 "\n             Input position Code : ")
            
        position = [
            'Bottom shell plating',
            'Side shell plating',
            'Exposed deck plating',
            'Cargo/car deck plating',
            'Other deck plating',
            'Watertight bulkhead plating',
            'Deep Tank Bulkhead plating']
        
        gamma = {
            'Bottom shell plating' : 0.75*fa,
            'Side shell plating' : 0.65*fa,
            'Exposed deck plating' : 0.65*fa,
            'Cargo/car deck plating' : 0.65*fa,
            'Other deck plating' :0.65*fa,
            'Watertight bulkhead plating' : 0.65*fa,
            'Deep Tank Bulkhead plating' :0.62*fa
            }        
        
        t_min = gamma * float(sqrt(self.Ls))
        
#       return gamma[position[int(pos_code)]]
        return t_min
    

        