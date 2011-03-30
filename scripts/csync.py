#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
from httplib import HTTP
from urlparse import urlparse
import os

SESSIONS = ["server", "client"]
CSYNC_FILE = "csync.list"

def check_url(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200:
        return True
    else:
        return False

def get_list():
    return os.listdir(os.getcwd())

def write_list_to_file():
    fileList = open(CSYNC_FILE, "w")
    items = []
    for item in get_list():
        items.append(item.rstrip())

    items.sort()

    for item in items:
        if item == CSYNC_FILE or item.startswith("."):
            continue
        fileList.write(item + "\n")
    fileList.close()


def main(arguments):
    url = ""
    session = ""
    try:
        session = arguments[1]
    except:
        print "You must start a client or server session"
        sys.exit(1)

    if not session in SESSIONS:
        print "Smarty, but our choices are %s" % SESSIONS
        sys.exit(1)

    if session == SESSIONS[0]:
        print "COMAK Sync: Server session is started!...\n"

        write_list_to_file()

        print "COMAK Sync: Server session is finished!...\n \
                file: %s is ready." % CSYNC_FILE


    if session == SESSIONS[1]:
        print "COMAK Sync: Client session is started!...\n"
        try:
            url = arguments[2]
        except:
            print "Couldn't find the url. Are you OK?"
            sys.exit(1)

        if url != "":
            if not check_url(url):
                print "Couldn't find %s" % url
            print "Fetching %s file to get file list..." % CSYNC_FILE
            try:
                urllib.urlretrieve(url + CSYNC_FILE, CSYNC_FILE + SERVER_EXT)
            except:
                print "Couldn't fetch %s... Aborting..." % CSYNC_FILE
                sys.exit(1)
            print "\t\t\t\t\tDone..."

            write_list_to_file()

            diff = subprocess.Popen(["diff -Nuar %s %s" % \
                    (CSYNC_FILE, CSYNC_FILE + SERVER_EXT)], shell=True, \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            diff.wait()

            diffResult = diff.communicate()[0]

            for item in diffResult():
                if item.startswith("+"):
                    fileName = item.split("+")[1]
                    print "Fetching %s..." % fileName
                    try:
                        urllib.urlretrieve(url + fileName)
                    except:
                        print "Couldn't fetch %s....." % fileName

if __name__ == "__main__":
    main(sys.argv)
