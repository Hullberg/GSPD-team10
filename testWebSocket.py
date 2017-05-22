# This is a simple WebSocket echo server
# I took from this repo from https://github.com/dpallot/simple-websocket-server

# I was using built-in python 2.7, Ubuntu 14.04
# Just run this installation line:
# sudo pip install git+https://github.com/dpallot/simple-websocket-server.git

# And then run the GUI.html to see the test result :)

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from pymongo import MongoClient
#import mongodb # DB API
import asyncdb
from tornado import ioloop, gen

class SimpleEcho(WebSocket):

	@gen.coroutine
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
			

			client.sendMessage(u'Found a slot for ' + packageName)
			client.sendMessage(packageName + u' is queued for storing. Please be informed');

			print "getting Slot from DB"
			# The line below is where it gets stuck... :(
			res = yield asyncdb.getSlot({"itemID" : ""})
			print res

		elif command == 'retrieve':
			packageId = parameters[1]
			client.sendMessage(u'Package ' + packageId + ' is queued for delivery to the gate. Please be informed');


	def handleConnected(client):
		print(client.address, 'connected')

	def handleClose(client):
		print(client.address, 'closed')



@gen.coroutine
def main():
	# Mongo-variables imported

	print "Started main"
	

if __name__ == '__main__':
	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	ioloop.IOLoop.instance().run_sync(main)
	server.serveforever()