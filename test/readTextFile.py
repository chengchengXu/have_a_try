#!/usr/bin/env python

'readTextFile.py -- read and display text file'

import os

def ReadTextFile():
    while True:
        fname = input('Enter file name: ')
        if (os.path.exists(fname)):
            break
        else :
            print('Error: ' + fname + ' not exists')

    try:
        fobj = open(fname, 'r')
    except IOError as e:
        print('File open error: ' + e)
    else:
        for eachLine in fobj:
            print(eachLine, end = '')
        fobj.close()

if '__main__' == __name__:
    ReadTextFile()
