# Input_Operation.py

import string
import os
import wx

SECT = []
GRUP = []
MEMBER = []
MEMBER_OFFSET = []
PLATE = []
PLATE_OFFSET = []
JOINT = []
JOINT_PERSET = []
     
n_sect = 0
n_grup = 0
n_member = 0
n_plate = 0
n_joint = 0

def SACS_Input_CARD(SACS_INPUT_FILE):

     fr = open(SACS_INPUT_FILE,'r')
     
     SACS_INPUT = []
     
     while 1:
          input_line = fr.readline()
          if not input_line: break
                    
          SACS_INPUT.append(input_line.strip())
          
          if input_line[0:4] == 'SECT':
               SECT.append(input_line)
               n_sec += 1

          elif input_line[0:4] == 'GRUP':
               GRUP.append(input_line)
               n_grou += 1

          elif input_line[0:6] == 'MEMBER':

               if input_line.find('OFFSET') != -1:
                    MEMBER_OFFSET.append(input_line)
               else:
                    MEMBER.append(input_line)
                    n_member += 1
                    
          elif input_line[0:5] == 'PLATE':

               if input_line.find('OFFSET') != -1:
                    PLATE_OFFSET.append(input_line)
               else:
                    PLATE.append(input_line)
                    n_plate += 1
                    
          elif input_line[0:5] == 'JOINT':

               if input_line.find('PERSET') != -1:
                    JOINT_PERSET.append(input_line)
               else:
                    JOINT.append(input_line)
                    
     return SACS_INPUT, n_dat, TYPE_INPUT


def SACS_Input_Read(SACS_INPUT_FILE, DATA_TYPE):

     nCOL = len(DATA_TYPE)
     
     fr = open(SACS_INPUT_FILE,'r')
     
     SACS_FINPUT = []
     TYPE_INPUT = []
     n_dat = 0
     
     while 1:
          input_line = fr.readline()
          SACS_FINPUT.append(input_line.strip())
          if not input_line: break

          if input_line.strip() == DATA_TYPE:

               while 1:

                    input_line = fr.readline()
                    SACS_FINPUT.append(input_line)
                    
                    if input_line[0:nCOL] != DATA_TYPE: break

                    TYPE_INPUT.append(input_line.strip())

                    n_dat += 1

     fr.close

     return SACS_FINPUT, n_dat, TYPE_INPUT

def SACS_Input_Read_Member(SACS_INPUT_FILE):

     fr = open(SACS_INPUT_FILE,'r')
     
     SACS_INPUT = []
     MEMBER_INPUT = []
     n_member = 0
     
     while 1:
          input_line = fr.readline()
          SACS_INPUT.append(input_line.strip())
          if not input_line: break

          if input_line.strip() == 'MEMBER':

               while 1:
                    input_line = fr.readline()
                    SACS_INPUT.append(input_line)

                    if input_line[0:6] != 'MEMBER': break

                    MEMBER_INPUT.append([])
                    MEMBER_INPUT[n_member].append(input_line.strip())

                    if input_line[6] is '1' or input_line[6] is '2':
                        input_line = fr.readline()
                        MEMBER_INPUT[n_member].append(input_line.strip())

                    n_member += 1

     fr.close

     return SACS_INPUT, n_member, MEMBER_INPUT

def SACS_Input_Read_Plate(SACS_INPUT_FILE):

     fr = open(SACS_INPUT_FILE,'r')
     
     SACS_INPUT = []
     PLATE_INPUT = []
     n_plate = 0
     
     while 1:
          input_line = fr.readline()
          SACS_INPUT.append(input_line.strip())
          if not input_line: break

          if input_line.strip() == 'PLATE':

               while 1:
                    input_line = fr.readline()
                    SACS_INPUT.append(input_line)

                    if input_line[0:6] != 'PLATE': break

                    PLATE_INPUT.append([])
                    PLATE_INPUT[n_plate].append(input_line.strip())

                    if input_line[42] is '1' or input_line[42] is '2':
                        input_line = fr.readline()
                        PLATE_INPUT[n_plate].append(input_line.strip())

                    n_plate += 1

     fr.close

     return SACS_INPUT, n_plate, PLATE_INPUT

