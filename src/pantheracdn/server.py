import SocketServer
import BaseHTTPServer
import CGIHTTPServer

class ThreadingCGIServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass
