#!/usr/bin/python

from string import *
from sys import *

try:
    f = open(argv[1], 'r')

    txt_line = []
    for in_str in f:
        if in_str.strip() != '':
            txt_line.append(in_str)

    f.close

    f = open(argv[1], 'w')
    for out_str in txt_line:
        f.write(out_str)

    f.close
except IOError:
    print >> stderr, 'cant open file'
    
        


            
        
        
