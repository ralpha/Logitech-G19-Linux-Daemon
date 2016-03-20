#!/usr/bin/python

from logitech.g19 import G19
from logitech.g19_menu import G19Menu
#from logitech.applets.xplanet.xplanet import xplanet

import time

if __name__ == '__main__':
    lg19 = G19(False)
    lg19.start_event_handling()
    menu = None
    try:
        menu = G19Menu(lg19)

        if lg19.lastOpenApplet == "None":
          lg19.add_applet(menu)
        else:
          lg19.add_applet(menu)
          result = menu.startApplet(lg19.lastOpenApplet)
          if not result:
              pass
              #lg19.add_applet(menu)

        while lg19.running:
            time.sleep(5)
    except KeyboardInterrupt:
        lg19.running = False
        if menu != None:
            menu.quitApplets()
        
    finally:
        lg19.stop_event_handling()
        lg19.reset()
