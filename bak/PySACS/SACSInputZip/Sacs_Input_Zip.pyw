import os
import zipfile
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

############# Main Process ##############################
if __name__ == "__main__":
    app = wx.PySimpleApp()

    dialog = wx.DirDialog(None, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

    if dialog.ShowModal() == wx.ID_OK:
        folder_name = dialog.GetPath()

    dialog.Destroy()

# folder_name = 'C:\Project\Usan\piperack PR9'

PrjName = os.path.split(folder_name)

org_dir = search(folder_name)

SacsZip = zipfile.ZipFile(PrjName[1] + ".zip","w")

for sf in org_dir:
    for sacs_inp in glob.glob(os.path.join(sf, "*.inp")):
        SacsZip.write(sacs_inp)

    for sacs_run in glob.glob(os.path.join(sf, "*.run")):
        SacsZip.write(sacs_run)

SacsZip.close()


