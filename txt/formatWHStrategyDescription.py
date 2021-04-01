#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re

def handle_line(line):
    if(re.search(r'@FUNCDESC={', line)):
        lines = line.split('{')
        partLine = lines[1]
        print(partLine)

        result=re.search(r'#?([a-zA-Z_0-9-]+(\([a-zA-Z,.0-9 \']*\))?)(( |,)([a-zA-Z_0-9-]+(\([a-zA-Z,.0-9 \']*\))?))*',partLine)
        if(result):
            result=result.span()
            print(result)
            for i in range(result[1],len(partLine)):
                if(partLine[i]!=' ' and partLine[i]!=',' and partLine[i]!=';'):
                    break;
            lines[1]=partLine[:result[1]]+" "+partLine[i:]

        line='{'.join(lines)
    return line

def handle_file(file='t.txt'):
    try:
        f = open(file, "r")
        f_temp = open(file+".temp", "w")
        for line in f.readlines():
            f_temp.write(handle_line(line))
            
    except Exception(e):
        print(str(e))

def main():
    handle_file('FmlKeyWord.txt')

if __name__=="__main__":
    main()
