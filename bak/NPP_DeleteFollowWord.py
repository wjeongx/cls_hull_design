#!/usr/bin/python

from string import *
from sys import *

try:
    del_word = raw_input("input word for delete")
    f = open(argv[1], 'r')

    txt_line = []
    for in_str in f:
        tmp = in_str.split(del_word)
        txt_line.append(tmp[0])

    f.close

    f = open(argv[1], 'w')
    for out_str in txt_line:
        f.write(out_str)

    f.close
except IOError:
    print >> stderr, 'cant open file'
    
        


            
        
        
