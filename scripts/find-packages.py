#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from xml.dom import minidom

def get_component(packageName):
    pisi_index = minidom.parse("pisi-index.xml")
    paketler = pisi_index.documentElement.getElementsByTagName("Package")
    for paket in paketler:
        name = paket.getElementsByTagName("Name")
        if name.__len__() != 0:
            name = name[0].toxml()
            name = name.split(">")[1]
            name = name.split("<")[0]
            partof = paket.getElementsByTagName("PartOf")
            partof = partof[0].toxml()

            if name == packageName:
                partof = partof.split(">")[1]
                partof = partof.split("<")[0]
                return partof

def main():
    pisi_index = minidom.parse("pisi-index.xml")
    paketler = pisi_index.documentElement.getElementsByTagName("Package")
    for paket in paketler:
        name = paket.getElementsByTagName("Name")
        if name.__len__() != 0:
            name = name[0].toxml()
            name = name.split(">")[1]
            name = name.split("<")[0]
            partof = paket.getElementsByTagName("PartOf")
            partof = partof[0].toxml()
            partof = partof.split(">")[1]
            partof = partof.split("<")[0]
            dirs = partof.replace(".","/")
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            filename = dirs + "/package.txt"
            if not os.path.exists(filename):
                f = open(filename, "w")
            else:
                f = open(filename, "a")
            f.write(name)

if __name__ == "__main__":
    main()
