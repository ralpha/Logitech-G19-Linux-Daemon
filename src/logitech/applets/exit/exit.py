from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *

import multiprocessing
import os
import tempfile
import threading
import time

class ExitProcessor(InputProcessor):

    def __init__(self, exitrun):
        self.__exitrun = exitrun

    def process_input(self, inputEvent):
        processed = True
            
        return processed

class ExitRun(Runnable):
    '''Lists Files in the given Directory and shows them on the screen'''
    def __init__(self, lg19):
        self.__lg19 = lg19
        Runnable.__init__(self)

    def execute(self):
        pass

class exit(object):

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__exitrun = ExitRun(self.__lg19)
        self.__inputProcessor = ExitProcessor(self.__exitrun)
        self.start()
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def start(self):
        #allProcessors = self.__lg19.__keyReceiver.list_all_input_processors();
        #for process in allProcessors:
        #    if process != self:
        #        self.__lg19.remove_applet(process)
        self.__lg19.load_text("        Shutting Down...", 2,True)
        
        self.__lg19.set_text()
        self.stop();
        self.__lg19.setLastOpenApplet("None")
    
    def stop(self):
        self.__lg19.running = False;
        #self.__lg19.reset();
        pass;

if __name__ == '__main__':
    lg19 = G19()
    exit = exit(lg19)
    exit.start()
