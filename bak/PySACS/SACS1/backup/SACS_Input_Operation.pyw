# Input_Operation.py

import string
import os
import wx

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
               JointId.remove(jid)               

     return Joint_Input

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

def MEMBER_INPUT_LINE(MEMBER_ID, MEMBER, MEMBER_OFFSET):

     Member_Input = []

     for mid in MEMBER_ID:
          tmp = "%6s%c%4s%4s%c%3s%2s%c%c%c%c%c%c%c%c%c%c%c%c%c %6s%4s%c%c%4s%4s%4s%5s%6s%2s%5s" %('MEMBER',
                                                                 MEMBER[mid]['OFFSET'],
                                                                 MEMBER[mid]['JA'],
                                                                 MEMBER[mid]['JB'],
                                                                 MEMBER[mid]['ADD_DATA'],
                                                                 MEMBER[mid]['GROUP'],
                                                                 MEMBER[mid]['SOUT'],
                                                                 MEMBER[mid]['GAP_TYPE'],
                                                                 MEMBER[mid]['JADX'],
                                                                 MEMBER[mid]['JADY'],
                                                                 MEMBER[mid]['JADZ'],
                                                                 MEMBER[mid]['JAMX'],
                                                                 MEMBER[mid]['JAMY'],
                                                                 MEMBER[mid]['JAMZ'],
                                                                 MEMBER[mid]['JBDX'],
                                                                 MEMBER[mid]['JBDY'],
                                                                 MEMBER[mid]['JBDZ'],
                                                                 MEMBER[mid]['JBMX'],
                                                                 MEMBER[mid]['JBMY'],
                                                                 MEMBER[mid]['JBMZ'],
                                                                 MEMBER[mid]['CHOANG'],
                                                                 MEMBER[mid]['LOCZ_REF'],
                                                                 MEMBER[mid]['FLD'],
                                                                 MEMBER[mid]['KLO'],
                                                                 MEMBER[mid]['AVG'],
                                                                 MEMBER[mid]['KYLY'],
                                                                 MEMBER[mid]['KZLZ'],
                                                                 MEMBER[mid]['UL_SHR'],
                                                                 MEMBER[mid]['DENS'],
                                                                 MEMBER[mid]['STRESS'],
                                                                 MEMBER[mid]['ED'])
                                                                 
          Member_Input.append(tmp)
          if MEMBER[mid]['OFFSET'] == '1' or MEMBER[mid]['OFFSET'] == '2':
               tmp = "%6s %7s %21s%6s%6s%6s%6s%6s%6s" %('MEMBER',
                                                        'OFFSETS',
                                                        MEMBER_OFFSET[mid]['COMMENT'],
                                                        MEMBER_OFFSET[mid]['JAX'],
                                                        MEMBER_OFFSET[mid]['JAY'],
                                                        MEMBER_OFFSET[mid]['JAZ'],
                                                        MEMBER_OFFSET[mid]['JBX'],
                                                        MEMBER_OFFSET[mid]['JBY'],
                                                        MEMBER_OFFSET[mid]['JBZ'])

               Member_Input.append(tmp)
          

     return Member_Input

def Get_Plates(SACS_INPUT_FILE):

    SACS_INPUT, n_plate, PLATE_INPUT = SACS_Input_Read(SACS_INPUT_FILE, 'PLATE')

    PLATE_ID = []
    PLATE = {}
    PLATE_OFFSET = {}
    OSN = {}
    for plate in PLATE_INPUT:
        plate = plate.ljust(81)
        if plate.find('OFFSET') == -1:
             PLATE_ID.append(plate[6:10])
             PLATE[PLATE_ID[-1]] = {'PID':plate[6:10],
                                    'JA':plate[11:15],
                                    'JB':plate[15:19],
                                    'JC':plate[19:23],
                                    'JD':plate[23:27],
                                    'GRUP':plate[27:30],
                                    'RPSK':plate[30:32],
                                    'THK':plate[32:38],
                                    'OFFSET':plate[42],
                                    'ELA':plate[47:54],
                                    'POSSON':plate[54:59],
                                    'YIELD':plate[59:64],
                                    'DENSITY':plate[69:74],
                                    'REMARK':plate[74:80]}

             PLATE[PLATE_ID[-1]]
             PLATE_OFFSET[PLATE_ID[-1]] = {}
             OSN[PLATE_ID[-1]] = []
             SN = 0 
        else:
             SN += 1
             OSN[PLATE_ID[-1]].append(SN)
             PLATE_OFFSET[PLATE_ID[-1]][SN] = {'PID':PLATE_ID[-1],
                                                'REMARK':plate[14:35],
                                                'OFF1X':plate[35:41],
                                                'OFF1Y':plate[41:47],
                                                'OFF1Z':plate[47:53],
                                                'OFF2X':plate[53:59],
                                                'OFF2Y':plate[59:65],
                                                'OFF2Z':plate[65:71] }
             
    return SACS_INPUT, n_plate, PLATE_ID, PLATE, OSN, PLATE_OFFSET


