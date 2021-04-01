#!/usr/bin/env python

"Core Python Programming Chapter2 Test"

import random

def Test2_2():
    print(1 + 2 * 4)

def Test2_3():
    a = int(input('A:'))
    b = int(input('B:'))


    print('a:' + str(a) + ' b:' + str(b))
    print('a ** b: ' + str(a ** b))

    a = a * 1.5 + b / 3 - 3000 % a - 0.7 * b
    b = 1 / b

    print('a\':' + str(a) + ' b\':' + str(b))
    print('a\' ** b\': ' + str(a ** b))

def Test2_5():
    for test in range(11):
        print(test)

def Test2_6():
    number = int(input('Your number: '))
    if (number > 0):
        print('+')
    elif (number < 0):
        print('-')
    else:
        print('zero')

def Test2_7():
    inStr = input('Your string: ')
    for ch in inStr:
        print(ch)

def Test2_8():
    inStr = input('Your string: ')
    aType = inStr.split(',')
    print(aType)
    for a in aType:
        print(a)

def Test2_9():
    aTuple = (random.uniform(0, 1000), random.uniform(0, 1000), random.uniform(0, 1000),
              random.uniform(0, 1000), random.uniform(0, 1000))
    print(aTuple)
    dbSum = .0
    for item in aTuple:
        dbSum += item
    print('Sum: ' + str(dbSum) + ' Average of sum: ' + str(dbSum / len(aTuple)))

def Test2_10():
    numberIn = float(input('Give me a number between 1 and 100: '))
    while not(1. <= numberIn <= 100.):
        print('Not right')
        numberIn = float(input('Give me a number between 1 and 100: '))
    print('The fucking number is: ' + str(numberIn))

def Test2_11():
    chIn = input('Your operation: ')
    while chIn != 'x' and chIn != 'X':
        if (chIn == '1'):
            print()# Get five numbers
        elif (chIn == '2'):
            print()# Get average number of five numbers
        else:
            print('Fuck yourself')
        chIn = input('Your operation: ')

if ('__main__' == __name__):
    Test2_11()
