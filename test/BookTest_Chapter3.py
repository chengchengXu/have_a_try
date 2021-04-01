#!/usr/bin/env python

"Core Python Programming Chapter3 Test"

import makeTextFile
import readTextFile

def Test3_6():
    x,y,z=1,2,3
    print(x)
    print(y)
    print(z)
    z,x,y=y,z,x
    print(x)
    print(y)
    print(z)

def Test3_12():
    while True:
        cmdIn = input('Your operation: ')
        if cmdIn == 'x' or cmdIn == 'X':
            break
        elif cmdIn == '1':
            makeTextFile.MakeTextFile()
        elif cmdIn == '2':
            readTextFile.ReadTextFile()
        else:
            print('Error operation')

if '__main__' == __name__:
    Test3_12()
