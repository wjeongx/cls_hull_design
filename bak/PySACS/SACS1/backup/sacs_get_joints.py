import wx
import os
import string

fread = 'Bent Support-2_sac.inp'
fr = open(fread,'r')

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

print 'Number of Joints(JOINT) : ' + str(n_jnt-1)
