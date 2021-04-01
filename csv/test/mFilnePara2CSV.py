#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os

# Only extract function of trading
def ExtractPara(file):
    try:
        fName = (file.split("/")[-1]).split(".")[0]
        fHandle = open(file, "r")
        fLines = fHandle.readlines()
        bFound = False
        for line in fLines:
            if not (bFound):
                bFound = line.find("% 输入参数") != -1
                if (bFound):
                    fCSV = open("input.csv", "a")
                    fCSV.write(fName + '\n')
                    fCSV.flush()
                    fCSV.close()
                continue
            if(len(line) <= 2):
                fCSV = open("input.csv", "a")
                fCSV.write('\n')
                fCSV.flush()
                fCSV.close()
                break
            else:
                handleInputLine(line)
                
        bFound = False
        for line in fLines:
            if not (bFound):
                bFound = line.find("% 输出参数") != -1
                if (bFound):
                    fCSV = open("output.csv", "a")
                    fCSV.write(fName + '\n')
                    fCSV.flush()
                    fCSV.close()
                continue
            if(len(line) <= 2):
                fCSV = open("output.csv", "a")
                fCSV.write('\n')
                fCSV.flush()
                fCSV.close()
                break
            else:
                handleOutputLine(line)

    except Exception as e:
        print(str(e))


def handleInputLine(line):
    handleLine(line, "input.csv")


def handleOutputLine(line):
    handleLine(line, "output.csv")


def handleLine(line, fileName):
    if(line[2] == " "):
        return
    line = line[2:].strip("\n").split("; ")
    paraComm = "; ".join([''] + line[1:])
    line = line[0].split(": ")
    paraName = line[0]
    line = (": ".join(line[1:])).split(", ")
    if (len(line) < 2):
        return
    paraType = line[1]
    line = ", ".join([line[0]] + line[2:])
    paraComm = "\"" + "\"\"".join(line.split("\"")) + paraComm + "\""        
    try:
        fCSV = open(fileName, "a")
        fCSV.write(",".join((paraName, paraType, paraComm)) + "\n")
        fCSV.flush()
        fCSV.close()
    except Exception as e:
        print(str(e))


def main():
#   ExtractPara('C:/Work/ToolBox/Matlab/Testing/Manual/traderBuy.m')
    mPath = "C:/Code/Python/csv/"
    os.chdir(mPath)
    for f in os.listdir():
        if (os.path.isfile(mPath + f)):
            ExtractPara(mPath + f)

if __name__ == "__main__":
    main()
