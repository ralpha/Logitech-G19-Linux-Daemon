# G19 Drivers for linux (Debian/Ubuntu based) systems.

This is a stable\* version of the drivers for a G19 keyboard on linux (Debian/Ubuntu based).

\* Stable in the sense that I have not been able to crash it or anything from normal use. This will also not break anything else on your computer.

Features of the system:
 - change backlit keys color
 - applets that use the display
 - change display brightness
 - installer
 - startup with system startup
 
Not working (correctly):
 - map G-keys

This code was based on sblatt his repository: https://github.com/sblatt/Logitech-G19-Linux-Daemon

Applets:
 - Google Calendar: view upcoming events of the display
 - Clock: see the date en time
 - Timer: have a timer that counts down (doesn't make sound yet)
 - Display Brightness: change the brightness of the display
 - Background light: change the key lights color
 - Slideshow: display pictures.
 - XPlanet: Show a spinning earth
 - Sample Applet: sample code for making your own applet
 - Exit: shut down keyboard drivers (may reset media keys)
 
Screenshots:
http://imgur.com/a/IEHRv

![screenshot](http://i.imgur.com/RpX4fRe.png)
![screenshot](http://i.imgur.com/2MbBCwo.png)


How to install:
 - make sure you have python installed
    - $ python --version
    - Python 2.7.x (might work with other versions, I'm running 2.7.6)
 - browse to install folder (contains src and service folder)
 - open terminal
```sh
$ sudo ./install.sh
```
 - type the username that you currently use
 - ...installing...
 - your keyboard should not light up and work. :D
 
Addition steps:
 - for calendar install additional packages:
```sh
$ pip install pyRFC3339
$ pip install pytz
$ pip install tzlocal
```
 - for calendar applet you need to create a client_secret.json file:
    - Follow instructions: https://developers.google.com/api-client-library/python/samples/samples
        1. Open the Credentials page. https://console.developers.google.com/project/_/apiui/credential
        2. Under OAuth, click Create New Client ID.
        3. Select Installed Application and Other and click Create Client ID.
        4. Copy the client ID and client secret values under Client ID for native application and paste into the client_id and client_secret fields in the downloaded client_secrets.json file. 
        5. paste the client_secret.json in the folder: ~/.lg19/client_secret.json
    - My instructions:
        1. Open the Credentials page. https://console.developers.google.com/project/_/apiui/credential
        2. screenshots: http://imgur.com/a/SORfp
        3. Download the file and save it as client_secret.json in the folder: ~/.lg19/client_secret.json
 - for XPlanet install additional packages:
```sh
sudo apt-get install xplanet xplanet-images
```
Known problems:
Calendar
 - No known problems
 - Add 'all' calendar option.
 
Display Brightness
 - Can not capture volume keys
 
Background light
 - Can not capture volume keys
 
Timer
 - Can use improvements in saving set time
 

If all breaks you need to shut down the app called g19.py in system manager (need root to do this)
This will do the job (at least if you have no other apps that are called this way):
```sh
sudo pkill g19.py
```
