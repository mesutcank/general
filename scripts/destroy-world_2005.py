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
        sys.stderr.write("ERROR: No Args Found!")
        sys.exit(0)

    if "updatePackages" in sys.argv:
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

    os.system("rm -rf /root/pardusman/work/%s/workDir/*" % arg)
    os.system("rm -rf /root/pardusman/work/%s/releaseNotes/*" % arg)

    os.system("python /root/pardusman/pardusman/pardusman.py make \
            /root/pardusman/distribution/%s/installation-%s.xml" % (arg, platform.machine()))

    os.system("cp -f /root/pardusman/work/%s/workDir/*.iso /var/www/localhost/htdocs/" % arg)
