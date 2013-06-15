import sys
import os
import json
import pcdnserver

class pantheraCDN:
    """ Panthera Content Delivery Network, main class """

    # server object
    server = None
    configFile = "./config.json"
    

    def main(self):
        # create home directory if doesnt exists
        if not os.path.isdir(os.path.expanduser("~/.panthera-cdn")):
            os.mkdir(os.path.expanduser("~/.panthera-cdn"))
    
        self.config = pantheraConfig(self.configFile)
        self.db = pantheraCacheDB(self)
    
        self.server = pcdnserver.spawnCGIServer()
        self.server.panthera = self
        
        try:
            self.server.serve()
        except KeyboardInterrupt:
            sys.exit(0)
            
            
class pantheraConfig:
    """ Configuration manager based on JSON files """

    values = dict()
    path = os.path.expanduser("~/.panthera-cdn/config")
    createNewFile = True # create new file if doesnt exists

    def __init__(self, path):
        """ Load configuration file """
        
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
        
    def setKey(self, key):
        """ Set configuration key """
    
        self.values[key] = key
        return True
        
    def save(self):
        """ Save configuration file """
    
        f = open(self.path, "w")
        f.write(json.dumps(self.values, indent=4))
        f.close()
        return True
            
            
class pantheraCacheDB(pantheraConfig):
    path = os.path.expanduser("~/.panthera-cdn/config")
