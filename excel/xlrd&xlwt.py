# -*- coding: utf-8 -*-

import xdrlib, sys
import xlrd
import xlwt

def open_excel(filename):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception(e):
        print(str(e))

def handle_excel(data):
    

def main():
    filename = u".xlsx"
    data = open_excel(filename)
    handle_excel(data)

def __name__=="__main__":
    main()
