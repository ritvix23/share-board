#various handlers



from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler 


#the following class handles the HTTP connection
class IndexView(RequestHandler):


	def get(self):
		self.render('website.html')				#website that would be rendered to the client



#the following class handles websocket connection
class WebSocket(WebSocketHandler):
	connections = {}               	#Dict that stores all connected clients with key as client id.
	last_client_id = 1				
	state = 'Hello'    				#Message that the client would recieve when connected. introduced from perspective of multiplayer games.
 
	def initialize(self):
		self.id = self.assign_id()


	#this method is triggered when connection is estabilished to a client.
	def open(self):
		self.write_message('Connection Estabilished to Server')			 #sends a confirmatory message to client
		self.add_to_connections()   
		print("connected to a new client")   
		self.send_state()				#comment this if you dont want to send state.
		


	#this method is triggered whenever server recieves a message from the client.
	def on_message(self, message):
		self.write_to_all(message)      	#message is echoed back to all connected clients

	#this method is triggered when connection to the client is closed-
	def on_close(self):
		print('Connection Closed')
		self.remove_from_connections()				

	# assigns unique id to each client upon connection-
	def assign_id(self):				
		new_id = WebSocket.last_client_id + 1
		WebSocket.last_client_id +=1
		return new_id

	#adds the client to dict of connected clients-
	def add_to_connections(self):			
		self.connections[self.id] = self

	#remove client from dict connections if client got disconnected-
	def remove_from_connections(self):
		del self.connections[self.id]

	#if an initial message/state is to be sent to the client upon connection-
	def send_state(self):
		self.write_message(self.state)

	# forwards recieved message to all the connected clients, including the client which sent it.
	@classmethod
	def write_to_all(cls, message):
		for key, value in cls.connections.items():
			value.write_message(message)