def PLATE_INPUT_LINE(PLT_ID, PLATE, OSN, PLATE_OFFSET):

     Plate_Input = []
     for pid in PLT_ID:
          tmp = "%5s %4s %4s%4s%4s%4s%3s%2s%6s%4s%c%4s%7s%5s%5s%5s%5s%6s" %('PLATE',
                                                                            PLATE[pid]['PID'],
                                                                            PLATE[pid]['JA'],
                                                                            PLATE[pid]['JB'],
                                                                            PLATE[pid]['JC'],
                                                                            PLATE[pid]['JD'],
                                                                            PLATE[pid]['GRUP'],
                                                                            PLATE[pid]['RPSK'],
                                                                            PLATE[pid]['THK'],
                                                                            ' ',
                                                                            PLATE[pid]['OFFSET'],
                                                                            ' ',
                                                                            PLATE[pid]['ELA'],
                                                                            PLATE[pid]['POSSON'],
                                                                            PLATE[pid]['YIELD'],
                                                                            ' ',
                                                                            PLATE[pid]['DENSITY'],
                                                                            PLATE[pid]['REMARK'])
                                                                 
          Plate_Input.append(tmp)
          
          if PLATE[pid]['OFFSET'] == '1' or PLATE[pid]['OFFSET'] == '2':
               for sn in OSN[pid]:
                    tmp = "%5s  %7s%21s%6s%6s%6s%6s%6s%6s" % ('PLATE',
                                                              'OFFSETS',
                                                              PLATE_OFFSET[pid][sn]['REMARK'],
                                                              PLATE_OFFSET[pid][sn]['OFF1X'],
                                                              PLATE_OFFSET[pid][sn]['OFF1Y'],
                                                              PLATE_OFFSET[pid][sn]['OFF1Z'],
                                                              PLATE_OFFSET[pid][sn]['OFF2X'],
                                                              PLATE_OFFSET[pid][sn]['OFF2Y'],
                                                              PLATE_OFFSET[pid][sn]['OFF2Z'])
                         
                    Plate_Input.append(tmp)
                              

     return Plate_Input


def SACS_Model_Subtract(fileA, fileB, fileC):
    
     # SACS_INPUT : List
     # n_member : Integer
     # Member_ID : List
     # MEMBER : Dictionary
     # MEMBER_OFFSET : Dictionary
     
     SACS_INPUT_A, n_memberA, Member_ID_A, MEMBER_A, MEMBER_OFFSET_A = Get_Members(fileA)

     SACS_INPUT_B, n_memberB, Member_ID_B, MEMBER_B, MEMBER_OFFSET_B = Get_Members(fileB)
     
     for mid in Member_ID_B:
        try:
             if MEMBER_A[mid]['OFFSET'] is '1' or MEMBER_A[mid]['OFFSET'] is '2':
                  del MEMBER_OFFSET_A[mid]

             del MEMBER_A[mid]
             Member_ID_A.remove(mid)
           
        except ValueError, Error:
            print Error

     idx = SACS_INPUT_A.index('MEMBER') + 1

     SACS_INPUT_MEMBER = MEMBER_INPUT_LINE(Member_ID_A, MEMBER_A, MEMBER_OFFSET_A)

     SACS_INPUT_A[idx:idx+n_memberA] = SACS_INPUT_MEMBER

     SACS_INPUT_C, n_plate_c, PLT_IDC, PLATE_C, OSNC, PLATE_OFFSET_C = Get_Plates(fileA)

     SACS_INPUT_D, n_plate_d, PLT_IDD, PLATE_D, OSND, PLATE_OFFSET_D = Get_Plates(fileB)

     for pid in PLT_IDD:
          try:
               PLT_IDC.remove(pid)
               del OSNC[pid]
               del PLATE_C[pid]
               del PLATE_OFFSET_C[pid]

          except ValueError, Error:
               print Error

     plate_input = PLATE_INPUT_LINE(PLT_IDC, PLATE_C, OSNC, PLATE_OFFSET_C)
     idx = SACS_INPUT_A.index('PLATE') + 1
     print idx
     SACS_INPUT_A[idx:idx+n_plate_c] = plate_input    
    
     fw = open(fileC, 'w')

     for input_line in SACS_INPUT_A:
          fw.write(input_line + '\n')

     fw.close

