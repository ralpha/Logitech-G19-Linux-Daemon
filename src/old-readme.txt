************IMPORTANT******************

I stoped working on this project as I'm now involved in an even better project for the Logitech G19:

http://g19linux.sourceforge.net/

If you want to continue this deamon, feel free to do so, or just join us at sourceforge!

***************************************


=== Logitech G19 Linux support ===

This is work in progress and considered absolutely alpha.  It SHOULD work, but no
guarantees are given.  If your keyboard goes up in flames, explodes and rapes
your hamster, don't say I didn't warn you!

This are my (sBlatt) additions to MultiCoreNOPs code, search für him @ gitHub if you want the original code

check out the Video: http://www.youtube.com/watch?v=dJN4_Ny7QkU

*** Warning: this driver is not at all stable and I consider this a development branch! It *should* not break
	     anything, but if it does, bad for you! I will upload a .deb beta Package as soon as i consider
	     it rather stable and a .deb package with an autostart daemon as soon as I'm shure it realy doesn't
	     crash! If you want to test it, I invite you to do so and send me bugs to sblatt2@gmail.com or
	     on github (http://github.com/sblatt/Logitech-G19-Linux-Daemon).

Now have fun with the Logitech G19 Linux Daemon


=== What you need to use this ===

Python 2.6
pyusb
python-virtkey
python-tk

optional:
PySide (not yet)

=== How to install ===

- Get the code
- unzip to any location
- start a terminal
- cd to the folder
- type sudo python main.py (usb needs root, change your permissions if you want to start this as a normal user)
- if it can't finde your fonts change path in ~/.lg19/lg19.cfg

=== How it works ===

- The menu shows your installed applets. As of now (11.5.10) only the simple_slideshow and simple_clock-applets have been tested, the others might work
***UPDATE*** All applets except the display brightness applet should work, maybe you have to change the fonts-path in g19.py if it can't find your fonts!
- Navigate with your display-keys
- Press OK to start an applet
- Press MENU to go back to the Menu (there is a chance the applet wil reapear on its own, just press MENU again)
- some applets use the option key (see below)

- if anything goes wrong: sudo killall python (might kill some other processes)

==== some tips ====
- If an applet crashes, most of the time it's possible to go back to the menu by pressing the MENU-Key (crashed app will be terminated)
- Ther will be created a config file @ ~/.lg19/lg19.cfg . check it out to check values manually
- Don't try any fancy stuff - Or please do so and send me the error log and a short summary of what you were doing

==== Special Keys ====
- After starting, you can map the G-Keys like any other Multimedia-Key (in Gnome: Menu->System->Preferences-> Keyboard Shortcuts
- The Standardkeys (Play, Mute, ...) should already be mapped, if not you can map them like the G-Keys

==== Slideshow ====

- Choose a folder if you start it for the first time
- Press OK to start automated slideshow
- Press UP/DOWN to change slideshow-delay (standard is 5sec, 1sec/step)

==== Simple_gb_light ====
- press one or multiple M* keys and use the scrollwheel to adjust color
- press SETTINGS to change images folder

==== xplanet ====
- takes a while to load, don't press OK till it's loaded (or go back to MENU to restart)
- when it's loaded you can play/pause with ok


=== Infos for developers ===

==== Naming convention ====

- ATM you have to name your applet file the same as your applet folder (otherwise the menu won't find it)
- ATM the name of your main-class has to be the same as your folder/filename after the last "_"
	exp. simple_slideshow: class name is slideshow; xplanet: class name is xplanet; simple_bg_light: class name is light 

==== Key-Problems ====

- Don't use the MENU-Key in your application, as it is used to terminate it.
- If you use the G- or MultimediaKeys, more than 1 action may be triggered (They may be used as gnome-shortcuts, may get fixed eventualy)


=== Changelog ===

Release 15.5.2010

** Added config file (~/.lg19/lg19.cfg) to save some stuff (gets automatically created @ first run (for every applet individually)
** Adapted some applets to use the config file
** Added folder open dialog for simple_slideshow
** Modified simple_timer to indicate selected item


------------------------ Original readmy by MultiCoreNOP--------------------------------------




=== What I want to do ===

Refactor and build an API+framework for applets.
Developers will get a simple way to create mini-programs of any kind.  An
infrastructure providing a base menu to select/activate applets and easy
possibilities to integrate into input handling will created.

So far it does not make much sense to start developing on the current code base
(as I just started to create this one week ago).  As soon as I stopped
experimenting, I'll change this file.


=== What it does right now ===

If invoked by "python main.py":

--- Color ---

By selecting M1..3 you select red/green/blue for manipulation.  Using the scroll
you can adjust the current backlight value.


--- Color ---

If no M-button is selected, scrolling will change the display brightness.


--- Xplanet ---

If you have 'xplanet' installed, you can press the "play"/"stop" buttons to
rotate the earth in your display.

(After pressing start, 360 images will be generated using as many CPUs as you
have, but nonetheless it will take up to three minutes.)

Currently I am working on supporting Qt on the display - let's see how far I
get...


=== How you can send anything you want to your G19 ===

Fire up a python shell.  The main API is logitech.g19.G19 atm:

>>> from logitech.g19 import G19

# if you get an error: lg19 = G19(True)
>>> lg19 = G19()

# setting backlight to red
>>> lg19.set_bg_color(255, 0, 0)

# fill your display with green
>>> lg19.fill_display_with_color(0, 255, 0)

# test your screen
>>> lg19.set_display_colorful()

# set backlight to blue after reset
# this will be your backlight color after a bus reset (or switching the keyboard
# off and no)
>>> lg19.save_default_bg_color(0, 0, 255)

# send an image to display
>>> data = [...] # format described in g19.py
>>> lg19.send_frame(data)

# load an arbitrary image from disk to display (will be resized non-uniform)
>>> lg19.load_image("/path/to/myimage.jpg")

# reset the keyboard via USB
>>> lg19.reset()
# now you have to rebuild the connection:
>>> lg19 = G19()


HINT: After creating a G19 object, your "light key" will not work anymore,
      because the keyboard waits for you to read its data.  You can start doing
      so by calling lg19.start_event_handling().
      (have a look at main.py)



As soon as I reach a stable point, I promise to write a lot of documentation. ;-)
