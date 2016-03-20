from g19_receivers import G19Receiver
from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *
import ConfigParser

import os

class G19Menu(object):
    def __init__(self, lg19):
        self.__applet_dir = "logitech/applets/"
        self.__lg19 = lg19
        self.__applets = []
        self.__menuOnly = False
        self.__firstItem = 1
        self.__selectedItem = 1
        self.__selection = 1
        self.__inputProcessor = MenuInputProcessor(self)
        self.loadApplets();
        self.showMenu(self.__applets)
        
    def loadApplets(self):
        try:
            for f in os.listdir(self.__applet_dir):
                validApplet = True
                appletPath = os.path.join(self.__applet_dir, f);
                
                applet = G19Applet()
                
                if not os.path.isdir(appletPath):
                    validApplet = False
                else:
                    applet.loadConfig(f)
                
                if validApplet:
                    self.__applets.append(applet)
        except:
            print "IO Exception"
    
    def startApplet(self, appletName):
        g19 = self.__lg19        
        try:
            applet = G19Applet()
            applet.loadConfig(appletName)
            
            #do before starting app
            g19.setLastOpenApplet(applet.getName())
            
            self.__menuOnly = True
            self.__selectedApplet = applet.start(g19)
        finally:
            pass
        return True
    
    def getMenuOnly(self):
        return self.__menuOnly
    
    def changeSelection(self, direction):
        if direction == -1:
            if self.__selectedItem > 1:
                self.__selectedItem -= 1
            if self.__selection > 0:
                self.__selection += direction

        if direction == 1:
            if self.__selectedItem < len(self.__applets):
                 self.__selectedItem = self.__selectedItem + 1
                 self.__selection += direction

        self.showMenu(self.__applets)
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def startSelected(self):
        g19 = self.__lg19        
        try:
            applet = self.__applets[self.__selection]
            
            #do before starting app
            g19.setLastOpenApplet(applet.getName())
            
            self.__menuOnly = True
            self.__selectedApplet = applet.start(g19)
        finally:
            pass

    def stopSelected(self):
        if self.__menuOnly == True:
            try:
                self.__selectedApplet.stop()
            finally:
                self.__lg19.remove_applet(self.__selectedApplet)
                self.__menuOnly = False
                self.__lg19.setLastOpenApplet("None")
        self.showMenu(self.__applets)
        
    def quitApplets(self):
        if self.__menuOnly == True:
            try:
                self.__selectedApplet.stop()
            finally:
                self.__lg19.remove_applet(self.__selectedApplet)
                self.__menuOnly = False
        
    def showMenu(self, menuEntries):
        i = 1
        if self.__selection+1 > self.__firstItem+6:
            if self.__firstItem+6 < len(menuEntries):
                self.__firstItem +=1
            self.__selectedItem = 7
        if self.__selection+1 < self.__firstItem:
            self.__firstItem -=1
            self.__selectedItem = 1
        self.__lg19.clear_text()
        for j in range(self.__firstItem, self.__firstItem+7):
            if j <= len(menuEntries):
                if i == self.__selectedItem:
                    self.__lg19.load_text("-> "+menuEntries[j-1].getDisplayName(), i, color=menuEntries[j-1].getHighlightColor())
                    self.__selection = j-1
                else:
                    self.__lg19.load_text(menuEntries[j-1].getDisplayName(), i, color=menuEntries[j-1].getColor())
                i = i+1

        self.__lg19.set_text()

class MenuInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, menu):
        self.__menu = menu

    def process_input(self, inputEvent):
        processed = False
        if not self.__menu.getMenuOnly():
            if Key.UP in inputEvent.keysDown:
                self.__menu.changeSelection(-1)
                processed = True
        
            if Key.DOWN in inputEvent.keysDown:
                self.__menu.changeSelection(1)
                processed = True
            
            if Key.OK in inputEvent.keysDown:
                self.__menu.startSelected()
        
        if Key.MENU in inputEvent.keysDown:
            self.__menu.stopSelected()                

        return processed
    
class G19Applet(object):

    def __init__(self):
        self.__applet_dir = "logitech/applets/"
        self.__appletConfig = "config.cfg"
        self.__section = 'Applet'
        self.__name = "";
        self.__displayName = "";
        self.__path = None;
        self.__mainclass = None;
        self.__color = "white";
        self.__highlightColor = "white";
        
    def define(self, name, displayName, path, mainclass):
        self.__name = name;
        self.__displayName = displayName;
        self.__path = path;
        self.__mainClass = mainClass;
    
    def getName(self):
        return self.__name;
        
    def getDisplayName(self):
        return self.__displayName;
    
    def getPath(self):
        return self.__path;
        
    def getMainClass(self):
        return self.__mainClass;
        
    def getColor(self):
        return self.__color;
        
    def getHighlightColor(self):
        return self.__highlightColor;
        
    def saveConfig(self):
        if path != None:
            appletConfig = os.path.join(path, self.__appletConfig);
            config = ConfigParser.RawConfigParser()
            config.add_section(self.__section)
            config.set(self.__section, 'mainClass', self.__mainClass)
            config.set(self.__section, 'displayName', self.__displayName)
            config.set(self.__section, 'name', self.__name)
            config.set(self.__section, 'color', self.__color)
            config.set(self.__section, 'highlightColor', self.__highlightColor)
            
            with open(appletConfig, 'wb') as configfile:
                config.write(configfile)
            
    def loadConfig(self, name):
        appletPath = os.path.join(self.__applet_dir, name);
        appletConfig = os.path.join(appletPath, self.__appletConfig);
        
        if not os.path.isfile(appletConfig):
            print "Applet {} had no config".format(f)
            self.saveConfig()
            print "config created."
        
        defaults = {'color': "white", 'highlightColor': "white" }
        
        config = ConfigParser.RawConfigParser(defaults = defaults)
        config.read(appletConfig)
        self.__name = config.get(self.__section, 'name')
        self.__displayName = config.get(self.__section, 'displayName')
        self.__path = appletPath
        self.__mainClass = config.get(self.__section, 'mainClass')
        self.__color = config.get(self.__section, 'color')
        self.__highlightColor = config.get(self.__section, 'highlightColor')
        
    def start(self, g19):
        exec 'from logitech.applets.' + self.__name + '.' + self.__name + ' import '+ self.__mainClass
        #TODO
        exec 'selectedApplet ='+ self.__mainClass+'(g19)'
        
        g19.add_applet(selectedApplet)
        return selectedApplet
    
