# This is a simple WebSocket echo server
# I took from this repo from https://github.com/dpallot/simple-websocket-server

# I was using built-in python 2.7, Ubuntu 14.04
# Just run this installation line:
# sudo pip install git+https://github.com/dpallot/simple-websocket-server.git

# And then run the GUI.html to see the test result :)

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from motor import motor_tornado
from tornado import ioloop, gen
from tornado.ioloop import IOLoop
import time
from bson.objectid import ObjectId

mc_client = motor_tornado.MotorClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
db = mc_client.gspd

class SimpleEcho(WebSocket):

	def handleMessage(client):
		parameters = client.data.split('|')
		command = parameters[0]

		print(client.data);
		
		if command == 'store':
			packageName = str(parameters[1])
			tempMin = int(parameters[2])
			tempMax = int(parameters[3])
			lightMin = int(parameters[4])
			lightMax = int(parameters[5])
			
			
			client.sendMessage(u'Found a slot for ' + packageName)
			client.sendMessage(packageName + u' is queued for storing. Please be informed');

			simpleQuery = { "lightSensitivity" : {"$lte" : lightMax}, "lightSensitivity" : {"$gte" : lightMin}, "temperature" : {"$lte" : tempMax}, "temperature" : {"$gte" : tempMin}}

			# # #
			# TODO : MUST SEND parameters[1:5] TO CALLBACK
			# # #
			db.slot.find_one(simpleQuery, callback=storeGetSlotDone)
			
			ioloop.IOLoop.current().start() # Goes to storeGetSlotDone when finished


		elif command == 'retrieve':
			packageId = parameters[1]
			client.sendMessage(u'Package ' + packageId + ' is queued for delivery to the gate. Please be informed');

			retrieveQuery = { "_id" : packageId }

			db.item.find_one(retrieveQuery, callback=retrieveGetItemDone)
			ioloop.IOLoop.current().start()


	def handleConnected(client):
		print(client.address, 'connected')

	def handleClose(client):
		print(client.address, 'closed')
		
# # #
# MARK - Storing an item, callback functions following each other, in order
# # #
def storeGetSlotDone(result,error):
	print('Slot info is now ready')
	print('result %s error %s' % (repr(result), repr(error)))
	slotID = repr(result['_id'])
	xCoord = int(repr(result['xCoord']))
	yCoord = int(repr(result['yCoord']))
	#packageName = ??
	#tempMin = ??
	#tempMax = ??
	#lightMin = ??
	#lightMax = ??
	# We also need the packageName, tempMin, tempMax, lightMin and lightMax of the item..
	
	postItemQuery = { "itemName" : "test", "xCoord" : xCoord, "yCoord" : yCoord, "tempMin" : 5, "tempMax" : 10, "lightMin" : 700, "lightMax" : 800, "itemTaken" : True, "robotID" : None, "slotID" : slotID}
	db.item.insert_one(postItemQuery, callback=storePostItemDone) # Continues to postItemDone

def storePostItemDone(result,error):
	print('Item inserted')
	print('result %s error %s' % (repr(result), repr(error)))
	itemID = repr(result.inserted_id) 
	# Need the slotID from inserted item
	# slotID = ?? 

	db.slot.update({ "_id" : ObjectId('591442da81aa9d5700e68cdb') }, {"$set" : {"itemID" : itemID} }, callback=storeUpdateSlotDone) # Continues to updateSlotDone


def storeUpdateSlotDone(result,error):
	print('Slot updated')
	print('result %s error %s' % (repr(result), repr(error)))

	ioloop.IOLoop.current().stop() # Update robot and send task to robot 

# # #
# MARK - Retrieving an item, callbacks in order
# # #
def retrieveGetItemDone(result,error):
	print('Item found')
	print('result %s error %s' % (repr(result), repr(error)))

	itemToRetrieve = repr(result) # The entire item-document
	slotID = str(itemToRetrieve['slotID'])
	#TODO
	db.item.update(({ "_id" : str(itemToRetrieve["_id"]) }, { "$set" : { "" }}))



# # #
# MARK - Robot interaction
# # #

# TODO: A robot finishes task, (delete) item, update necessary fields


if __name__ == '__main__':
	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	server.serveforever()