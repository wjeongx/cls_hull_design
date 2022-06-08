import wx
import os
import string

wildcard = "SACS Input files (*.input)|*.input|"     \
           "All files (*.*)|*.*"

if __name__ == "__main__":

     app = wx.PySimpleApp()
     dlg = wx.FileDialog(
                 None, message="Choose a file",
                 defaultDir=os.getcwd(), 
                 defaultFile="",
                 wildcard=wildcard,
                 style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                 )

     if dlg.ShowModal() == wx.ID_OK:
          filename = dlg.GetFilename()
          
     dlg.Destroy()

print filename

fread = 'Bent Support-2_sac.inp'
fr = open(filename,'r')

JOINTS = []

n_jnt = 0

while 1:
     line = fr.readline()
     if not line: break

     if line.strip() == 'JOINT':
          while 1:
               line = fr.readline()
               if line[0:5] != 'JOINT': break

               if (line in JOINTS) == 0:
                    JOINTS.append(line)
                    n_jnt +=1
                    
fr.close

print 'Number of Joints : ' + str(n_jnt-1)
