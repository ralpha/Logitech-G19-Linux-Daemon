from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *
from logitech.runnable import Runnable
from logitech.g19_config import G19Config

import multiprocessing
import os
import threading
import time
import Tkinter, tkFileDialog

class SlideshowInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, slideshowrun):
        self.__slideshowrun = slideshowrun

    def process_input(self, inputEvent):
        processed = False
        if Key.RIGHT in inputEvent.keysDown:
            try:
                self.__slideshowrun.changeI("f")
                processed = True
            except IOError:
                print "File not found+"
        if Key.LEFT in inputEvent.keysDown:
            try:
                self.__slideshowrun.changeI("r")
                processed = True
            except IOError:
                print "File not found -"
                
        if Key.UP in inputEvent.keysDown:
            try:
                self.__slideshowrun.changeDelay(1)
                processed = True
            except IOError:
                print "File not found -"
                
        if Key.DOWN in inputEvent.keysDown:
            try:
                self.__slideshowrun.changeDelay(-1)
                processed = True
            except IOError:
                print "File not found -"
                
        if Key.OK in inputEvent.keysDown:
            self.__slideshowrun.switchIsStarted()
            processed = True

            
        if Key.SETTINGS in inputEvent.keysDown:
            self.__slideshowrun.optionsMenu()
            processed = True

            
        return processed

class SlideshowRun(Runnable):
    '''Lists Files in the given Directory and shows them on the screen'''
    def __init__(self, lg19):
        Runnable.__init__(self)
        self.__ssconf = G19Config("simple_slideshow")
        self.__isStarted = True
        self.__wasStarted = True
        self.__delay = self.__ssconf.read("delay", "10", "float")
        self.__i = -1
        self.__lg19 = lg19
        self.__arrFiles = []
        self.__location = self.__ssconf.read("imagePath")
        if not os.path.isdir(self.__location):
            self.__isStarted = False
            self.__lg19.load_text("      No pictures loaded",1,True)
            self.__lg19.load_text("Press option to choose folder",2)
            self.__lg19.set_text()
            self.optionsMenu() 
        self.createList()

    def optionsMenu(self):
        root = Tkinter.Tk()
        tmp = tkFileDialog.askdirectory(parent=root,initialdir=os.path.expanduser('~/'),title='Select Images Directory')
        if not tmp == "":
            self.__location = tmp            
        root.destroy()
        self.__ssconf.write("imagePath",self.__location)
        self.createList()

    def createList(self):
        self.__arrFiles = []
        self.__i = -1
        if not self.__location == "":
            for f in os.listdir(self.__location):
                if os.path.isfile(os.path.join(self.__location, f)):
                    (rubbish, type) = os.path.splitext(f)
                    if type == ".jpg" or type == ".jpeg" or type == ".png" or type == ".gif":
                        self.__arrFiles.append(f)
                        self.__i = self.__i+1
        if self.__i < 0:
            self.__isStarted = False
            self.__lg19.load_text("      No pictures loaded",1,True)
            self.__lg19.load_text("Press option to choose folder",2)
            self.__lg19.set_text()
        else:
            self.__isStarted = self.__wasStarted
            self.changeI("f")


    def changeDelay(self, direction):
        if self.__delay >1:
            self.__delay = self.__delay + direction
        elif direction == 1:
            self.__delay = self.__delay + 1

    def execute(self):      
        if self.__isStarted:
            self.changeI("f")
        time.sleep(self.__delay)
    
    def switchIsStarted(self):
        self.__isStarted = not self.__isStarted
        self.__wasStarted = self.__isStarted

    def update(self, i):
        try:
            self.__lg19.load_image(os.path.join(self.__location, self.__arrFiles[i]))
        except IOError:            
            print "File "+ os.path.join(self.__location, self.__arrFiles[i])+" not found"
            
    def changeI(self, direction):
        if len(self.__arrFiles) != 0:
            if direction == "f":
                if self.__i < len(self.__arrFiles)-1:
                    self.__i = self.__i+1
                else:
                    self.__i = 0
                self.update(self.__i)
            if direction == "r":
                if self.__i == 0:
                    self.__i = len(self.__arrFiles)-1
                else:
                    self.__i = self.__i-1
                self.update(self.__i)
        return True

class slideshow(object):

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__slideshowrun = SlideshowRun(lg19)        
        self.__inputProcessor = SlideshowInputProcessor(self.__slideshowrun)
        self.start()
        
    def get_input_processor(self):
        return self.__inputProcessor
    
    def start(self):
        t = threading.Thread(target=self.__slideshowrun.run)
        t.start()
    

    def stop(self):
        self.__slideshowrun.stop()

if __name__ == '__main__':
    lg19 = G19()
    slideshow = slideshow(lg19)
    slideshow.start()
    try:
        while True:
            time.sleep(10)
    finally:
        slideshow.stop()