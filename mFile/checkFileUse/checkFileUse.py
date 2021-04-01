#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os


def find_func_in_line(line):
    result = re.findall(r'[a-zA-Z_]\w*\(', line)
    result = [res[: -1] for res in result]
    func_in_line = set(result)
    return func_in_line


def find_inner_function_call(file_name):
    func_in_file = set()
    try:
        f_temp = open(file_name, "r")
        for line in f_temp.readlines():
            func_in_file = func_in_file | find_func_in_line(line)
    except IOError as e:
        print(e)
    finally:
        f_temp.close()
    return func_in_file


def main():
    #   ExtractPara('C:/Work/ToolBox/Matlab/Testing/Manual/traderBuy.m')
    m_path = "C:/Code/Python/mFile/checkFileUse"
    os.chdir(m_path)
    file_inner_func_call = {}
    all_inner_func_call = set()
    file_no_one_call = set()
    for f in os.listdir():
        if not os.path.isfile(f):
            continue
        file_inner_func_call[f] = find_inner_function_call(f)
        all_inner_func_call = all_inner_func_call | file_inner_func_call[f]
        # if (os.path.isfile(mPath + f)):
        #     ExtractPara(mPath + f)
    for f in os.listdir():
        if not os.path.isfile(f) or f.startswith('trader'):
            continue
        if os.path.splitext(f)[0] not in all_inner_func_call:
            file_no_one_call.add(f)
            print(f)
    print(file_no_one_call)


if __name__ == "__main__":
    main()
