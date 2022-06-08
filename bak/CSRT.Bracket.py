import math
print 'Bracket Design for CSR.Tanker'

print 'fbkt = 0.2 for brackets with flange or edge stiffener'
print '       0.3 for brackets without flange or edge stiffener'
fbkt = input('fbkt = ')
print
print 'syd-stf = specified minimum yield stress of the material of the stiffener, in N/mm2'
syd_stf = input('syd-stf = ')
print
print 'syd-bkt = specified minimum yield stress of the material of the bracket, in N/mm2'
syd_bkt = input('syd-bkt = ')
print
print 'Zrl-net = net rule section modulus, for the stiffener, in cm3. In the case of two'
print '          stiffeners connected, it need not be taken as greater than that of the'
print '          smallest connected stiffener'
Zrl = input('Zrl-net = ')
print 

tbkt_net = (2+fbkt * math.sqrt(Zrl)*(math.sqrt(syd_stf/syd_bkt)))

print tbkt_net

input()