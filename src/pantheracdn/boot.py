import sys
import json
import pcdnserver

class pantheraCDN:
    """ Panthera Content Delivery Network, main class """

    # server object
    server = None
    configFile = "./config.json"
    
    def loadConfig(self):
        self.config = pantheraConfig(self.configFile)
    

    def main(self):
        self.loadConfig()
    
        self.server = pcdnserver.spawnCGIServer()
        self.server.panthera = self
        
        try:
            self.server.serve()
        except KeyboardInterrupt:
            sys.exit(0)
            
class pantheraCacheDB:
    memory = dict()
    
    
            
class pantheraConfig:
    """ Configuration manager based on JSON files """

    values = dict()
    path = ""

    def __init__(self, path):
        """ Load configuration file """
        
        self.path = path
        f = open(path, "r")
        self.values = json.loads(f.read())
        f.close()
        
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
            