def Get_Joints(SACS_INPUT_FILE):

    FINPUT = []
    JOINT_INPUT = []

    SACS_INPUT, n_joint, JOINT_INPUT = SACS_Input_Read(SACS_INPUT_FILE, 'JOINT')

    JOINT_ID = []
    JOINT = {}
    JOINT_PERSET = {}
    
    for joint in JOINT_INPUT:
        joint = joint.ljust(72)
        JOINT_ID.append(joint[6:10])
        if joint.find('PERSET') == -1:
             JOINT[JOINT_ID[-1]] = {'JID':joint[6:10],
                                  'X':float(joint[11:18].strip().zfill(7)),
                                  'Y':float(joint[18:25].strip().zfill(7)),
                                  'Z':float(joint[25:32].strip().zfill(7)),
                                  'x':float(joint[32:39].strip().zfill(7)),
                                  'y':float(joint[39:46].strip().zfill(7)),
                                  'z':float(joint[46:53].strip().zfill(7)),
                                  'DX':joint[54],
                                  'DY':joint[55],
                                  'DZ':joint[56],
                                  'MX':joint[57],
                                  'MY':joint[58],
                                  'MZ':joint[59],
                                  'REMARK':joint[61:69]}
        else:
             JOINT_PERSET[JOINT_ID[-1]] = {'JID':joint[6:10],
                                           'DX':joint[11:18],
                                           'DY':joint[18:25],
                                           'DZ':joint[25:32],
                                           'MX':joint[32:39],
                                           'MY':joint[39:46],
                                           'MZ':joint[46:53],
                                           'PERSET':joint[54:60],
                                           'COMMENTS':joint[61:68],
                                           'LCNAME':joint[68:72]
                                           }
             
             
        
    return SACS_INPUT, n_joint, JOINT_ID, JOINT, JOINT_PERSET

def Get_Members(SACS_INPUT_FILE):

    FINPUT = []
    MEMBER_INPUT = []

    FINPUT, count, MEMBER_INPUT = SACS_Input_Read_Member(SACS_INPUT_FILE)

    Member_ID = []
    MEMBER = {}
    MEMBER_OFFSET = {}
    for member in MEMBER_INPUT:
        member[0] = member[0].ljust(80)
        Member_ID.append(member[0][7:15])
        MEMBER[Member_ID[-1]] = {'OFFSET':member[0][6],
                             'JA':member[0][7:11],
                             'JB':member[0][11:15],
                             'ADD_DATA':member[0][15],
                             'GROUP':member[0][16:19],
                             'SOUT':member[0][19:21],
                             'GAP_TYPE':member[0][21],
                             'JADX':member[0][22],
                             'JADY':member[0][23],
                             'JADZ':member[0][24],
                             'JAMX':member[0][25],
                             'JAMY':member[0][26],
                             'JAMZ':member[0][27],
                             'JBDX':member[0][28],
                             'JBDY':member[0][29],
                             'JBDZ':member[0][30],
                             'JBMX':member[0][31],
                             'JBMY':member[0][32],
                             'JBMZ':member[0][33],
                             'CHOANG':member[0][35:41],
                             'LOCZ_REF':member[0][41:45],
                             'FLD':member[0][45],
                             'KLO':member[0][46],
                             'AVG':member[0][47:51],
                             'KYLY':member[0][51:55],
                             'KZLZ':member[0][55:59],
                             'UL_SHR':member[0][59:64],
                             'DENS':member[0][64:70],
                             'STRESS':member[0][70:72],
                             'ED':member[0][72:78]}

        if MEMBER[Member_ID[-1]]['OFFSET'] is '1' or MEMBER[Member_ID[-1]]['OFFSET'] is '2':
               member[1] = member[1].ljust(71)
               MEMBER_OFFSET[Member_ID[-1]] = {'COMMENT':member[1][14:35],
                                           'JAX':member[1][35:41],
                                           'JAY':member[1][41:47],
                                           'JAZ':member[1][47:53],
                                           'JBX':member[1][53:59],
                                           'JBY':member[1][59:65],
                                           'JBZ':member[1][65:71]}
                                           
    return FINPUT, count, Member_ID, MEMBER, MEMBER_OFFSET

