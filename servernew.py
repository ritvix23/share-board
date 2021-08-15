from tornado.web import Application
from tornado.options import options, define
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from handlers import WebSocket, IndexView
import os

define('port', default='8888')   # define port attribute of options object(port at which websocket is estabilished)
APP_DIR = os.path.dirname(os.path.realpath(__file__))

settings = {
    "static_path": os.path.join(APP_DIR, "static")            #to server static files
}



#http handler at localhost:8888/ and websocket handler at localhost:8888/ws
app = Application([
	('/', IndexView),					#(uri of homepage, http handler). 
	(r'/ws', WebSocket)					#(uri of websocket, websocket handler)
	], **settings)


if __name__=='__main__':
	http_server = HTTPServer(app)
	http_server.listen(options.port)  #listen to the given port for requests.
	IOLoop.current().start()		#start the input/output loop for asynchronous operation
