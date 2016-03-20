#!/bin/sh

ROOT_UID="0"

#Check if run as root
if [ $(id -u) != "$ROOT_UID" ] ; then
	echo "You need root permission to run this."
	exit 1
fi

cd /usr/lib/g19/

#DATE=$(date +"%m-%d-%y");

#/usr/lib/g19/g19.py >> /usr/lib/g19/log/$DATE.out 2>> /usr/lib/g19/log/$DATE.err &
/usr/lib/g19/g19.py &
