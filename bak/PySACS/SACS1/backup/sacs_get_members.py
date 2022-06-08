import wx
import string

fread = 'Bent Support-2_sac.inp'
fr = open(fread,'r')

n_mem = 0
MEMBERS=[]
while 1:
     line = fr.readline()
     if not line: break

     if line.strip() == 'MEMBER':
          while 1:
               line = fr.readline()
               if line[0:6] != 'MEMBER': break

               if line[7:16].strip() == 'OFFSETS':
                    n_mem -=1
                    MEMBERS[n_mem] = MEMBERS[n_mem] + line
                    n_mem +=1
               else:
                    if (line in MEMBERS) == 0:
                         MEMBERS.append(line)
                         n_mem +=1

fr.close

print 'Number of Members(MEMBER) : ' + str(n_mem-1)



    
