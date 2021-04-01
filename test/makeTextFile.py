#!/usr/bin/env python

'MakeTextFile.py -- create text file'

import os

ls = os.linesep

def MakeTextFile():
    while True:
        fname = input('Your file name: ')
        if (os.path.exists(fname)):
            print('Error: ' + fname + ' already exists')
        else :
            break

    all = []
    print('Enter lines (\'.\' by itself to quit).')

    while True:
        entry = input()
        if (entry == '.'):
            break
        else :
            all.append(entry)

    fobj = open(fname, 'w')
    fobj.writelines(['%s%s' % (x, ls) for x in all])
    fobj.close()
    print('Done')

if ('__main__' == __name__):
    #print(ls)
    #print('%s %s' % (1, 'abc'))
    MakeTextFile()
