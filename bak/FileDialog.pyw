import os
import wx
import string

def FileDialog():
    app = wx.PySimpleApp()

    dlg = wx.FileDialog(None, "Choose a file", "","","*.lst",wx.MULTIPLE)

    if dlg.ShowModal() == wx.ID_OK:
        fname = dlg.GetPaths()

    dlg.Destroy()

    return fname[0]

if __name__ == "__main__":
    fname = FileDialog()
    print fname