def JOINT_INPUT_LINE(JointId, Joint):

     Joint_Input = []
     for jid in JointId:
          tmp = "%5s %4s %7s%7s%7s %7s%7s%7s %c%c%c%c%c%c %8s" %('JOINT',
                                                                 Joint[jid]['JID'],
                                                                 Joint[jid]['X'],
                                                                 Joint[jid]['Y'],
                                                                 Joint[jid]['Z'],
                                                                 Joint[jid]['x'],
                                                                 Joint[jid]['y'],
                                                                 Joint[jid]['z'],
                                                                 Joint[jid]['DX'],
                                                                 Joint[jid]['DY'],
                                                                 Joint[jid]['DZ'],
                                                                 Joint[jid]['MX'],
                                                                 Joint[jid]['MY'],
                                                                 Joint[jid]['MZ'],
                                                                 Joint[jid]['REMARK'])
                                                                 
                                                                 
          Joint_Input.append(tmp)

     return Joint_Input

def MEMBER_INPUT_LINE(MemberId, Member):

     Member_Input = []
     for mid in MemberId:
          tmp = "%5s %4s %7s%7s%7s %7s%7s%7s %c%c%c%c%c%c %8s" %('JOINT',
                                                                 Member[jid]['JID'],
                                                                 Member[jid]['X'],
                                                                 Member[jid]['Y'],
                                                                 Member[jid]['Z'],
                                                                 Member[jid]['x'],
                                                                 Member[jid]['y'],
                                                                 Member[jid]['z'],
                                                                 Member[jid]['DX'],
                                                                 Member[jid]['DY'],
                                                                 Member[jid]['DZ'],
                                                                 Member[jid]['MX'],
                                                                 Member[jid]['MY'],
                                                                 Member[jid]['MZ'],
                                                                 Member[jid]['REMARK'])
                                                                 
                                                                 
          Member_Input.append(tmp)

     return Member_Input

def Remove_Free_Joint(fileR, fileW):

    FINPUT = []
    MEMBER_ID = []
    MEMBERS = {}
    MEMBERS_OFFSET = {}
    FINPUT, count, MEMBER_ID, MEMBERS, MEMBERS_OFFSET = Get_Members(fileR)
     
    JOINTS = {}
    JOINT_ID = []
    FINPUT, count_joint, JOINT_ID, JOINTS, JOINTS_PERSET = Get_Joints(fileR)

    for JID in JOINT_ID:
         CHK = 1
         for MID in MEMBER_ID:
              if JID == MEMBERS[MID]['JA'] or JID == MEMBERS[MID]['JB']:
                   CHK = CHK * 0
              else:
                   CHK = CHK * 1

         if CHK is 0:
              del JOINTS[JID]
              JOINT_ID.remove(JID)
              
    idx = FINPUT.index('JOINT') + 1
    Joint_Input = []
    Joint_Input = JOINT_INPUT_LINE(JOINT_ID, JOINTS)

    FINPUT[idx:idx+count_joint] = Joint_Input

    fw = open(fileW, 'w')
    
    for input_line in FINPUT:
         fw.write(input_line + '\n')

    fw.close()
         
#    for joint in JOINTS:
#         print joint[
         #chk = 1
         #for member in MEMBERS:
         #     print joint
              #if joint['JID'] is member['JA'] or joint['JID'] is member['JA']:
              #     chk = chk * 0
              #else:
              #     chk = chk * 1
         #print chk

# Remove_Free_Joint('inp_pump_pf_sac.inp', 'inp_pump_only10_sac.inp')

def Run_Joints():

     fileR = 'inp_pump_pf_sac.inp'

     SACS_INPUT = []
     JOINT_ID = []
     JOINT = []
     JOINT_PERSET = []
     
     SACS_INPUT, n_joint, JOINT_ID, JOINT, JOINT_PERSET = Get_Joints(fileR)

     for jid in JOINT_ID:
          print JOINT_PERSET[jid]
     
     
Run_Joints()     
'''
def test():

     tes={}
     tes['t1'] = { 'a1':1, 'b1':2}
     tes['t2'] = { 'a1':2, 'b1':4}
     tes['t3'] = { 'a1':100, 'b1':100}

     return tes

te = {}
te = test()
del te['t1']
print te
     #for t in te:
     #     print t[1]
'''














    
        

    

    
    
