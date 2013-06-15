import tornado.ioloop
import tornado.web

class pcdnSocketServer(tornado.web.Application):
    def serve(self):
        tornado.ioloop.IOLoop.instance().start()
    
class pcdnRequestHandler(tornado.web.RequestHandler):
    """ Panthera CDN request handler """

    def preRequest(self):
        pass

    def getHeader(self, header):
        """ Parse RAW headers """
        
        if header in self.headers:
            return self.headers[header]


    @tornado.web.asynchronous
    def get(self):
        """ Handle GET request """
        self.preRequest()  

        self.write("Hello, world")        
        return ""
    
    
def spawnCGIServer(port=8080):
    """ Create new instance of CGI server """
    application = pcdnSocketServer([
        (r"/", pcdnRequestHandler),
    ])
    application.listen(port)
    
    return application
