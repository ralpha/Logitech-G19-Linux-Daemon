from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *

import multiprocessing
import os
import tempfile
import threading
import time

class ClockInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, clockrun):
        self.__clockrun = clockrun

    def process_input(self, inputEvent):
        processed = True
            
        return processed

class ClockRun(Runnable):
    '''Lists Files in the given Directory and shows them on the screen'''
    def __init__(self, lg19):
        self.__lg19 = lg19
        Runnable.__init__(self)

    def execute(self):
        self.__lg19.load_text(time.strftime("%d %b %Y", time.localtime()), 2,True, center=True)      
        self.__lg19.load_text(time.strftime("%H:%M:%S", time.localtime()), 4, center=True)
        
        self.__lg19.set_text()
        time.sleep(0.1)

class clock(object):

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__clockrun = ClockRun(self.__lg19)
        self.__inputProcessor = ClockInputProcessor(self.__clockrun)
        self.start()
                
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def start(self):
        t = threading.Thread(target=self.__clockrun.run)
        t.start()
    
    def stop(self):
        self.__clockrun.stop()
