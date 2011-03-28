#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import platform

def index_repos():
#    for i in ["fluxbox", "enlightenment", "lxde", "xfce", "gnome", "gnome3", "managers"]:
    for i in ["comak"]:
        if not os.path.exists("/var/www/localhost/htdocs/%s/" % i):
            os.makedirs("/var/www/localhost/htdocs/%s/" % i)
        os.system("pisi index /var/www/localhost/htdocs/%s/" % i)
        os.system("mv pisi-index.* /var/www/localhost/htdocs/%s/" % i)
        os.system("rm -f /var/www/localhost/htdocs/%s/index.htm*" % i)


if __name__ == "__main__":

    os.system("pisi ur")

    out = subprocess.Popen(["buildfarm up"], shell=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
    out.wait()

    output = out.communicate()[0]
    found = False

    queue = open("/var/lib/buildfarm/workqueue", "r")
    queueList = queue.readlines()
    queue.close()

    for i in output.split("\n"):
        if "testing" in i:
            continue
        i=i.strip()
        if i.endswith("pspec.xml"):
            for que in queueList:
                que = que.split("\n")[0]
                if i == que:
                    found = True
            if not found:
                queueList.append(i + "\n")
                found = False
    queue = open("/var/lib/buildfarm/workqueue", "w")
    queue.writelines(queueList)
    queue.close()

    queue = open("/var/lib/buildfarm/workqueue", "r")
    queueList = queue.readlines()
    queue.close()

    try:
        arg = sys.argv[1]

    except:
        arg = None

    if arg != None:
        out = subprocess.Popen(["find /var/lib/buildfarm/repositories/COMAK/%s/ \
                -name pspec.xml" % arg], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out.wait()

        findList = out.communicate()[0]
    else:
        findList = None

    if findList != None:

        for i in findList.split("\n"):
            found = False
            i=i.strip()
            if i.endswith("pspec.xml"):
                for que in queueList:
                    que = que.split("\n")[0]
                    if i == que:
                        found = True
                        break
                if not found:
                    queueList.append(i + "\n")

        queue = open("/var/lib/buildfarm/workqueue", "w")
        queue.writelines(queueList)
        queue.close()


    if not os.path.exists("/var/db/buildfarm/packages/COMAK/packages/%s-orig" % platform.machine()):
        os.makedirs("/var/db/buildfarm/packages/COMAK/packages/%s-orig" % platform.machine())
    os.system("mv /var/db/buildfarm/packages/COMAK/packages/%s/* /var/db/buildfarm/packages/COMAK/packages/%s-orig/" % (platform.machine(), platform.machine()))

#   queue = open("/var/lib/buildfarm/workqueue", "r")
#   queueList = queue.readlines()
#   queue.close()

    os.system("buildfarm run")


#    for que in queueList:
#        que=que.split("\n")[0]
#        que=que.split("COMAK/packages/")[1]
#        _pak_name = que.split("/pspec.xml")[0]
#        pak_name = _pak_name[_pak_name.rfind("/")+1:]
#
#        comp1 = que[0:que.find("/")]
#        if comp1 == "desktop":
#            comp2 = que.split("desktop/")[1]
#            comp2 = comp2[:comp2.find("/")]
#            os.system("cp -f /var/db/buildfarm/packages/COMAK/packages/%s/%s* /var/www/localhost/htdocs/%s/" % (platform.machine(), pak_name, comp2))
#        elif comp1 == "managers":
#            os.system("cp -f /var/db/buildfarm/packages/COMAK/packages/%s/%s* /var/www/localhost/htdocs/%s/" % (platform.machine(), pak_name, comp1))
#
#        else:
#            os.system("cp -f /var/db/buildfarm/packages/COMAK/packages/%s/%s* /var/www/localhost/htdocs/" % (platform.machine(), pak_name))
#
    os.system("cp -n /var/db/buildfarm/packages/COMAK/packages/%s/*.pisi /var/www/localhost/htdocs/comak" % platform.machine())


    index_repos()
