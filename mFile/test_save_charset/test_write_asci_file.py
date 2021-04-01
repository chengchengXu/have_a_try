#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os
import shutil


def main():
    print(os.path.dirname(os.path.realpath(__file__)))
    print(os.getcwd())

    f_dir = os.getcwd()
    os.chdir(f_dir)
    for md_f in os.listdir():
        md_f_ext = os.path.splitext(md_f)[-1]
        if md_f_ext != ".md":
            continue

        try:
            md_handle = open(md_f, 'r', encoding='utf-8')
            md_lines = md_handle.readlines()
            m_lines = ["% " + line for line in md_lines]
            m_lines += ['% block    char 板块或指数的名称，其中\'index\'——返回所有指数；\'plate_industry\'——返回全部行业']
            # m_lines += ['% ——']

            m_f = os.path.splitext(md_f)[0] + ".m"
            m_handle = open(m_f, 'w', encoding='gbk')
            m_handle.writelines(m_lines)
            m_handle.flush()
            m_handle.close()

        except OSError:
            print('OSError rise')


if __name__ == "__main__":
    main()
