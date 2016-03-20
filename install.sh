#!/bin/sh

INSTALLDIR=/usr/lib/g19

ROOT_UID="0"

#Check if run as root
if [ $(id -u) != "$ROOT_UID" ] ; then
	echo "You need root permission to install this."
	echo "Run:"
	echo "\t\033[93msudo ./install.sh"
	echo "\033[1m\033[31mInstall failed"
	exit 1
fi

# make directory
echo "Make install folder: $INSTALLDIR"
mkdir $INSTALLDIR

# copy src
echo "Install G19..."
cp -R ./src/* /usr/lib/g19/

#make run without pass
echo "Add to startup"
validuser=false
username="root"
while ! ( $validuser ) ; do
  if [ -z "$1" ]; then 
    echo "Type your username: (eg. 'bob', 'eva')"
    read username
  else 
    username=$1; 
  fi

  id -u $username > /dev/null 2> /dev/null
  if [ "$?" = "0" ] ; then
    validuser=true
  else
    echo "\t\033[31mUser '$username' doesn't exist on this system.\033[0m"
  fi
done;
echo "Cmnd_Alias G19STARTUP = /usr/lib/g19/g19-startup.sh\n$username ALL=NOPASSWD:G19STARTUP" > /etc/sudoers.d/g19

#add file for ubuntu application startup
userhomedir=$(eval echo "~$username")
cp ./service/G19.desktop $userhomedir/.config/autostart/G19.desktop


# start service
echo "Start app..."
/usr/lib/g19/g19-startup.sh


echo "\033[1m\033[92mInstall succesfull"

echo "\033[0mIf you want to use the \033[1mCalendar\033[0m applet to work install the following packages:"
echo "\033[31m\tpip install pyRFC3339"
echo "\033[31m\tpip install pytz"
echo "\033[31m\tpip install tzlocal"

echo "\033[0mIf you want to use the \033[1mXPlanet\033[0m applet to work install the following packages:"
echo "\033[31m\tsudo apt-get install xplanet xplanet-images"

