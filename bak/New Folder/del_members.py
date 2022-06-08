import wx

fread = 'Bent Support-1_sac.inp'
fwrite = 'Bent Support._sac1.inp'
fr = open(fread,'r')
fw = open(fwrite, 'w')

while 1:
     line = fr.readline()
     if not line: break
    
     x1 = line[7:11]
     x2 = line[11:15]
     
     if line[0:6] == 'MEMBER':
         if x1 == x2:
             line = '***' + line
             print line

     if line[0:4] == 'LOAD':
         if x1 == x2:
             line = '***' + line
             print line

     fw.write(line)
fr.close
fw.close
    
