import string
import wx

def get_sacs_data(SACS_INPUT_FILE, DATA_TYPE):

     if DATA_TYPE == 'SECT':
          nCOL = 4
     elif DATA_TYPE == 'GRUP':
          nCOL = 4
     elif DATA_TYPE == 'MEMBER':
          nCOL = 6
     elif DATA_TYPE == 'JOINT':
          nCOL = 5

     fr = open(SACS_INPUT_FILE,'r')
     
     SACS = []
     n_dat = 0
     
     while 1:
          dat_line = fr.readline()
          if not dat_line: break

          if dat_line.strip() == DATA_TYPE:
               while 1:
                    dat_line = fr.readline()
                    if dat_line[0:nCOL] != DATA_TYPE: break

                    if(dat_line in SACS) == 0:
                         SACS.append(dat_line)

                    if DATA_TYPE == 'MEMBER':
                         if dat_line[6:7].strip() == '1':
                              dat_line = fr.readline()
                              SACS[n_dat] = SACS[n_dat]+ dat_line

                    n_dat += 1

     fr.close

     return n_dat-1, SACS

def get_sacs_joint(SACS_INPUT_FILE):

     JOINT = []

     n_jnt, JOINT = get_sacs_data(SACS_INPUT_FILE, 'JOINT')

     Joint = {}
     for JNT in JOINT:
          Joint[JNT[6:10].strip()] = [(float(JNT[11:18].strip().zfill(10))+float(JNT[32:39].strip().zfill(10))/100.),
                                      (float(JNT[18:25].strip().zfill(10))+float(JNT[39:46].strip().zfill(10))/100.),
                                      (float(JNT[25:32].strip().zfill(10))+float(JNT[46:53].strip().zfill(10))/100.),
                                       JNT[54:60],0,[]]
     return n_jnt, Joint

def sacs_get_joint_name(SACS_INPUT_FILE):

     JOINT = []

     n_jnt, JOINT = get_sacs_data(SACS_INPUT_FILE, 'JOINT')

     Joint = []
     for JNT in JOINT:
          Joint.append([JNT[6:10].strip(),0])
          
     return n_jnt, Joint
    
def get_sacs_member(SACS_INPUT_FILE):

     MEMBER = []

     n_mem, MEMBER = get_sacs_data(SACS_INPUT_FILE, 'MEMBER')

     Member = []
     for MEM in MEMBER:
          Member.append({'JA':MEM[7:11].strip(), 'JB':MEM[11:15].strip(), 'GRP':MEM[16:19].strip(), 'DLST':MEM})
          
     return n_mem, Member

def get_sacs_group(SACS_INPUT_FILE):

     GRUP = []

     n_grup, GRUP = get_sacs_data(SACS_INPUT_FILE, 'GRUP')

     Group = []
     for GRP in GRUP:
          Group.append({'NAME':GRP[5:9], 'SEC':GRP[9:15]})
          

     return n_grup, Group


def get_sacs_section(SACS_INPUT_FILE):

     SECT = []

     n_sect, SECT = get_sacs_data(SACS_INPUT_FILE, 'SECT')

     Section = []
     for SEC in SECT:
          Section.append({'NAME':SEC[6:11], 'TYP':SEC[11:15]})
          
     return n_sect, Section







