#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from pisi import api as pisiapi

def usage(err_id):
    if err_id == 0:
        sys.stderr.write("No Parameter Found: Repo is Needed. \n")
        sys.exit(1)
    if err_id == 1:
        sys.stderr.write("Missing Argument: Repo Address. \n")
        sys.exit(1)

def isRepoUri(repo_name):
    #decide whether it is a uri or a name
    if repo_name.endswith(".xml.xz") or repo_name.endswith(".xml.bz2"):
        return True
    else:
        return False

def get_from_db(repo_name):
    #Find the repo_name in pisi db.
    found = False
    try:
        pisiapi.list_repos().index(repo_name)
        #sys.sysout.write("Repo %s found in pisi.\n" % repo_name)
    except:
        #If not found, Exit.
        sys.stderr.write("Repo %s not found.\n" % repo_name)
        sys.exit(1)

    #Delete Cache whether if it has our packages
    print "Deleting Pisi Cache..."
    pisiapi.delete_cache()
    print "Done."

    #Update Repos
    print "Updating Repo: %s..." % repo_name
    pisiapi.update_repos(["%s" % repo_name])
    print "Done."

    #Get package list in repo
    print "Generating package list..."
    package_list = pisiapi.list_available(repo_name)
    print "Done."

    #Install packages
    #TODO: With --reinstall maybe?
    print "Installing %s packages, please wait..." % len(package_list)
    pisiapi.install(package_list)
    print "Done."

def main(arguments):
    #User should be root!
    if not os.geteuid()==0:
        sys.stderr.write("Only \"root\" can do that. \n \nThis incident will be reported.\n")
        sys.exit(1)

    #get the repo uri or/and name
    try:
        repo_param1 = arguments[1]
        if isRepoUri(repo_param1):
            usage(1)
    except:
        usage(0)

    try:
        repo_param2 = arguments[2]
        if isRepoUri(repo_param2):
            usage(2)
        add_to_db(repo_param1, repo_param2)
    except:
        get_from_db(repo_param1)

if __name__ == "__main__":
    main(sys.argv)
