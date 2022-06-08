# Input_Operation.py

import string
import os
import wx
import SACS_Input

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

def SACS_Input_Read_Joint(SACS_INPUT_FILE):

     fr = open(SACS_INPUT_FILE,'r')
     
     SACS_INPUT = []
     JOINT_INPUT = []
     n_joint = 0
     
     while 1:
          input_line = fr.readline()
          if not input_line: break
          SACS_INPUT.append(input_line.strip())

          if input_line.strip() == 'JOINT':

               while 1:

                    input_line = fr.readline()
                    SACS_INPUT.append(input_line)
                    
                    if input_line[0:5] == 'JOINT':
                         if input_line.find('PERSET') == -1:
                              JOINT_INPUT.append(input_line.strip())
                         else:
                              JOINT_INPUT.append(input_line.strip())

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
    LCN = {}
    for joint in JOINT_INPUT:
        joint = joint.ljust(75)
        JOINT_ID.append(joint[6:10])
        LC = joint[68:72]
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
             JOINT_PERSET[JOINT_ID[-1]] = {}
             LCN[JOINT_ID[-1]] = []
        else:
             LCN[JOINT_ID[-1]].append(joint[68:72])
             JOINT_PERSET[JOINT_ID[-1]][LC] = {'JID':joint[6:10],
                                           'DX':joint[11:18],
                                           'DY':joint[18:25],
                                           'DZ':joint[25:32],
                                           'MX':joint[32:39],
                                           'MY':joint[39:46],
                                           'MZ':joint[46:53],
                                           'PERSET':joint[54:60],
                                           'COMMENTS':joint[61:68],
                                           'LCNAME':joint[68:72]}
             
             
    return SACS_INPUT, n_joint, JOINT_ID, JOINT, LCN, JOINT_PERSET

'''
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
'''
def JOINT_INPUT_LINE(JointId, JOINT, PERSET_ID, JOINT_PERSET):

     Joint_Input = []
     for jid in JointId:
          tmp = "%5s %4s %7s%7s%7s %7s%7s%7s %c%c%c%c%c%c %8s" %('JOINT',
                                                                 JOINT[jid]['JID'],
                                                                 JOINT[jid]['X'],
                                                                 JOINT[jid]['Y'],
                                                                 JOINT[jid]['Z'],
                                                                 JOINT[jid]['x'],
                                                                 JOINT[jid]['y'],
                                                                 JOINT[jid]['z'],
                                                                 JOINT[jid]['DX'],
                                                                 JOINT[jid]['DY'],
                                                                 JOINT[jid]['DZ'],
                                                                 JOINT[jid]['MX'],
                                                                 JOINT[jid]['MY'],
                                                                 JOINT[jid]['MZ'],
                                                                 JOINT[jid]['REMARK'])
                                                                 
                                                                 
          Joint_Input.append(tmp)

          for PID in PERSET_ID[jid]:
               tmp = "%5s %4s %7s%7s%7s %7s%7s%7s %6s %6s%4s" %('JOINT',
                                                                 JOINT_PERSET[jid][PID]['JID'],
                                                                 JOINT_PERSET[jid][PID]['DX'],
                                                                 JOINT_PERSET[jid][PID]['DY'],
                                                                 JOINT_PERSET[jid][PID]['DZ'],
                                                                 JOINT_PERSET[jid][PID]['MX'],
                                                                 JOINT_PERSET[jid][PID]['MY'],
                                                                 JOINT_PERSET[jid][PID]['MZ'],
                                                                 JOINT_PERSET[jid][PID]['PERSET'],   
                                                                 JOINT_PERSET[jid][PID]['COMMENTS'],
                                                                 JOINT_PERSET[jid][PID]['LCNAME'])
               Joint_Input.append(tmp)
                              

     return Joint_Input


def Input_Subtract(fileA, fileB, fileC):
    
    SACS_INPUT_A = []
    MEMBER_A = []
    SACS_INPUT_A, countA, MEMBER_A = Get_Members(fileA):

    SACS_INPUT_B = []
    MEMBER_B = []
    SACS_INPUT_B, countB, MEMBER_B = Get_Members(fileA):

    for member in MEMBER_B:
        try:
            MEMBER_A.remove(member)
        except ValueError, Error:
            print Error

    idx = SACS_INPUT_A.index('MEMBER') + 1

    SACS_INPUT_A[idx:idx+countA+1] = MEMBER_A

    SACS_INPUT_C = []
    PLATE_C = []
    SACS_INPUT_C, countC, PLATE_C = SACS_Input_Read(fileA, 'PLATE')

    SACS_INPUT_B = []
    PLATE_B = []
    SACS_INPUT_B, countB, PLATE_B = SACS_Input_Read(fileB, 'PLATE')

    for plate in PLATE_B:
        try:
            PLATE_C.remove(plate)
        except ValueError, Error:
            print Error

    if len(PLATE_C) == 0:
        idx = SACS_INPUT_A.index('PLATE')
        SACS_INPUT_A[idx:idx+countC+2] = PLATE_C        
    else:
        idx = SACS_INPUT_A.index('PLATE') + 1
        SACS_INPUT_A[idx:idx+countC+1] = PLATE_C        
    
    fw = open(fileC, 'w')

    for input_line in SACS_INPUT_A:
        fw.write(input_line + '\n')

    fw.close

    Remove_Free_Joint(fileC, fileC)
    
