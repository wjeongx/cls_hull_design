import wx
import string

fread = 'Bent Support-2_sac.inp'
fr = open(fread,'r')

LCOMBS = []

n_lcs = 0

while 1:
     line = fr.readline()
     if not line: break

     if line.strip() == 'LCOMB':
          while 1:
               line = fr.readline()
               if line[0:5] != 'LCOMB': break

               if (line in LCOMBS) == 0:
                    LCOMBS.append(line)
                    n_lcs +=1
                    
fr.close

print 'Number of Load combine(LCOMB) : ' + str(n_lcs-1)
