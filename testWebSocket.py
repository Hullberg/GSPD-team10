# This is a simple WebSocket echo server
# I took from this repo from https://github.com/dpallot/simple-websocket-server

# I was using built-in python 2.7, Ubuntu 14.04
# Just run this installation line:
# sudo pip install git+https://github.com/dpallot/simple-websocket-server.git

# And then run the GUI.html to see the test result :)

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
# from pymongo import MongoClient
#import mongodb # DB API
# import asyncdb
from motor import motor_tornado
from tornado import ioloop, gen
from tornado.ioloop import IOLoop
import time
from motor import motor_tornado
import pprint

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
			tempMin = int(parameters[2])
			tempMax = int(parameters[3])
			lightMin = int(parameters[4])
			lightMax = int(parameters[5])
			# pprint(tempMin)
			# pprint(tempMax)
			# pprint(lightMin)
			# pprint(lightMax)
			
			
			client.sendMessage(u'Found a slot for ' + packageName)
			client.sendMessage(packageName + u' is queued for storing. Please be informed');

			# gte = greater than or equal to
			# lte = lesser than or equal to
			simpleQuery = { "lightSensitivity" : {"$lt" : lightMax}, "lightSensitivity" : {"$gt" : lightMin}, "temperature" : {"$lt" : tempMax}, "temperature" : {"$gt" : tempMin}}

			# # #
			# TODO : MUST SEND parameters[1:5] TO CALLBACK
			# # #
			db.slot.find_one(simpleQuery, callback=getSlotDone)
			ioloop.IOLoop.current().start()

			# Post the item
			# newItem = [packageName, gotten[1], gotten[2], tempMin, tempMax, lightMin, lightMax, False, None, result[0]]
			# posted = asyncdb.postItem(newItem)

			# Update slot to slotTaken = True, and itemID. (posted is the ID of the newly inserted item)
			# gotten[3] = True
			# gotten[6] = posted
			# ioloop.IOLoop.current().stop()
			# updated = asyncdb.updateSlot(gotten[0], gotten[1:6])
			# updated == 1 => successful

			

		elif command == 'retrieve':
			packageId = parameters[1]
			client.sendMessage(u'Package ' + packageId + ' is queued for delivery to the gate. Please be informed');


	def handleConnected(client):
		print(client.address, 'connected')

	def handleClose(client):
		print(client.address, 'closed')
		

def getSlotDone(result,error):
	print('Slot info is now ready')
	print('result %s error %s' % (repr(result), repr(error)))
	slotID = repr(result['_id'])
	xCoord = repr(result['xCoord'])
	yCoord = repr(result['yCoord'])
	#packageName = ??
	#tempMin = ??
	#tempMax = ??
	#lightMin = ??
	#lightMax = ??
	# We also need the packageName, tempMin, tempMax, lightMin and lightMax of the item.. HOW?!


	postItemQuery = { "itemName" : "test", "xCoord" : xCoord, "yCoord" : yCoord, "tempMin" : 5, "tempMax" : 10, "lightMin" : 700, "lightMax" : 800, "itemTaken" : False, "robotID" : None, "slotID" : slotID}
	db.item.insert_one(postItemQuery, callback=postItemDone)

def postItemDone(result,error):
	print('Item inserted')
	print('result %s error %s' % (repr(result), repr(error)))
	itemID = repr(result.inserted_id) # The ID of the inserted item, will now update slot.
	# Need the slotID from inserted item

	updateSlotQuery = { "_id" : slotID , "$set" : { "itemID" : itemID } }

	db.slot.update(updateSlotQuery, callback=updateSlotDone)


def updateSlotDone(result,error):
	print('Slot updated')
	print('result %s error %s' % (repr(result),repr(error)))

	ioloop.IOLoop.current().stop()


if __name__ == '__main__':
	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	server.serveforever()