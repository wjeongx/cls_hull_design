import wx
import os
import string
from get_sacs_data import *

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
n_memb, MEMBER = get_sacs_member(fread)
n_jnt, JOINT = get_sacs_joint(fread)

n_joint, JOINTS = sacs_get_joint_name(fread)

file_name = os.path.split(fread)
file_name = os.path.splitext(file_name[1])

fwrite = file_name[0] + '.angle'

fw = open(fwrite,'w')

fw.write('MEMBER\n')

idx = 0
for MEMB in MEMBER:
     if MEMB['GRP'] == 'ANG':
          JOINT[MEMB['JA']][4] = JOINT[MEMB['JA']][4] + 1
          JOINT[MEMB['JA']][5].append([idx,MEMB['GRP'],MEMB['JB']])
          
          JOINT[MEMB['JB']][4] = JOINT[MEMB['JB']][4] + 1
          JOINT[MEMB['JB']][5].append([idx, MEMB['GRP'],MEMB['JA']])

     idx +=1

for JNT in JOINTS:
     if JOINT[JNT[0]][4] == 4:
          for i in range(0,4):
               MMEMB = JNT[0]+ JOINT[JNT[0]][5][i][2]

               MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'] = MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'][:7] + MMEMB + MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'][15:]               

#               fw.write(MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'])

for MEMB in MEMBER:
     fw.write(MEMB['DLST'])

fw.close     

print "Process Complete"


























