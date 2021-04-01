# -*- coding: utf-8 -*-

#coding = gbk

import xdrlib, sys
import xlrd

def open_excel(file= 'App接口_v1.0.1.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception(e):
        print(str(e))
              
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file='App接口_v1.0.1.xlsx',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    list = []
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
             list.append(app)
    return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file, colnameindex, by_name):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #列头行 
    tables = []
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             tables.append(app)
    return tables

def excel_xml_row_2_md_content(rawData):
    bytesData = b""
    if len(rawData["Command Explanation"]):
        bytesData += b"\n## " + rawData["Command Explanation"].encode("utf-8") + b"\n"
    if len(rawData["Command"]):
        bytesData += b"* **Command** `" + rawData["Command"].encode("utf-8") + b"`\n"
        bytesData += b"* **Parameters**\n"
    #print(rawData["Parameters"] + " " + str(len(rawData["Parameters"])))
    #print(rawData["Parameters Explanation"] + " " + str(len(rawData["Parameters Explanation"])))
    if len(rawData["Parameters"]) and len(rawData["Parameters Explanation"]):
        bytesData += b" - **`" + rawData["Parameters"].encode("utf-8") + b"`** " + rawData["Parameters Explanation"].encode("utf-8")
        if rawData["Remark"]:
            bytesData += b" | " + rawData["Remark"].encode("utf-8")
        bytesData += b"\n"
    #print(bytesData.decode("utf-8"))
    return bytesData

#convert excel xml tables content to a MD file
def excel_xml_tables_2_md_file(tables, file):
    try:
        f_md = open(file, "wb")
        for rowData in tables:
            bytesContent = excel_xml_row_2_md_content(rowData)
            f_md.write(bytesContent)
            f_md.flush()
    except Exception(e):
        print(str(e))

def excel_raw_row_2_md_content(rawData):
    bytesData = b""
    bBuffer = False
    if len(rawData["Command Explanation"]):
        bytesData += b"\n## " + rawData["Command Explanation"].encode("utf-8") + b"\n"
    if len(rawData["Command"]):
        bytesData += b"* **Command** `" + rawData["Command"].encode("utf-8") + b"`\n"
        if len(rawData["Parameters Position"]):
            bytesData += b"* **Parameters**\n"
            bytesData += b"    - **" + rawData["Parameters Position"].encode("utf-8") + b"**\n"
            if rawData["Parameters Position"] == "Buffer":
                bBuffer = True
    if not bBuffer and rawData["Parameters Position"] == "Buffer":
        bytesData += b"    - **" + rawData["Parameters Position"].encode("utf-8") + b"**\n"
    if len(rawData["Parameters Explanation"]) and len(rawData["Parameters Name"]) and len(rawData["Parameters Type"]):
        bytesData += b"        + **`" + rawData["Parameters Name"].encode("utf-8") + b"`** `" + rawData["Parameters Type"].encode("utf-8") \
        + b"` | " + rawData["Parameters Explanation"].encode("utf-8")
        if len(rawData["Remark"]):
            bytesData += b" | " + rawData["Remark"].encode("utf-8")
        bytesData += b"\n"
    return bytesData

#convert excel raw tables content to a MD file
def excel_raw_tables_2_md_file(tables, file):
    try:
        f_md = open(file, "wb")
        for rowData in tables:
            bytesContent = excel_raw_row_2_md_content(rowData)
            f_md.write(bytesContent)
            f_md.flush()
    except Exception(e):
        print(str(e))

def excel_data_row_2_md_content(rawData):
    bytesData = b""
    if len(rawData["Parameters Type"]):
        bytesData += b"\n## " + rawData["Parameters Type"].encode("utf-8") + b"\n"
        if len(rawData["Inner Parameters Name"]):
            bytesData += b"* **Type** `struct`\n"
            bytesData += b"* **Struct Inner Layout**\n"
        else:
            bytesData += b"* **Type** `" + rawData["Inner Parameters Type"].encode("utf-8") + b"`\n"
    if len(rawData["Inner Parameters Name"]):
        bytesData += b"    - **" + rawData["Inner Parameters Name"].encode("utf-8") + b"** `" + rawData["Inner Parameters Type"].encode("utf-8") \
        + b"`"
        if len(str(rawData["Follow NULL number"])):
            bytesData += b" | " + str(int(rawData["Follow NULL number"])).encode("utf-8") + b" NULL"
        bytesData += b"\n"
    return bytesData

def excel_data_tables_2_md_file(tables, file):
    try:
        f_md = open(file, "wb")
        for rowData in tables:
            bytesContent = excel_data_row_2_md_content(rowData)
            f_md.write(bytesContent)
            f_md.flush()
    except Exception(e):
        print(str(e))

def excel_meaning_row_2_md_content(rawData):
    bytesData = b""
    if len(rawData["Patameters Name"]) and len(rawData["Parameters Type"]):
        bytesData += b"\n## " + rawData["Patameters Name"].encode("utf-8") + b"\n"
        bytesData += b"* **Type** `" + rawData["Parameters Type"].encode("utf-8") + b"`\n"
        bytesData += b"* **Value Meaning**\n"
    if len(str(rawData["Value"])) and len(rawData["Meaning"]):
        bytesData += b"    - **`" + str(int(rawData["Value"])).encode("utf-8") + b"`** " + rawData["Meaning"].encode("utf-8")
        if len(rawData["Remark"]):
            bytesData += b" | " + rawData["Remark"].encode("utf-8")
        bytesData += b"\n"
    return bytesData

def excel_meaning_tables_2_md_file(tables, file):
    try:
        f_md = open(file, "wb")
        for rowData in tables:
            bytesContent = excel_meaning_row_2_md_content(rowData)
            f_md.write(bytesContent)
            f_md.flush()
    except Exception(e):
        print(str(e))

def excel_tables_2_md_file(tables, file, func):
    try:
        f_md = open(file, "wb")
        for rowData in tables:
            bytesContent = func(rowData)
            f_md.write(bytesContent)
            f_md.flush()
    except Exception(e):
        print(str(e))

def main():
   tables = excel_table_byname()
   for row in tables:
       print(row)

def test1():
    tables = excel_table_byname()
    for row in tables:
        print(row)

def test2():
    tables = excel_table_byname('App接口_v1.0.1.xlsx', 0, u'XML')
    excel_tables_2_md_file(tables, u'XML.md', excel_xml_row_2_md_content)
    tables = excel_table_byname('App接口_v1.0.1.xlsx', 0, u'RAW')
    excel_tables_2_md_file(tables, u'RAW.md', excel_raw_row_2_md_content)
    tables = excel_table_byname('App接口_v1.0.1.xlsx', 0, u'RAW Buffer Data')
    excel_tables_2_md_file(tables, u'RAW Buffer Data.md', excel_data_row_2_md_content)
    tables = excel_table_byname('App接口_v1.0.1.xlsx', 0, u'RAW Data Meaning')
    excel_tables_2_md_file(tables, u'RAW Data Meaning.md', excel_meaning_row_2_md_content)

if __name__=="__main__":
    test2()
