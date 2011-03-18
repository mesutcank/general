#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

try:
    arg = sys.argv[1]
except:
    sys.exit(1)

poFile = open(arg.split(".")[0]+".po", "w")


for i in open(arg, "r").readlines():
    i = i.split("\n")[0]
    if i.startswith("$"):
        continue
    else:
        if not i == "":
            try:
                poFile.write('msgid "%s"\n' % i[i.find(" ")+1:])
                poFile.write('msgstr ""\n\n')
                print "try"
            except:
                poFile.write('msgid "%s"\n' % i)
                poFile.write('msgstr ""\n\n')
                print "except"