#    Remove_Free_Joint(fileC, fileC)
    
#    CompleteMessage('Subtract Complete')
#     wx.MessageBox("Subtract Complete", "Information")

def Remove_Load_NonExitedMember(fileR, fileW):
    
    fr = open(fileR,'r')

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

    fr = open(fileR,'r')
    fw = open(fileW, 'w')
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

def Remove_Member_with_OneJoint(fileR, fileW):

    MEMBERS = []
    FINPUT = []

    FINPUT, count, MEMBERS = SACS_Input_Read(fileR, 'MEMBER')

    for member in MEMBERS:
        if member[7:11] == member[11:15]:
            MEMBERS.remove(member)
    
    idx = FINPUT.index('MEMBER') + 1

    FINPUT[idx:idx] = MEMBERS
    
    fw = open(fileW, 'w')

    for input_line in FINPUT:
        fw.write(input_line + '\n')

    fw.close

def Remove_DuplicatedMembers(fileR, fileW):

    MEMBERS = []
    FINPUT = []

    FINPUT, count, MEMBERS = SACS_Input_Read(fileR, 'MEMBER')

    for member in MEMBERS:
        for check_member in MEMBERS:
            if member[7:15] == check_member[7:15]:
                MEMBERS.remove(check_member)
    
    idx = FINPUT.index('MEMBER') + 1

    FINPUT[idx:idx] = MEMBERS
    
    fw = open(fileW, 'w')

    for input_line in FINPUT:
        fw.write(input_line + '\n')

    fw.close
    
def Remove_Free_Joint(fileR, fileW):

     SACS_INPUT, n_member, MEMBER_ID, MEMBERS, MEMBERS_OFFSET = Get_Members(fileR)
     
     SACS_INPUT, n_joint, JOINT_ID, JOINT, PER_ID, JOINT_PERSET = Get_Joints(fileR)

     RJID = []
     for JID in JOINT_ID:
          CHK = 1
          for MID in MEMBER_ID:
               if JID.strip() == MEMBERS[MID]['JA'].strip() or JID.strip() == MEMBERS[MID]['JB'].strip():
                    CHK = CHK * 0
               else:
                    CHK = CHK * 1

          if CHK == 1:
               RJID.append(JID)

     before_id = 0
     for rid in RJID:

          JOINT_ID.remove(rid)

          if before_id != rid:
               del JOINT[rid]
               del PER_ID[rid]
               del JOINT_PERSET[rid]
               
          before_id = rid
          

     idx = SACS_INPUT.index('JOINT') + 1

     Joint_Input = JOINT_INPUT_LINE(JOINT_ID, JOINT, PER_ID, JOINT_PERSET)

     SACS_INPUT[idx:idx+n_joint] = Joint_Input

     fw = open(fileW, 'w')

     for input_line in SACS_INPUT:
          fw.write(input_line + '\n')

     fw.close()

def Matching_Local_Coordinate(fileR, fileW):

    MEMBERS = []
    JOINTS = []
    JOINTS_NAME = []

    count_member, MEMBERS = SACS_Input.Get_Members(fileR)
    count_joint, JOINTS = SACS_Input.Get_Joints(fileR)
    count_joint_name, JOINTS_NAME = SACS_Input.Get_Joints_Name(fileR)

    fw = open(fileW,'w')

    fw.write('MEMBER\n')

    idx = 0

    for MEMB in MEMBERS:
         if MEMB['GRP'] == 'ANG':
              JOINTS[MEMB['JA']][4] = JOINTS[MEMB['JA']][4] + 1
              JOINTS[MEMB['JA']][5].append([idx,MEMB['GRP'],MEMB['JB']])

              JOINTS[MEMB['JB']][4] = JOINTS[MEMB['JB']][4] + 1
              JOINTS[MEMB['JB']][5].append([idx, MEMB['GRP'],MEMB['JA']])

         idx +=1

    for JNT in JOINTS:
         if JOINT[JNT[0]][4] == 4:
              for i in range(0,4):
                   MMEMB = JNT[0]+ JOINT[JNT[0]][5][i][2]

                   MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'] = MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'][:7] + MMEMB + MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'][15:]

    #               fw.write(MEMBER[JOINT[JNT[0]][5][i][0]]['DLST'])

    for MEMB in MEMBER:
         fw.write(MEMB['DLST'])

    fw.close

    print "Process Complete"


