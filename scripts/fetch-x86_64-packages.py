#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib
from httplib import HTTP
from urlparse import urlparse

def checkURL(url):
     p = urlparse(url)
     h = HTTP(p[1])
     h.putrequest('HEAD', p[2])
     h.endheaders()
     if h.getreply()[0] == 200: return 1
     else: return 0

path=os.getcwd()

file_list= os.listdir(path)
package_list=[]

not_found = open("not_found.txt","w")
found = open("found.txt","w")
for i in file_list:
    if i.endswith(".pisi"):
            pack=i[:-9]
            pack_64=pack+'x86_64.pisi'
            package_list.append(pack_64)

os.mkdir("x86_64")
for i in package_list:
    url="http://packages.pardus.org.tr/pardus/2011/devel/x86_64/"+i
    if not checkURL(url):
        not_found.write(i+" not found\n")
        print "File %s not found." % i
        continue
    print "\nFetching \"%s\" file..." % i
    urllib.urlretrieve(url,'x86_64/'+i)
    found.write(i+" found\n")
    print "\t"*11 + ".done."
