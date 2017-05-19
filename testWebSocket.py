# This is a simple WebSocket echo server
# I took from this repo from https://github.com/dpallot/simple-websocket-server

# I was using built-in python 2.7, Ubuntu 14.04
# Just run this installation line:
# sudo pip install git+https://github.com/dpallot/simple-websocket-server.git

# And then run the GUI.html to see the test result :)

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from pymongo import MongoClient
import mongodb # DB API
from tornado import ioloop
import datetime
from tornado import gen

class SimpleEcho(WebSocket):

	def handleMessage(client):
		parameters = client.data.split('|')
		command = parameters[0]

		print(client.data);
		
		if command == 'store':
			packageName = parameters[1]
			tempMin = parameters[2]
			tempMax = parameters[3]
			lightMin = parameters[4]
			lightMax = parameters[5]
			print "getting Slot from DB"
			ioloop.IOLoop.current().run_sync(getDocument("slot", { "temperature" : {"$in" : [tempMin,tempMax]} , "lightSensitivity" : {"$in" : [lightMin,lightMax]}}))
			#slotfromDB = 
			#print slot

			client.sendMessage(u'Found a slot for ' + packageName)
			client.sendMessage(packageName + u' is queued for storing. Please be informed');

		elif command == 'retrieve':
			packageId = parameters[1]
			client.sendMessage(u'Package ' + packageId + ' is queued for delivery to the gate. Please be informed');


	def handleConnected(client):
		print(client.address, 'connected')

	def handleClose(client):
		print(client.address, 'closed')

def my_callback():
	#print('result %s' % repr(result.inserted_id))
	ioloop.IOLoop.current().stop()

@gen.coroutine
def main():
	#mc_client = motor_tornado.MotorClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
	#db = mc_client.gspd
	#slot = db.slot

	#io_loop = ioloop.IOLoop.current()
	#io_loop.add_timeout(datetime.timedelta(seconds=5),callback=my_callback)
	#callback = functools.partial(connection_ready, sock)
	#io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
	#io_loop.start()

	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	server.serveforever()

if __name__ == '__main__':
	ioloop.IOLoop.current().run_sync(main)