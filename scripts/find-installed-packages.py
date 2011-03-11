#!/usr/bin/python
# -*- coding: utf-8 -*-

from find-packages import find_component
import os
from pisi import api as pisiapi

def main():
    installed = pisiapi.list_installed()
    installed.sort()
    list_file = open("installed.txt", "w")
    for i in installed:
        componentOf = find_component(i)
        #componentOf = "system.base"
        dirs = componentOf.replace(".","/")
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        filename = dirs + "/installed.txt"
        if not os.path.exists(filename):
            list_file2 = open(filename, "w")
        else:
            list_file2 = open(filename, "a")
        list_file2.write(i+"\n")
    list_file.close()

if __name__ == "__main__":
    main()
