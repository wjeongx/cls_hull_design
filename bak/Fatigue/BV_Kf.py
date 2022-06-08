from math import *
ramda1 = [1.85,1.85,2.10,3.95,1.60,1.90,3.95,1.85,2.05]
ramda2 = [2.10, 2.10, 2.40,4.50,1.80,2.15,4.5,2.10,2.35]

for x in ramda2:
    kf = x * sqrt(45./30.)
    print x, kf, kf/1.43
    