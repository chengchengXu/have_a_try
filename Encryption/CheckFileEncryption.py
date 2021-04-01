#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

def CheckFileSHA256(filePath, fileSHA256):
    f = open(filePath, 'rb')
    sh = hashlib.sha256()
    sh.update(f.read())
    print("FilePath: " + filePath)
    print("Given FileSHA256: " + fileSHA256)
    print("Calculated FileSHA256: " + sh.hexdigest())
    return fileSHA256 == sh.hexdigest()

def CheckFileMD5(filePath, fileMD5):
    f = open(filePath, 'rb')
    sh = hashlib.md5()
    sh.update(f.read())
    print("FilePath: " + filePath)
    print("Given FileMD5: " + fileMD5)
    print("Calculated FileMD5: " + sh.hexdigest())
    return fileMD5 == sh.hexdigest()

def CheckFileSHA1(filePath, fileSHA1):
    f = open(filePath, 'rb')
    sh = hashlib.md5()
    sh.update(f.read())
    print("FilePath: " + filePath)
    print("Given FileSHA1: " + fileSHA1)
    print("Calculated FileSHA1: " + sh.hexdigest())
    return fileSHA1 == sh.hexdigest()

def main():
##    print("xerces-c-3.1.4.zip: " + str(CheckFileMD5('C:\\Downloads\\xerces-c-3.1.4.zip', '6fcd8ec268f6bfe11d8ce2cd7d25a185')))
    print("Haskell.exe: " + str(CheckFileSHA256('C:\Downloads\HaskellPlatform-8.0.1-full-x86_64-setup-a.exe', 'b3a5a1e95e6f9348e0f02aef928c893efaa1811914c486ceb8d6898e1a2c00ce')))
    print("Python.exe: " + str(CheckFileMD5('C:\Downloads\python-3.5.2-amd64.exe', '4da6dbc8e43e2249a0892d257e977291')))
    return

if __name__ == "__main__":
    main()
