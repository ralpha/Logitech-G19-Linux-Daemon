from logitech.g19 import *
from logitech.g19_keys import (Data, Key)
from logitech.g19_receivers import *



class brightness(object):
    '''Simple adjustment of display brightness.

    Uses scroll to adjust display brightness.

    '''

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__run = BrightnessRun(self.__lg19)
        self.__inputProcessor = BrightnessInputProcessor(self.__run)
        self.start()

    def get_input_processor(self):
        return self.__inputProcessor
    
    def stop(self):
        self.__run.stop()
        pass
        
    def start(self):
        t = threading.Thread(target=self.__run.run)
        t.start()
        pass
        
class BrightnessRun(Runnable):
    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__conf = G19Config("display")
        self.__curBrightness = self.__conf.read("brightness", 100, "int")
        self.__saved = False
        
        Runnable.__init__(self)
        
    def execute(self):
        self.__lg19.load_text("Display Brightness", 1,True, center=True, color="yellow")
        self.__lg19.load_text(str(self.__curBrightness), 3, center=True, color="red")
        if self.__saved:
            self.__lg19.load_text("Brightness saved", 5, center=True, color="green")
        self.__lg19.set_text()
        time.sleep(0.1)
    
    def setBrightness(self, value):
        self.__saved = False
        if value < 0:
            value = 0
        if value >= 100:
            value = 100
        self.__lg19.set_display_brightness(value)
        self.__curBrightness = value
    
    def changeBrightness(self, value):
        self.setBrightness(self.__curBrightness + value)
        
    def saveBrightness(self):
        self.__conf.write("brightness", self.__curBrightness)
        self.__saved = True
        
class BrightnessInputProcessor(InputProcessor):

    def __init__(self, run):
        self.__run = run

    def process_input(self, evt):
        processed = False

        if Key.SCROLL_UP in evt.keysDown:
            self.__run.changeBrightness(5)
            processed = True
        if Key.SCROLL_DOWN in evt.keysDown:
            self.__run.changeBrightness(-5)
            processed = True
        if Key.OK in evt.keysDown:
            self.__run.saveBrightness();
            processed = True
            
        return processed
        
    
