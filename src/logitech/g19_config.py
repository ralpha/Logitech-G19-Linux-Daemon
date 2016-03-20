import ConfigParser
import os

class G19Config(object):

    def __init__(self, section):
        self.__configFile = os.path.expanduser('~/.lg19/lg19.cfg')
        self.__section = section
        self.__config = ConfigParser.RawConfigParser()
        if not os.path.isdir(os.path.expanduser('~/.lg19/')):
            os.mkdir(os.path.expanduser('~/.lg19/'))
        if not os.path.isfile(self.__configFile):
            fd = open(self.__configFile, "w")
            fd.close()
        self.__config.read(self.__configFile)
        if not self.__config.has_section(self.__section):
            self.__config.add_section(self.__section)

    
    def write(self, key, value):        
        

        self.__config.set(self.__section, key, value)
        
        
        self.__config.write(open(self.__configFile, "wb"))
    
    def read(self, key, default="", type="string"):
        '''Returns the config value of key.
            
            If key does not exist, it will create key with value default=""

            If you need a specific type you can set one of (float, int) as 3th
            argument, nothing or string will return a string value

        '''
        
        self.__config.read(self.__configFile)
        if not self.__config.has_option(self.__section, key):
            self.write(key, default)
        if type == "string":
            return self.__config.get(self.__section, key)
        if type == "float":
            return self.__config.getfloat(self.__section, key)
        if type == "int":
            return self.__config.getint(self.__section, key)

        