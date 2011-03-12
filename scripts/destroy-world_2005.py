#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import platform

if __name__ == "__main__":

    try:
        arg = sys.argv[1]

    except:
        arg = None

    for i in ["fluxbox", "lxde", "xfce", "enlightenment", "gnome", "gnome3", \
            ".", "managers"]:
        os.system("cp -rf /var/www/localhost/htdocs/%s/*.pisi /root/pardusman/repo/" % i)

    if "sync" in sys.argv:
        os.system("wget -r -np http://pardus.comu.edu.tr/2011-devel-%s/" % \
            platform.machine())

        os.system("mv /root/pardusman/repo/pardus.comu.edu.tr/2011-devel-%s/* /root/pardusman/repo/" % platform.machine())

        os.system("rm -rf /root/pardusman/repo/pardus.comu.edu.tr/")

    if "index" in sys.argv:
        os.system("pisi index /root/pardusman/repo/")
        os.system("mv pisi-index.* /root/pardusman/repo/")

    os.system("svn up /root/pardusman/distribution/")

    os.system("python /root/pardusman/pardusman/pardusman.py make \
            /root/pardusman/distribution/%s/installation-%s.xml" % (arg, platform.machine()))
