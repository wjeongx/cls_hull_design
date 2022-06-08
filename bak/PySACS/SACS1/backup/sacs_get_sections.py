import wx
import string

fread = 'Bent Support-2_sac.inp'
fr = open(fread,'r')

SECTS = []

n_sec = 0

while 1:
     line = fr.readline()
     if not line: break

     if line.strip() == 'SECT':
          while 1:
               line = fr.readline()
               if line[0:4] != 'SECT': break

               if (line in SECTS) == 0:
                    SECTS.append(line)
                    n_sec +=1
                    
fr.close

print 'Number of Sections(SECT) : ' + str(n_sec-1)
