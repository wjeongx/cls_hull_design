import math

"""
E12 = (((D6*E8)-(D4*E4))-(D7*E11))/(E10-E11)
G12 = ((D6*G8)-(D4*G4)-(D7*G11))/(G10-G11)

if E15 == E10 and G15 == G10:
    ValU = min(E12,G12)
elif E15 == E11 and G15==G11:
    ValU = -max(E12,G12)+D7
elif E12>G12 and E15==E10 and G15!=G10:
    ValU = max(E12,G12)-min(E12,G12)
elif G12>E12 and E15!=E10 and G15 = G10:
    ValU= max(E12,G12)-min(E12,G12)
else:
    ValU = 0
    

if X == SHFTX and Y == SHFTY:
    ValU = min(E12,G12)
elif E15 == E11 and G15==G11:
    ValU = -max(E12,G12)+D7
elif E12>G12 and E15==E10 and G15!=G10:
    ValU = max(E12,G12)-min(E12,G12)
elif G12>E12 and E15!=E10 and G15 = G10:
    ValU= max(E12,G12)-min(E12,G12)
else:
    ValU = 0
"""
# Applied Load
AL = 1000.

#Based Weight
BWT = 2264614000/1000.

#Based COG
BCG = [0.060618,0.46908,26.44851]

#Target Weight
TWT = 229678.*9.807

#Target COG
TCG = [-0.275068284,-1.502977082]

#Extra Weight
EWT = TWT-BWT
# LOAD DATA
    # LOAD BLOCK

LBLK = ['C10U', 'C20U', 'C30U', 'C40U']

LPC =[[42.871, 41.239, 0.],[42.871, -41.249, 0.],[-42.197, 41.239, 0.],[-42.197, -41.249, 0.]]

LP = {}

LP['C10U'] = [0,0,0,0,0]
LP['C20U'] = [0,0,0,0,0]
LP['C30U'] = [0,0,0,0,0]
LP['C40U'] = [0,0,0,0,0]

#Shift COG
SCG = [0.,0.,0.]
if TCG[0] < BCG[0]:
    SCG[0] = min(LPC[0][0],LPC[1][0],LPC[2][0],LPC[3][0])
else:
    SCG[0] = max(LPC[0][0],LPC[1][0],LPC[2][0],LPC[3][0])

if TCG[1] < BCG[1]:
    SCG[1] = min(LPC[0][1],LPC[1][1],LPC[2][1],LPC[3][1])
else:
    SCG[1] = max(LPC[0][1],LPC[1][1],LPC[2][1],LPC[3][1])

#Other Coordinate
OCG = [0.,0.,0.]
if TCG[0] > BCG[0]:
    OCG[0] = min(LPC[0][0],LPC[1][0],LPC[2][0],LPC[3][0])
else:
    OCG[0] = max(LPC[0][0],LPC[1][0],LPC[2][0],LPC[3][0])

if TCG[1] > BCG[1]:
    OCG[1] = min(LPC[0][1],LPC[1][1],LPC[2][1],LPC[3][1])
else:
    OCG[1] = max(LPC[0][1],LPC[1][1],LPC[2][1],LPC[3][1])
    
#Required Weight
RWT = [0,0]
RWT[0] = (((TWT*TCG[0])-(BWT*BCG[0]))-(EWT*OCG[0]))/(SCG[0]-OCG[0])
RWT[1] = (((TWT*TCG[1])-(BWT*BCG[1]))-(EWT*OCG[1]))/(SCG[0]-OCG[1])

LWT = [0,0,0,0]
LPF = [0,0,0,0]

for idx in range(0,4):
    if LPC[idx][0] == SCG[0] and LPC[idx][1] == SCG[1]:
        LWT[idx] = min(RWT)
    elif LPC[idx][0] == OCG[0] and LPC[idx][1]==OCG[1]:
        LWT[idx] = -max(RWT)+EWT
    elif RWT[0]>RWT[1] and LPC[idx][0]==SCG[0] and LPC[idx][1]!=SCG[1]:
        LWT[idx] = max(RWT)-min(RWT)
    elif RWT[0]<RWT[1] and LPC[idx][0]!=SCG[0] and LPC[idx][1] == SCG[1]:
        LWT[idx]= max(RWT)-min(RWT)
    else:
        LWT[idx] = 0

    LPF[idx] = LWT[idx] / AL

print 'LWT :',LWT,'\n'
print 'LPF :',LPF

"""
if E15 == E10 and G15 == G10:
    ValU = min(E12,G12)
elif E15 == E11 and G15==G11:
    ValU = -max(E12,G12)+D7
elif E12>G12 and E15==E10 and G15!=G10:
    ValU = max(E12,G12)-min(E12,G12)
elif G12>E12 and E15!=E10 and G15 = G10:
    ValU= max(E12,G12)-min(E12,G12)
else:
    ValU = 0
"""




    
