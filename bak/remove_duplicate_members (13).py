import wx
import string

fread = 'Bent Support._sac.inp'
fr = open(fread,'r')
MEMBERS = []
idx = 0

while 1:
     line = fr.readline()
     if not line: break

     if line.strip() == 'MEMBER':
          while 1:
               line = fr.readline()
               if line[0:6] != 'MEMBER': break

               if line[7:16].strip() == 'OFFSETS':
                    idx -=1
                    MEMBERS[idx] = MEMBERS[idx] + line
                    idx +=1
               else:
                    if (line in MEMBERS) == 0:
                         MEMBERS.append(line)
                         idx +=1

print MEMBERS[idx-1]

fr.close

fwrite = 'Bent Support._sac2.inp'
fw = open(fwrite,'w')

for xid in range(0, idx):
     fw.write(MEMBERS[xid])

fw.close     




    