def matching_local_coordinate2(fileR, fileW):

    n_member, MEMBER = get_sacs_member(fread)
    n_joint, JOINT = get_sacs_joint(fread)

    file_name = os.path.split(fread)
    file_name = os.path.splitext(file_name[1])

    fwrite = file_name[0] + '.members'

    fw = open(fwrite,'w')

    fw.write('MEMBER\n')

    for memb in MEMBER:
         ja = [JOINT[memb['JA']][0], JOINT[memb['JA']][1], JOINT[memb['JA']][2]]

         jb = [JOINT[memb['JB']][0], JOINT[memb['JB']][1], JOINT[memb['JB']][2]]

         dif = [abs(ja[0]-jb[0]), abs(ja[1]-jb[1]), abs(ja[2]-jb[2])]

         if dif[0] == max(dif):
              if ja[0] <= jb[0]:
                   mmemb = memb['JA'] + memb['JB']
              else:
                   mmemb = memb['JB'] + memb['JA']
         elif dif[1] == max(dif):
              if ja[1] <= jb[1]:
                   mmemb = memb['JA'] + memb['JB']
              else:
                   mmemb = memb['JB'] + memb['JA']
         elif dif[2]== max(dif):
              if ja[2] <= jb[2]:
                   mmemb = memb['JA'] + memb['JB']
              else:
                   mmemb = memb['JB'] + memb['JA']

         fw.write(memb['DLST'][:7] + mmemb+ memb['DLST'][15:])

    fw.close

    print "Process Complete"

def Run_Joints():

     fileR = 'inp_pump_pf_sac.inp'

     #SACS_INPUT = []
     #JOINT_ID = []
     #JOINT = []
     #LC_ID = {}
     #JOINT_PERSET = []
     
     SACS_INPUT, n_joint, JOINT_ID, JOINT, LC_ID, JOINT_PERSET = Get_Joints(fileR)

     SACS_INPUT_JOINT = JOINT_INPUT_LINE(JOINT_ID, JOINT, LC_ID, JOINT_PERSET)

     for input_line in SACS_INPUT_JOINT:
          print input_line
     
def Run_Members():
     
     fileR = 'inp_c8_LEV_PF_RA_sac.inp'

     #SACS_INPUT = []
     #MEMBER_ID = []
     #MEMBERS = {}
     #MEMBERS_OFFSET = {}

     SACS_INPUT, n_member, MEMBER_ID, MEMBERS, MEMBERS_OFFSET = Get_Members(fileR)

     SACS_INPUT_MEMBER = MEMBER_INPUT_LINE(MEMBER_ID, MEMBERS, MEMBERS_OFFSET)

     for input_line in SACS_INPUT_MEMBER:
          print input_line

def Run_Plates():
     
     fileR = 'inp_c8_LEV_PF_RA_sac.inp'

     #SACS_INPUT = []
     #PLT_ID = []
     #PLATES = {}
     #PLATES_OFFSET = {}

     SACS_INPUT, n_plate, PLT_ID, PLATES, OSN, PLATES_OFFSET = Get_Plates(fileR)

     SACS_INPUT_PLATE = PLATE_INPUT_LINE(PLT_ID, PLATES, OSN, PLATES_OFFSET)

     for input_line in SACS_INPUT_PLATE:
          print input_line

def Run_Subtract():

     fileA = 'inp_c8_LEV_PF_RA_sac.inp'
     fileB = 'inp_remove_LEV_sac.inp'
     fileC = 'inp_Only_LEV_sac.inp'
     
     SACS_Model_Subtract(fileA, fileB, fileC)

     
          
#Run_Joints()
#Run_Members()
#Run_Plates()

Run_Subtract()

fileR = 'inp_Only_LEV_sac.inp'
fileW = 'inp_remove_joint_sac.inp'

Remove_Free_Joint(fileR,fileW)











    
        

    

    
    
