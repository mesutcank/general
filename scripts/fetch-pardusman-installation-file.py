#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xml.dom.minidom

fayl = open("hede.txt", "w")

def parse(dom_file):
    for a in dom_file.getElementsByTagName("PardusmanProject"):
        for b in a.getElementsByTagName("PackageCollections"):
            for c in b.getElementsByTagName("PackageCollection"):
                for d in c.getElementsByTagName("PackageSelection"):
                    for e in d.getElementsByTagName("SelectedComponent"):
                        fayl.write("Component: %s\n" % e.toxml().split("<SelectedComponent>")[1].split("</SelectedComponent>")[0])
                    for f in d.getElementsByTagName("SelectedPackage"):
                        fayl.write("Package: %s\n" % f.toxml().split("<SelectedPackage>")[1].split("</SelectedPackage>")[0])


def main(arguments):
    #open the file
    xml_file = open(arguments[1])
    #copy file to a string and close file
    xml_file_string = xml_file.read()
    xml_file.close()
    #get the xml file from first argument
    dom_xml = xml.dom.minidom.parseString(xml_file_string)
    parse(dom_xml)




if __name__ == "__main__":
    main(sys.argv)
