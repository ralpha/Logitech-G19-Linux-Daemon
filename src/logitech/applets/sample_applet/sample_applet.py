from logitech.g19 import *
from logitech.g19_keys import (Data, Key)
from logitech.g19_receivers import *


# this class name need to be the same as 'mainClass = <name>' in order for the menu to find it
class sampleMain(object):
    '''Simple applet.

    Uses this applet te make new applets.

    '''

    def __init__(self, lg19):
        self.__lg19 = lg19
        # TODO: change AppletRun to some other name.
        self.__run = AppletRun(self.__lg19)
        # TODO: change AppletInputProcessor to some other name.
        self.__inputProcessor = AppletInputProcessor(self.__run)
        self.start()

    def get_input_processor(self):
        return self.__inputProcessor
    
    def stop(self):
        self.__run.stop()
        
    def start(self):
        t = threading.Thread(target=self.__run.run)
        t.start()
        
# This is the main runnable for the programm and can be used to handle the display and save properties
class AppletRun(Runnable):
    def __init__(self, lg19):
        self.__lg19 = lg19
        # this can be used to save users settings
        # this is saved in plain text, so don't put sensitive data in here
        self.__conf = G19Config("sample")
        # read already stored settings, or load defualt value
        self.__name = self.__conf.read("name", "bob", "string")
        self.__saved = False
        
        Runnable.__init__(self)
        
    def execute(self):
        # this function is executed repeatedly
        # this function can be used to handle the display
        self.__lg19.load_text("This is a sample applet", 1,True, center=True, color="yellow")
        self.__lg19.load_text("You can use this to", 2, center=True, color="yellow")
        self.__lg19.load_text("make your own applet.", 3, center=True, color="yellow")
        
        
        self.__lg19.load_text("Name: " + self.__name, 5, center=True, color="white")
        if self.__saved:
            self.__lg19.load_text("Saved", 7, center=True, color="green")
        
        #redraw display
        self.__lg19.set_text()
        
        # time between refreshed (lower means faster updates, but more cpu usage)
        time.sleep(0.5)
    
    # define any functions you want
    
    def setName(self, name):
        self.__name = name;
        self.__saved = False
        
    def saveSettings(self):
        self.__conf.write("name", self.__name)
        self.__saved = True
        
# this class is used to handle input of the keyboard
class AppletInputProcessor(InputProcessor):

    def __init__(self, run):
        self.__run = run

    def process_input(self, evt):
        processed = False

        # keys for interaction
        # look in ./src/logitech/g19_keys.py for more keys
        # do not use the MENU key, this is used to close applets
        if Key.UP in evt.keysDown:
            self.__run.setName("Bob")
            processed = True
            
        if Key.DOWN in evt.keysDown:
            self.__run.setName("Jack")
            processed = True
            
        if Key.LEFT in evt.keysDown:
            self.__run.setName("Tessa")
            processed = True
            
        if Key.RIGHT in evt.keysDown:
            self.__run.setName("Michelle")
            processed = True
        
        if Key.OK in evt.keysDown:
            self.__run.saveSettings();
            processed = True
            
        return processed
        
    
