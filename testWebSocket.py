# This is a simple WebSocket echo server
# I took from this repo from https://github.com/dpallot/simple-websocket-server

# I was using built-in python 2.7, Ubuntu 14.04
# Just run this installation line:
# sudo pip install git+https://github.com/dpallot/simple-websocket-server.git

# And then run the GUI.html to see the test result :)

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from pymongo import MongoClient
#import mongodb # DB API
# import asyncdb
from tornado import ioloop, gen
import time

mc_client = motor_tornado.MotorClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
db = mc_client.gspd

class SimpleEcho(WebSocket):

	# @gen.coroutine
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

			# gte = greater than or equal to
			# lte = lesser than or equal to
			simpleQuery = { "lightSensitivity" : {"$lt" : 800}, "lightSensitivity" : {"$gt" : 700} };

			db.find_one(simpleQuery, getSlotDone)

			# Post the item
			# newItem = [packageName, gotten[1], gotten[2], tempMin, tempMax, lightMin, lightMax, False, None, result[0]]
			# posted = asyncdb.postItem(newItem)

			# Update slot to slotTaken = True, and itemID. (posted is the ID of the newly inserted item)
			# gotten[3] = True
			# gotten[6] = posted
			# ioloop.IOLoop.current().stop()
			# updated = asyncdb.updateSlot(gotten[0], gotten[1:6])
			# updated == 1 => successful

			ioloop.IOLoop.current().start()



		elif command == 'retrieve':
			packageId = parameters[1]
			client.sendMessage(u'Package ' + packageId + ' is queued for delivery to the gate. Please be informed');

			# get item and slot info
			ioloop.IOLoop.current.start()
			itemToGet = asyncdb.getItem({ "_id" : packageId})
			ioloop.IOLoop.current.stop()
			slotToGet = asyncdb.getItem({ "_id" : itemToGet[10]})
			ioloop.IOLoop.current.stop()


	def getSlotDone(result, error):
		print('Slot info is now ready')
		print('result %s error %s' % (repr(result), repr(error)))
		IOLoop.current().stop()


	def handleConnected(client):
		print(client.address, 'connected')

	def handleClose(client):
		print(client.address, 'closed')



# @gen.coroutine
def main():
	# Mongo-variables imported


if __name__ == '__main__':
	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	ioloop.IOLoop.instance().run_sync(main)
	server.serveforever()