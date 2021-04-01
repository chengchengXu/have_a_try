#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re


def NorStr2CSVStr(item=''):
    result = re.search(r',', item)
    print(item)
    if (result):
        item = '\"' + item + '\"'
        print(item)
    return item


def handle_line(line):
    if (re.search(r'@FUNCDESC={', line)):
        line = line.split('{')[1]
        line = line.split('}')[0]
        line = line.split('\r')[0]
        line = line.split('\n')[0]

        des = ''
        func = ''
        result = re.search(
            r'#?([a-zA-Z_0-9-]+(\([a-zA-Z,.0-9 \']*\))?)(( |,)([a-zA-Z_0-9-]+(\([a-zA-Z,.0-9 \']*\))?))*', line)
        if (result):
            result = result.span()
            des = line[result[1] + 1:]
            func = line[result[0]:result[1]]
            result = re.search(r'#?[a-zA-Z_0-9-]+', func)
            if result:
                result = result.span()
                func = func[result[0]:result[1]]
        return NorStr2CSVStr(func) + ',' + NorStr2CSVStr(des)
    return ''


def handle_file(file='t.txt'):
    try:
        f_temp = open(file + ".temp", "r")
        f_csv = open(file + ".csv", "w")
        for line in f_temp.readlines():
            line = handle_line(line)
            if (line != ''):
                f_csv.write(line + '\n')
                f_csv.flush()
    except Exception(e):
        print(str(e))


def main():
    handle_file('FmlKeyWord.txt')


if __name__ == "__main__":
    main()
