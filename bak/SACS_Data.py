from string import *
import scipy
import os
import glob
import wx

f_struct = []

def search(dir_name):
    sub_dir_list = os.listdir(dir_name)
    for sub_dir in sub_dir_list:
        f = os.path.join(dir_name, sub_dir)
        if os.path.isdir(f):
            search(f)
            f_struct.append(f)

    return f_struct

def run():
    ############# Main Process ##############################
    if __name__ == "__main__":
        app = wx.PySimpleApp()

        dlg  = wx.FileDialog(
            None, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="All files (*.*)|*.*",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetPaths()

        dlg.Destroy()

    f = open(file_name,'r')
    fout = open('frame.dat','w')
    while 1:
        line = f.readline()
        fout.writeline(line)

        if len(line) <=0: break
        
    f.close()    
    fout.close()

run()
