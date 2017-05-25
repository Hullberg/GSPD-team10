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
from functools import partial

mc_client = motor_tornado.MotorClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
db = mc_client.gspd


# # #
# MARK - Websocket interaction with client
# # #
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
			parameters = [packageName, tempMin, tempMax, lightMin, lightMax]
			callback_function = partial(storeGetSlotDone,parameters)
			db.slot.find_one(simpleQuery, callback=callback_function)
			
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
def storeGetSlotDone(parameters, result, error):
	print('Slot info is now ready')
	print('result %s error %s' % (repr(result), repr(error)))
	temp = repr(result['_id']).split("'")[1]
	slotID = ObjectId(temp)
	print slotID
	xCoord = int(repr(result['xCoord']))
	yCoord = int(repr(result['yCoord']))
	packageName = parameters[0]
	tempMin = parameters[1]
	tempMax = parameters[2]
	lightMin = parameters[3]
	lightMax = parameters[4]
	
	postItemQuery = { "itemName" : packageName, "xCoord" : xCoord, "yCoord" : yCoord, "tempMin" : tempMin, "tempMax" : tempMax, "lightMin" : lightMin, "lightMax" : lightMax, "itemTaken" : True, "robotID" : None, "slotID" : slotID}
	callback_function = partial(storePostItemDone, slotID)
	db.item.insert_one(postItemQuery, callback=callback_function) # Continues to postItemDone


def storePostItemDone(parameters, result, error):
	print('Item inserted')
	print('result %s error %s' % (repr(result), repr(error)))
	temp = repr(result.inserted_id).split("'")[1]
	itemID = ObjectId(temp)
	print('itemID %s' % itemID)
	print('slotID %s' % parameters)
	slotID = parameters

	callback_function = partial(storeUpdateSlotDone,itemID)
	db.slot.update({ '_id' : slotID }, {"$set" : {"itemID" : itemID, "slotTaken" : True }}, callback=callback_function) # Continues to updateSlotDone


def storeUpdateSlotDone(parameters, result, error):
	print('Slot updated')
	print('result %s error %s' % (repr(result), repr(error)))
	print('itemID %s ' % parameters)

	# We also want to get a robot to do the work. So find a robot that is free and assign the item to it.
	# pass itemID to robot creator
	callback_function = partial(storeFindRobotDone, parameters)
	# Send it to a robot that is marked as available (and online [state])
	db.robot.find_one({"state" : True, "robotTaken" : False}, callback=callback_function)
	

def storeFindRobotDone(parameters, result, error):
	print('Found robot')
	print('result %s error %s' % (repr(result), repr(error)))
	temp = repr(result['_id']).split("'")[1]
	robotID = ObjectId(temp)
	params = [parameters, robotID]
	# Keep sending itemID
	callback_function = partial(storeUpdateRobotDone, params)
	db.robot.update({ '_id' : robotID }, {"$set" : {"robotTaken" : True, "itemID" : parameters}}, callback=callback_function)
	
def storeUpdateRobotDone(parameters, result, error):
	print('Robot updated')
	print('result %s error %s' % (repr(result), repr(error)))
	print parameters
	#Update the item, then we're done.
	# Find item with params[0], set it's robotID to params[1]

	callback_function = partial(storeUpdateItemDone, parameters)
	db.item.update({ '_id' : parameters[0] }, {"$set" : {"robotID" : parameters[1]}}, callback=callback_function)

def storeUpdateItemDone(parameters, result, error):
	print('Item updated')
	print('result %s error %s' % (repr(result), repr(error)))
	print('Everything went nice')
	ioloop.IOLoop.current().stop()


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

# # #
# MARK - Main
# # #
if __name__ == '__main__':
	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	server.serveforever()