#    CompleteMessage('Subtract Complete')
    wx.MessageBox("Subtract Complete", "Information")

    

def MEMBER_INPUT_LINE(MemberId, Member):

     Member_Input = []
     for mid in MemberId:
          tmp = "%5s %4s %7s%7s%7s %7s%7s%7s %c%c%c%c%c%c %8s" %('MEMBER',
                                                                 Member[jid]['OFFSET'],
                                                                 Member[jid]['JA'],
                                                                 Member[jid]['JB'],
                                                                 Member[jid]['ADD_DATA'],
                                                                 Member[jid]['GROUP'],
                                                                 Member[jid]['SOUT'],
                                                                 Member[jid]['GAP_TYPE'],
                                                                 Member[jid]['JADX'],
                                                                 Member[jid]['JADY'],
                                                                 Member[jid]['JADZ'],
                                                                 Member[jid]['JAMX'],
                                                                 Member[jid]['JAMY'],
                                                                 Member[jid]['JAMZ'],
                                                                 Member[jid]['JBDX'],
                                                                 Member[jid]['JBDY'],
                                                                 Member[jid]['JBDZ'],
                                                                 Member[jid]['JBMX'],
                                                                 Member[jid]['JBMY'],
                                                                 Member[jid]['JBMZ'],                                                                 
                                                                 Member[jid]['LOCZ_REF'],
                                                                 Member[jid]['FLD'],
                                                                 Member[jid]['KLO'],
                                                                 Member[jid]['AVG'],
                                                                 Member[jid]['KYLY'],
                                                                 Member[jid]['KZLZ'],
                                                                 Member[jid]['UL_SHR'],
                                                                 Member[jid]['DENS'],
                                                                 Member[jid]['STRESS'],
                                                                 Member[jid]['ED'])
                                                                 
          Member_Input.append(tmp)

     return Member_Input

def Remove_Free_Joint(fileR, fileW):

    SACS_INPUT = []
    MEMBER_ID = []
    MEMBERS = {}
    MEMBERS_OFFSET = {}

    SACS_INPUT, n_member, MEMBER_ID, MEMBERS, MEMBERS_OFFSET = Get_Members(fileR)
     
    SACS_INPUT = []
    JOINT_ID = []
    JOINT = []
    LC_ID = {}
    JOINT_PERSET = []
     
    SACS_INPUT, n_joint, JOINT_ID, JOINT, LC_ID, JOINT_PERSET = Get_Joints(fileR)

    for JID in JOINT_ID:
         CHK = 1
         for MID in MEMBER_ID:
              if JID == MEMBERS[MID]['JA'] or JID == MEMBERS[MID]['JB']:
                   CHK = CHK * 0
              else:
                   CHK = CHK * 1

         if CHK is 0:
              del JOINT[JID]
              del JOINT_PERSET[JID]
              JOINT_ID.remove(JID)
              
    idx = SACS_INPUT.index('JOINT') + 1
    
    Joint_Input = []
    Joint_Input = JOINT_INPUT_LINE(JOINT_ID, JOINTS)

    SACS_INPUT[idx:idx+count_joint] = Joint_Input

    fw = open(fileW, 'w')
    
    for input_line in SACS_INPUT:
         fw.write(input_line + '\n')

    fw.close()
         
def Run_Joints():

     fileR = 'inp_pump_only_sac.inp'

     SACS_INPUT = []
     JOINT_ID = []
     JOINT = []
     LC_ID = {}
     JOINT_PERSET = []
     
     SACS_INPUT, n_joint, JOINT_ID, JOINT, LC_ID, JOINT_PERSET = Get_Joints(fileR)

     SACS_INPUT_JOINT = JOINT_INPUT_LINE(JOINT_ID, JOINT, LC_ID, JOINT_PERSET)

     for input_line in SACS_INPUT_JOINT:
          print input_line
     
def Run_Members():
     
     fileR = 'inp_pump_only_sac.inp'

     SACS_INPUT = []
     JOINT_ID = []
     JOINT = []
     LC_ID = {}
     JOINT_PERSET = []




     
Run_Joints()     


# Remove_Free_Joint('inp_pump_only_sac.inp', 'inp_pump_only100_sac.inp')











    
        

    

    
    
