import sys
import os
import json
import pcdnserver
import signal
import tornado

class pantheraCDN:
    """ Panthera Content Delivery Network, main class """

    # server object
    server = None
    configFile = "./config.json"
    

    def main(self):
        """ Initialize app """
        
        # create home directory if doesnt exists
        if not os.path.isdir(os.path.expanduser("~/.panthera-cdn")):
            os.mkdir(os.path.expanduser("~/.panthera-cdn"))
    
        # initialize configuration and database
        self.hooking = pantheraHooking()
        self.logging = pantheraLogging(self)
        self.config = pantheraConfig(self)
        self.db = pantheraCacheDB(self)
        
        # spawn server
        self.server = pcdnserver.spawnCGIServer(port=8080, args=dict(panthera=self))
        self.server.panthera = self
        
        # handling signals
        signal.signal(signal.SIGTERM, self.server.closeServer)
        signal.signal(signal.SIGINT, self.server.closeServer)
        
        try:
            self.logging.output("Listening at 8080 port")
            self.server.serve()
        except KeyboardInterrupt:
            sys.exit(0)
            
class pantheraLogging:
    """ Panthera logging and debugging class """
    
    panthera = ""
    
    def __init__(self, panthera):
        self.panthera = panthera

    def output(self, msg, msgType=""):
        """ Output a message """
    
        print(msg)
            
            
class pantheraConfig:
    """ Configuration manager based on JSON files """

    values = dict()
    path = os.path.expanduser("~/.panthera-cdn/config")
    createNewFile = True # create new file if doesnt exists
    panthera = ""

    def __init__(self, panthera):
        """ Load configuration file """
        
        self.panthera = panthera
        
        # save configuration on server exit
        self.panthera.hooking.add_option('server.exit', self.save)
        
        # check if file exists and create it (if self.createNewFile == True)
        if not os.path.isfile(self.path):
            if self.createNewFile == True:
                f = open(self.path, "w")
                f.write("")
                f.close()
            else:
                print("Fatal error: "+self.path+" does not exists")
                sys.exit(1)
        
        try:
            f = open(self.path, "r")
            self.values = json.loads(f.read())
            f.close()
        except ValueError:
            self.values = {} # create new dict if there isnt any
        
    def getKey(self, key):
        """ Get key from configuration storage """
        
        if key in self.values:
            return key
            
        return None
        
    def keyExists(self, key):
        """ Check if key exists """
    
        return key in self.values
        
    def setKey(self, key):
        """ Set configuration key """
    
        self.values[key] = key
        return True
        
    def save(self, a=''):
        """ Save configuration file """
        
        self.panthera.logging.output("Saving "+self.path, 'pantheraConfig')
    
        f = open(self.path, "w")
        f.write(json.dumps(self.values, indent=4))
        f.close()
        return True
            
            
class pantheraCacheDB(pantheraConfig):
    """ Extended pantheraConfig class, provides simple cache management """

    path = os.path.expanduser("~/.panthera-cdn/config")
    
    def getFile(key):
        """ Get file contents from cache """
    
        if self.keyExists(key):
            f = open(self.getKey(key), "r")
            c = f.read()
            f.close()
            
            return c
            
        return None
        
class pantheraHooking:
    """ Simple hooking class """

    memory = dict()
    
    def add_option(self, name, callback):
        """ Add a callback """
    
        if not name in self.memory:
            self.memory[name] = list()
            
        self.memory[name].append(callback)
    
    def get_options(self, name, data=""):
        """ Execute hooks """
       
        # check if any hooks defined
        if not name in self.memory:
            return data
            
        for hook in self.memory[name]:
            data = hook(data)
            
        return data
