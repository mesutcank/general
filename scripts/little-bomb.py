#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Experimental new Perl PiSi package builder
# See Usage function for instructions.
#
# inspired by Onur's newpisipackage and bump scripts
#
# just put a .pisipackager file in your home and fill it like
#
# name = Onur Küçük
# email = onur@pardus.org.tr
#
# or directly write it to Package Information part.

import os
import sys
import time
import string
import pisi

packagerfile = ".pisipackager"

# Packager Information
name = "Mesutcan Kurt"
email = "mesutcank@gmail.com"

data = {"date": time.strftime("%Y-%m-%d")}

temp_pspec = '''<?xml version="1.0" ?>
<!DOCTYPE PISI SYSTEM "http://www.pardus.org.tr/projeler/pisi/pisi-spec.dtd">
<PISI>
    <Source>
        <Name>%(package)s</Name>
        <Homepage>%(homepage)s</Homepage>
        <Packager>
            <Name>%(packager_name)s</Name>
            <Email>%(packager_email)s</Email>
        </Packager>
        <License>GPLv2</License>
        <IsA>library</IsA>
        <Summary>FIXME!!</Summary>
        <Description>FIXME!!</Description>
        <Archive sha1sum="a" type="%(archive_type)s">%(download_address)s</Archive>
        <BuildDependencies>
            <Dependency>xfce4-panel-devel</Dependency>
        </BuildDependencies>
        <!--
        <Patches>
            <Patch level="1"></Patch>
        </Patches>
        -->
    </Source>

    <Package>
        <Name>%(package)s</Name>
        <RuntimeDependencies>
            <Dependency>xfce4-panel</Dependency>
        </RuntimeDependencies>
        <Files>
            <Path fileType="config">/etc</Path>
            <Path fileType="executable">/usr/bin</Path>
            <Path fileType="executable">/usr/libexec</Path>
            <Path fileType="doc">/usr/share/doc</Path>
            <Path fileType="doc">/usr/share/xfce4/doc</Path>
            <Path fileType="data">/usr/share/xfce4</Path>
            <Path fileType="data">/usr/share/applications</Path>
            <Path fileType="data">/usr/share/icons</Path>
            <Path fileType="localedata">/usr/share/locale</Path>
        </Files>
    </Package>

    <History>
        <Update release="1">
            <Date>%(date)s</Date>
            <Version>%(version)s</Version>
            <Comment>First release.</Comment>
            <Name>%(packager_name)s</Name>
            <Email>%(packager_email)s</Email>
        </Update>
    </History>
</PISI>
'''

temp_actions = '''#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import perlmodules
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

WorkDir = "%s-%s" % (get.srcNAME()[5:], get.srcVERSION())

def setup():
    autotools.configure()

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "NEWS", "README", "TODO")

'''

temp_translation = '''<?xml version="1.0" ?>
<PISI>
    <Source>
        <Name>%(package)s</Name>
        <Summary xml:lang="tr">DUZELT</Summary>
        <Description xml:lang="tr">%(package)s bir Xfce modülüdür.</Description>
    </Source>
</PISI>
'''

def usage():
    print "Usage : %s NewPackageDir DownloadAddress" % sys.argv[0]
    print " "
    print "Example : %s ~/playground/hede_package http://www.download.com/hede_package.tar.gz " % sys.argv[0]
    print " "

def write(filename, data):
    try:
       f = file("%s/%s" % (target, filename), "w")
       f.write(data)
       f.close()
    except:
        print "Could not write file %s/%s" % (target, filename)

def readConfig():
    home = os.getenv("HOME", "")
    cfg = "%s/%s" % (home, packagerfile)
    d = {"name": "", "email": ""}

    if home != "" and os.path.exists(cfg):
        for line in file(cfg):
            if line != "" and not line.startswith("#") and "=" in line:
                l, m = line.split("=", 1)
                k = l.strip()
                v = m.strip()
                if k in ["name", "email"]:
                    if v.startswith('"') or v.startswith("'"):
                        v = v[1:-1]
                    d[k.strip()] = v.strip()
    else:
        d["name"] = name
        d["email"] = email

    return d["name"], d["email"]

