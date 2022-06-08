import wx
import string
from get_sacs_data import *

import os

def open_sacs_input_file():

     filename = ''
     
     wildcard = "SACS Input files (*.inp)|*.inp|"     \
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

     return filename

fread = open_sacs_input_file()
            
MEMBER = []
JOINT = []
n_member, MEMBER = get_sacs_member(fread)
n_joint, JOINT = get_sacs_joint(fread)

file_name = os.path.split(fread)
file_name = os.path.splitext(file_name[1])

fwrite = file_name[0] + '.members'

fw = open(fwrite,'w')

fw.write('MEMBER\n')

for memb in MEMBER:
     ja = [JOINT[memb['JA']][0], JOINT[memb['JA']][1], JOINT[memb['JA']][2]]

     jb = [JOINT[memb['JB']][0], JOINT[memb['JB']][1], JOINT[memb['JB']][2]]
     
     dif = [abs(ja[0]-jb[0]), abs(ja[1]-jb[1]), abs(ja[2]-jb[2])]
            
     if dif[0] == max(dif):
          if ja[0] <= jb[0]:
               mmemb = memb['JA'] + memb['JB']
          else:
               mmemb = memb['JB'] + memb['JA']
     elif dif[1] == max(dif):
          if ja[1] <= jb[1]:
               mmemb = memb['JA'] + memb['JB']
          else:
               mmemb = memb['JB'] + memb['JA']
     elif dif[2]== max(dif):
          if ja[2] <= jb[2]:
               mmemb = memb['JA'] + memb['JB']
          else:
               mmemb = memb['JB'] + memb['JA']
          
     fw.write(memb['DLST'][:7] + mmemb+ memb['DLST'][15:])

fw.close     

print "Process Complete"

fr = open(fwrite, 'r')

























