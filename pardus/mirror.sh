#!/bin/bash

if [ "$#" = "0" ]; then
	echo "usage: $0 <repo_directory> <mirror> <distro_codename>";
	exit 1;
fi

apt-get install ed debmirror

debmirror $1 -v --source --i18n --diff=mirror \
	  --host=$2 --di-dist=$3, --di-arch=amd64,i386 \
	  --dist=$3,$3-proposed-updates \
	  --arch=amd64,i386 --getcontents \
	  --method=http \
	  --section=main,contrib,non-free,main/debian-installer
