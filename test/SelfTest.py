#!/usr/bin/env python

"Self Test"

def CheckReference(paraIn):
    print('CheckReference function begin: ' + str(paraIn))
    paraIn = paraIn + 101
    print('CheckReference function end: ' + str(paraIn))

def Test_CheckReference():
    numberIn = int(input('Give me a number to use: '))
    print('Your number in Test_CheckReference before using: ' + str(numberIn))
    CheckReference(numberIn)
    print('Your number in Test_CheckReference after using: ' + str(numberIn))

def Test_ReferenceCount():
    numberIn = int(input('Give me a number to use: '))
    x = numberIn
    print('Your number: ' + str(numberIn) + ' other number: ' + str(x))
    numberIn += x
    print('After numberIn += x, your number: ' + str(numberIn) + ' other number: ' + str(x))
    x += numberIn
    print('After x += numberIn, your number: ' + str(numberIn) + ' other number: ' + str(x))
    
if ('__main__' == __name__):
    #Test_CheckReference()
    Test_ReferenceCount()
