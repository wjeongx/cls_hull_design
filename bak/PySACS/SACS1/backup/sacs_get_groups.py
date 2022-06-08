import wx
import string

def get_groups():
     GROUPS = []

     n_grp = 0

     while 1:
          read_dat_line = fr.readline()
          if not read_dat_line: break

          if read_dat_line.strip() == 'GRUP':
               while 1:
                    read_dat_line = fr.readline()
                    if read_dat_line[0:4] != 'GRUP': break

                    if (group_line in GROUPS) == 0:
                         GROUPS.append(group_line)
                         n_grp +=1
                         

fread = 'Bent Support-2_sac.inp'
fr = open(fread,'r')

get_groups()