def remove_comment_out():
    ret = []
    for l in open("actions.py" ,"r").readlines():
        if "# WorkDir =" in l:
            ret.append(l.split("# ")[1])
        elif "#from pisi" in l:
            pass
        else:
            ret.append(l)

    return "".join(ret)


def update_Workdir(WorkDir):
    ret = []
    if WorkDir.split("-")[-1] == data["version"]:
        WorkDir = '"' + WorkDir.split(data["version"])[0] + '%s" % get.srcVERSION()'
        commentout_get_import = True
    else:
        WorkDir = '"' + WorkDir + '"'
        commentout_get_import = False

    for l in open("actions.py" ,"r").readlines():
        if "#from pisi" in l:
            if commentout_get_import:
                ret.append(l.split('#')[1])
            else:
                pass

        elif "# WorkDir =" in l:
            ret.append("WorkDir = %s\n" % WorkDir)
        else:
            ret.append(l)

    return "".join(ret)


def update_sha1sum(fl):
    sh = os.popen("sha1sum /var/cache/pisi/archives/%s" %fl).read().split()[0]
    print sh

    if sh:
        ret = []
        for l in open("pspec.xml", "r").readlines():
            if "<Archive" in l:
                nls = l.split("sha1sum=\"")
                nl = nls[0] + "sha1sum=\"%s\"" %sh + nls[1].split("\"", 1)[1]
                ret.append(nl)
            else:
                ret.append(l)

        return "".join(ret)

if __name__ == "__main__":

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    else:
        target = sys.argv[1]
        data["homepage"] = "http://goodies.xfce.org/projects/panel-plugins/%s" % (sys.argv[1])[6:]

        download_addr = sys.argv[2]  # TODO: will be parsed for mirrors
        data["download_address"] = download_addr
        data["packagedir"], data["package"] = os.path.split(target)

    if data["packagedir"]:
        os.chdir(data["packagedir"])
    else:
        pass

    if os.path.exists(target):
        print "%s already exists, please remove it first" % target
        sys.exit(1)
    else:
        try:
            os.makedirs(target)
        except:
            print "a problem occured while trying to create %s" % target
            sys.exit(1)

    # Locate the version and archive_type of the package.
    version = download_addr.split("-")[-1]
    if "tar" in version:
        if version.split(".tar")[1] == "bz2":
            data["archive_type"] = "tarbz2"
        else:
            data["archive_type"] = "targz"
        version = version.split(".tar")[0]
    elif "tgz" in version:
        data["archive_type"] = "targz"
        version = version.split(".tgz")[0]
    else:
        data["archive_type"] = "zip"
        version = version.split(".zip")[0]

    data["version"] = version

    # here we go
    data["packager_name"], data["packager_email"] = readConfig()
    write("pspec.xml", temp_pspec % data)
    write("actions.py", temp_actions)
    write("translations.xml", temp_translation % data)

    os.chdir("%s" %target)

    # First fetch the tarball
    if os.getenv("USER") != "root":
        os.system("sudo pisi build pspec.xml --fetch")
    else:
        os.system("pisi build pspec.xml --fetch")

    fl = os.path.basename(pisi.specfile.SpecFile('pspec.xml').source.archive[0].uri)

    newpspec = update_sha1sum(fl)
    open("pspec.xml", "w").write(newpspec)

    # Get WorkDir() of the package
#    if os.getenv("USER") != "root":
#        os.system("sudo pisi build pspec.xml --unpack")
#    else:
#        os.system("pisi build pspec.xml --unpack")
#
#    for i in os.listdir("/var/pisi/%(package)s-%(version)s-1/work/" % data ):
#        if os.path.isdir("/var/pisi/%s-%s-1/work/%s" % (data["package"], data["version"], i)):
#            WorkDir = i

    # Compare WorkDir with package name
#    if WorkDir == "%(package)s-%(version)s" % data:
#        print "\t!!No need to update WorkDir!!"
#    elif WorkDir == "python-%(package)s-%(version)s" % data:
#        newactions = remove_comment_out()
#        open("actions.py", "w").write(newactions)
#    else:
#        newactions = update_Workdir(WorkDir)
#        open("actions.py", "w").write(newactions)

    # Build the package
    if os.getenv("USER") != "root":
        os.system("sudo pisi build pspec.xml")
    else:
        os.system("pisi build pspec.xml")


