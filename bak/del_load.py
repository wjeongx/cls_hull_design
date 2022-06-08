import wx
import string

fread = 'Group10-LM8_sac.inp'
fr = open(fread,'r')

while 1:
     line = fr.readline()
     if not line: break
    
     x1 = line[7:11]
     x2 = line[11:15]
     
     if line.strip() == 'MEMBER':
          member_line = []
          idx = 0
          while 1:
               line = fr.readline()
               if line[0:6] != 'MEMBER': break

               member_line.append(line)
#               print member_line[idx]
               idx +=1

fr.close

fr = open(fread,'r')
fwrite = 'Group10-LM8_sac2.inp'
fw = open(fwrite, 'w')
while 1:
     line = fr.readline()
     if not line: break
 
     if line[0:5] == 'LOAD ':
          tf1 = 0
          tf2 = 0
          for member in member_line:
               if member[7:15] != line[7:15]:
                    tf1= 0
               else:
                    tf2=1

          if tf1+tf2 == 0:
               line = "***" + line

     fw.write(line)

fr.close
fw.close









          
     
#     if line[0:7] == 'MEMBER ':
#         print line

#     if line[0:5] == 'LOAD ':
#         print line

#     fw.write(line)

fw.close
    
