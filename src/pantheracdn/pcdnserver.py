import tornado.ioloop
import tornado.web

class pcdnSocketServer(tornado.web.Application):
    def serve(self):
        tornado.ioloop.IOLoop.instance().start()
        
    def closeServer(self, sig, frame):
        self.panthera.logging.output("Shutting down...", "server")
        
        # execute all hooked functions to save data
        self.panthera.hooking.get_options("server.exit")
        
        # exit application
        tornado.ioloop.IOLoop.instance().stop()
    
class pcdnRequestHandler(tornado.web.RequestHandler):
    """ Panthera CDN request handler """
    
    def initialize(self, panthera):
        self.panthera = panthera

    def preRequest(self):
        pass

    #@tornado.web.asynchronous
    def get(self, path):
        """ Handle GET request """
        
        # server normal files
            
class pcdnStorageHandler(tornado.web.RequestHandler):
    def initialize(self, panthera):
        self.panthera = panthera

    def get(self, path):
        """ Handle manual added files to #storage """
        
        if not self.panthera.db.keyExists(path):
            self.send_error(404)
            return ""
            
        
            
             
        
        
    
    
def spawnCGIServer(port=8080, args=""):
    """ Create new instance of CGI server """
    application = pcdnSocketServer([
        (r"/storage/(.*)", pcdnStorageHandler, args),
        (r"/(.*)", pcdnRequestHandler, args)
    ])
    application.listen(port)
    
    return application
