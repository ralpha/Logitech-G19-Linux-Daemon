from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *

import multiprocessing
import os
import tempfile
import threading
import time

class TimerInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, timerrun):
        self.__timerrun = timerrun

    def process_input(self, evt):
        processed = False
        if Key.OK in evt.keysDown:
            if self.__timerrun.get_isRunning():
                self.__timerrun.set_isRunning(False)
            else:
                self.__timerrun.set_isRunning(True)

            processed = True
        if Key.SETTINGS in evt.keysDown:
            self.__timerrun.reset();
            processed = True
        if not self.__timerrun.get_isRunning():
            if Key.UP in evt.keysDown:
                self.__timerrun.changeSelected(1)
                processed = True
            
            if Key.DOWN in evt.keysDown:
                self.__timerrun.changeSelected(-1)
                processed = True
            
            if Key.LEFT in evt.keysDown:
                self.__timerrun.changeSelection(-1)
                processed = True
            
            if Key.RIGHT in evt.keysDown:
                self.__timerrun.changeSelection(1)
                processed = True
            
        return processed

class TimerRun(Runnable):
    '''Lists Files in the given Directory and shows them on the screen'''
    def __init__(self, lg19, timer):
        self.__lg19 = lg19
        self.__hours = 0
        self.__minutes = 0
        self.__i = 3
        self.__seconds = 0
        self.__isRunning = False
        self.__timer = timer
        self.__blink = False
        self.__selection = 1
        self.__finished = False
        Runnable.__init__(self)

    def execute(self):
        if self.__isRunning and not self.__finished:
            self.changeSeconds(-1)
        if self.__isRunning:
            self.__time = "%02d:%02d:%02d" % (self.__hours, self.__minutes, self.__seconds)
            if self.__finished:
                # TODO os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 400))
                if self.__i > 1:
                  self.__i = 0
                  self.__lg19.load_text(self.__time,4, center=True, color="red")
                else:
                  self.__i += 1;
                  self.__lg19.load_text(self.__time,4, center=True, color="white")
            else:
                self.__lg19.load_text(self.__time,4, center=True)
            self.__lg19.set_text()
            time.sleep(1)
        else:
            self.__time = "%02d:%02d:%02d" % (self.__hours, self.__minutes, self.__seconds)
            
            if self.__selection == 1:
                if self.__i > 3:
                    self.__time = "__:%02d:%02d" % (self.__minutes, self.__seconds)
                    self.__i = 0
                else:
                    self.__i += 1
            if self.__selection == 2:
                if self.__i > 3:
                    self.__time = "%02d:__:%02d" % (self.__hours, self.__seconds)
                    self.__i = 0
                else:
                    self.__i += 1
            if self.__selection == 3:
                if self.__i > 3:
                    self.__time = "%02d:%02d:__" % (self.__hours, self.__minutes)
                    self.__i = 0
                else:
                    self.__i += 1
            
            self.__lg19.load_text(self.__time,4, center=True)
            self.__lg19.set_text()
            time.sleep(0.1)
    
    def changeSelected(self, direction):
        self.__i = 5
        if self.__selection == 1:
            self.changeHours(direction)
        if self.__selection == 2:
            self.changeMinutes(direction)
        if self.__selection == 3:
            self.changeSeconds(direction)

    def set_isRunning(self, isRunning):
        self.__isRunning = isRunning
    
    def get_isRunning(self):
        return self.__isRunning
        
    def reset(self):
        self.__isRunning = False
        self.__selection = 1
        self.__finished = False
        
    def changeHours(self, direction):
        if self.__isRunning:
            if self.__hours > 0:
                self.__hours += direction
        else:
            if self.__hours == 0 and direction == -1:
                self.__hours = 99
            elif self.__hours == 99 and direction == 1:
                self.__hours = 0
            else:
                self.__hours += direction
        
    def changeMinutes(self,direction):
        if self.__isRunning:
            if self.__minutes > 0:
                self.__minutes += direction
            else:
                if self.__hours == 0:
                    self.__minutes = 0
                else:
                    self.__minutes = 59
                    self.changeHours(-1)
        else:
            if self.__minutes == 0 and direction == -1:
                self.__minutes = 59
            elif self.__minutes == 59 and direction == 1:
                self.__minutes = 0
            else:
                self.__minutes += direction

    def changeSeconds(self, direction):
        if self.__isRunning:
            if self.__seconds > 0:
                self.__seconds += direction
            else:
                if self.__minutes == 0 and self.__hours == 0:
                    self.__seconds = 0
                    self.__finished = True
                    #self.__timer.stop()
                else:
                    self.__seconds = 59
                    self.changeMinutes(-1)
        else:
            if self.__seconds == 0 and direction == -1:
                self.__seconds = 59
            elif self.__seconds == 59 and direction == 1:
                self.__seconds = 0
            else:
                self.__seconds += direction
    
    def changeSelection(self, direction):
        self.__i = 5
        if self.__selection == 3 and direction == 1:
            self.__selection = 1
        elif self.__selection == 1 and direction == -1:
            self.__selection = 3
        else:
            self.__selection += direction

class timer(object):

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__lg19.load_text("Timer",1,True, center=True, color="yellow")
        self.__lg19.load_text("Use Arrows to set time",2, center=True)
        
        lg19.set_text()
        self.__timerrun = TimerRun(self.__lg19, self)
        self.__inputProcessor = TimerInputProcessor(self.__timerrun)
        self.start()
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def start(self):
        t = threading.Thread(target=self.__timerrun.run)
        t.start()
    
    def stop(self):
        self.__timerrun.stop()

