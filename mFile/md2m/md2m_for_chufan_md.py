#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os
import shutil


def split_big_md_to_small_md(md_dir_path):
    os.chdir(md_dir_path)
    split_md_dir_path = md_dir_path + '/split_md_for_m'
    if os.path.exists(split_md_dir_path):
        # os.removedirs(split_md_dir_path)
        shutil.rmtree(split_md_dir_path)
    os.mkdir(split_md_dir_path)
    for f in os.listdir():
        f_ext = os.path.splitext(f)[-1]
        if f_ext != '.md':
            continue
        split_md_to_single_md(f, split_md_dir_path)
    return split_md_dir_path


def convert_md_to_m_multi(md_dir_path, m_dir_path):
    # Convert each m file to real one
    if os.path.exists(m_dir_path):
        # os.removedirs(m_dir_path)
        shutil.rmtree(m_dir_path)
    os.mkdir(m_dir_path)
    os.chdir(md_dir_path)
    for md_f in os.listdir():
        md_f_ext = os.path.splitext(md_f)[-1]
        if md_f_ext != '.md':
            continue

        input_md_file_path = md_dir_path + '/' + md_f
        output_m_file_path = m_dir_path + '/' + os.path.splitext(md_f)[0] + '.m'
        convert_md_to_m(input_md_file_path, output_m_file_path)
    return


def split_md_to_single_md(md_file_path, split_md_dir_path):
    # split a big md to every single md
    try:
        md_handle = open(md_file_path, 'r', encoding='utf-8')
        md_lines = md_handle.readlines()
        m_file_name = ''
        m_lines = []
        for line in md_lines:
            if line.startswith('###') and len(line[3:].strip()):
                if len(m_file_name):
                    m_handle = open(split_md_dir_path + '/' + m_file_name + '.md', 'a', encoding='utf-8')
                    m_handle.writelines(m_lines)
                    m_handle.flush()
                    m_handle.close()
                    m_lines.clear()
                m_file_name = line[3:].strip()

            if len(m_file_name):
                m_lines.append(line)

        if len(m_file_name):
            m_handle = open(split_md_dir_path + '/' + m_file_name + '.md', 'a', encoding='utf-8')
            m_handle.writelines(m_lines)
            m_handle.flush()
            m_handle.close()
            m_lines.clear()
    except OSError:
        print('OSError rise')
    return


def convert_md_to_m(input_md_file_path, output_m_file_path):
    try:
        md_handle = open(input_md_file_path, 'r', encoding='utf-8')
        md_lines = md_handle.readlines()
        m_lines = []
        is_last_white = False
        is_count_table = False
        dict_table = dict()
        for line in md_lines:
            if is_count_table:
                if line.startswith('|'):
                    table_content = [c.strip() for c in line.strip(' |').split('|')]
                    if len(table_content) < len(dict_table):
                        for pos in range(len(table_content)):
                            dict_table[pos] += [table_content[pos]]
                        for pos in range(len(table_content), len(dict_table)):
                            dict_table[pos] += ['']
                    else:
                        for pos in range(len(dict_table)):
                            dict_table[pos] += [table_content[pos]]
                    continue
                else:
                    # Save table
                    dict_max_width = {pos: max([len(content) + count_normal_chinese(content) + 1
                                                for content in dict_table[pos]]) for pos in range(len(dict_table))}
                    dict_width = {pos: [dict_max_width[pos] - count_normal_chinese(content)
                                        for content in dict_table[pos]] for pos in range(len(dict_table))}
                    for row in range(len(dict_table[0])):
                        if row == 1:
                            append_line = '=' * sum(dict_max_width.values())
                        else:
                            append_line = ''.join([dict_table[pos][row].ljust(dict_width[pos][row])
                                                   for pos in range(len(dict_table))])
                        m_lines.append(append_line + '\n')

                    dict_table.clear()
                    dict_width.clear()
                    is_count_table = False

            if line.startswith('###') and len(line[3:].strip()):
                # Function name
                m_lines.append(line[3:].strip() + '\n')
                is_last_white = False
                continue
            elif line.startswith('#'):
                continue

            if line.startswith('- ') and len(line[2:].strip()):
                # Title name
                m_lines.append(line[2:].strip() + '\n')
                is_last_white = False
                continue
            elif line.startswith('-'):
                continue

            if line.startswith('|'):
                table_header = [h.strip() for h in line.strip(' |').split('|')]
                dict_table = {n: [table_header[n]] for n in range(len(table_header))}
                is_count_table = True
                is_last_white = False
                continue

            if line.strip():
                is_last_white = False
                m_lines.append(line.rstrip() + '\n')
            else:
                if is_last_white:
                    continue
                else:
                    m_lines.append('\n')
                    is_last_white = True

        m_handle = open(output_m_file_path, 'w', encoding='gbk')
        m_lines = ['% ' + s for s in m_lines]
        m_handle.writelines(m_lines)
        m_handle.flush()
        m_handle.close()

    except OSError:
        print('OSError rise')
    return


def count_normal_chinese(input_str):
    # \u4E00-\u9FA5 normal chinese character
    # \uFF00-\uFFEF normal chinese symbol
    return len(re.findall(u'[\u4E00-\u9FA5\uFF00-\uFFEF]', input_str))


def main():
    # md_dir_path = 'C:/Code/Python/mFile/md2m'
    md_dir_path = os.getcwd()
    print('Begin convert md file in path: ' + md_dir_path)
    m_dir_path = md_dir_path + '/converted_m'
    split_md_dir_path = split_big_md_to_small_md(md_dir_path)
    print('Split md file saved into path: ' + split_md_dir_path)
    convert_md_to_m_multi(split_md_dir_path, m_dir_path)
    print('Finished converting m file into path: ' + m_dir_path)


if __name__ == '__main__':
    main()
