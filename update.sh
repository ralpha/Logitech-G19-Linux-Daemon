#!/bin/sh

INSTALLDIR=/usr/lib/g19

ROOT_UID="0"

#Check if run as root
if [ $(id -u) != "$ROOT_UID" ] ; then
	echo "You need root permission to install this."
	echo "Run:"
	echo "\t\033[93msudo ./update.sh"
	echo "\033[1m\033[31mUpdate failed"
	exit 1
fi

# make directory
echo "Make install folder: $INSTALLDIR"
mkdir $INSTALLDIR

# copy src
echo "Install G19..."
cp -R ./src/* /usr/lib/g19/

# start service
echo "Start app..."
/usr/lib/g19/g19-startup.sh


echo "\033[1m\033[92mUpdate succesfull"

