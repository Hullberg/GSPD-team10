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
import robot_conn
#import ardnet

mc_client = motor_tornado.MotorClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
db = mc_client.gspd

global itemsInDB
global amt

# # # # # # # # # # # # # # # # # #
# MARK - Websocket interaction with client
# # # # # # # # # # # # # # # # # #

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


			client.sendMessage(u'Searching for a slot for ' + packageName)
			client.sendMessage(packageName + u' is queued for storing. Please be informed');

			simpleQuery = { "slotTaken" : False, "lightSensitivity" : {"$lte" : lightMax}, "lightSensitivity" : {"$gte" : lightMin}, "temperature" : {"$lte" : tempMax}, "temperature" : {"$gte" : tempMin}}
			parameters = [packageName, tempMin, tempMax, lightMin, lightMax]
			callback_function = partial(storeGetSlotDone,parameters)
			db.slot.find_one(simpleQuery, callback=callback_function)

			ioloop.IOLoop.current().start() # Goes to storeGetSlotDone when finished


		elif command == 'retrieve':
			packageId = parameters[1]
			client.sendMessage(u'Package ' + packageId + ' is queued for delivery to the gate. Please be informed');
			# The ID is simply a string in front-end, convert to ObjectId

			pckID = ObjectId(packageId)
			callback_function = partial(retrieveGetItemDone, pckID)

			db.item.find_one({ "_id" : pckID }, callback=callback_function)
			ioloop.IOLoop.current().start()


	def handleConnected(client):
		print(client.address, 'connected')
		# print(itemsInDB)
		#client.sendMessage(itemsInDB) # Send all items in the database to the client. To know what to retrieve


	def handleClose(client):
		print(client.address, 'closed')


# # # # # # # # # # # # # # # # # #
# MARK - Storing an item, callback functions following each other, in order
# # # # # # # # # # # # # # # # # #

def storeGetSlotDone(parameters, result, error):
	if (repr(result) == "None"):
		print('Either all slots are filled, or no slots fulfill the requirements')
	#	SimpleEcho.client.sendMessage(u'Either all slots are filled, or no slots fulfill the requirements')
		# Send back to client it didn't work.
	else:
		print('Slot info is now ready')
	print('result %s error %s' % (repr(result), repr(error)))
	temp = repr(result['_id']).split("'")[1]
	slotID = ObjectId(temp)
	xCoord = int(repr(result['xCoord']))
	yCoord = int(repr(result['yCoord']))
	packageName = parameters[0]
	tempMin = parameters[1]
	tempMax = parameters[2]
	lightMin = parameters[3]
	lightMax = parameters[4]

	params = [slotID, xCoord, yCoord]

	postItemQuery = { "itemName" : packageName, "xCoord" : xCoord, "yCoord" : yCoord, "tempMin" : tempMin, "tempMax" : tempMax, "lightMin" : lightMin, "lightMax" : lightMax, "itemTaken" : True, "robotID" : None, "slotID" : slotID}
	callback_function = partial(storePostItemDone, params)
	db.item.insert_one(postItemQuery, callback=callback_function) # Continues to postItemDone


def storePostItemDone(parameters, result, error):
	print('Item inserted')
	print('result %s error %s' % (repr(result), repr(error)))
	temp = repr(result.inserted_id).split("'")[1]
	itemID = ObjectId(temp)
	slotID = parameters[0]
	parameters[0] = itemID

	callback_function = partial(storeUpdateSlotDone,parameters)
	db.slot.update({ '_id' : slotID }, {"$set" : {"itemID" : itemID, "slotTaken" : True }}, callback=callback_function) # Continues to updateSlotDone


def storeUpdateSlotDone(parameters, result, error):
	print('Slot updated')
	print('result %s error %s' % (repr(result), repr(error)))

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
	robX = repr(result['xCoord'])
	robY = repr(result['yCoord'])
	#  [itemID, x, y]
	params = [parameters[0],parameters[1],parameters[2], robotID, robX, robY]
	# Keep sending itemID
	callback_function = partial(storeUpdateRobotDone, params)
	db.robot.update({ '_id' : robotID }, {"$set" : {"robotTaken" : True, "itemID" : parameters[0]}}, callback=callback_function)

def storeUpdateRobotDone(parameters, result, error):
	print('Robot updated')
	print('result %s error %s' % (repr(result), repr(error)))
	# [slotID, x, y, robotID, robX, robY]
	# Find item with params[0], set it's robotID to params[3]
        print(parameters[0])
	callback_function = partial(storeUpdateItemDone, parameters)
	db.item.update({ '_id' : parameters[0] }, {"$set" : {"robotID" : parameters[3]}}, callback=callback_function)

def storeUpdateItemDone(parameters, result, error):
	print('Item updated')
	print('result %s error %s' % (repr(result), repr(error)))
	# Parameters = [itemID, x,y, robotID, robX, robY]
	# When doing a store, the robot will always be at (0,0,0)
	

	# We have tested and know the robot will get the task. Update database before
	# However, tasks can then be overridden, caution.
	callback_function = partial(storeUpdateRobotSecond, parameters)
	db.robot.update({ '_id' : parameters[3] }, { "$set" : { "robotTaken" : False, "itemID" : None }}, callback = callback_function)

def storeUpdateRobotSecond(parameters, result, error):
	print('Robot is available, be cautious')
	coords = [0, 0, 0, int(parameters[1]), int(parameters[2]), 0]
	response = sendCoords(coords)
	print('Coordinates sent to the robot')
	ioloop.IOLoop.current().stop()
	


# # # # # # # # # # # # # # # # # #
# MARK - Retrieving an item, callbacks in order
# # # # # # # # # # # # # # # # # #

def retrieveGetItemDone(parameters, result, error):
	print('Item found')
	print('result %s error %s' % (repr(result), repr(error)))
	# result is the document found.
	# They are received as strings, and must be converted to ObjectId's.
	temp1 = repr(result['_id']).split("'")[1]
	itemID = ObjectId(temp1)
	temp2 = repr(result['slotID']).split("'")[1]
	slotID = ObjectId(temp2)

	xCoord = repr(result['xCoord'])
	yCoord = repr(result['yCoord'])

	parameters = [itemID, slotID, xCoord, yCoord] # Keep these throughout the callback, to avoid loosing track
        print(parameters)
	callback_function = partial(retrieveFindRobotDone, parameters)

	db.robot.find_one({ "state" : True, "robotTaken" : False}, callback = callback_function)


def retrieveFindRobotDone(parameters, result, error):
	print('Available robot found')
	print('result %s error %s' % (repr(result), repr(error)))
	temp = repr(result['_id']).split("'")[1]
	robotID = ObjectId(temp)
	robX = repr(result['xCoord'])
	robY = repr(result['yCoord'])
	parameters.append(robotID) # [itemID, slotID, xCoord, yCoord, robotID, robX, robY]
	parameters.append(robX)
	parameters.append(robY)

	callback_function = partial(retrieveUpdateRobotDone, parameters)
	db.robot.update({ '_id' : robotID }, { "$set" : { "robotTaken" : True, "itemID" : parameters[0] }}, callback = callback_function)


def retrieveUpdateRobotDone(parameters, result, error):
	print('result %s error %s' % (repr(result), repr(error)))
	# Update slot
	callback_function = partial(retrieveUpdateSlotDone, parameters)
	db.slot.update({ '_id' : parameters[1] }, { "$set" : { "slotTaken" : False, "itemID" : None }}, callback = callback_function)


def retrieveUpdateSlotDone(parameters, result, error):
	print('result %s error %s' % (repr(result), repr(error)))
	# Lastly update item
	callback_function = partial(retrieveUpdateItemDone, parameters)
	db.item.update({ '_id' : parameters[0]}, { "$set" : { "robotID" : parameters[4], "slotID" : None }}, callback = callback_function)


def retrieveUpdateItemDone(parameters, result, error):
	print('result %s error %s' % (repr(result), repr(result)))
	# Item is updated, send task to robot.
	# parameters = [itemID, slotID, xCoord, yCoord, robotID, robX, robY]
	# When doing a retrieve robot will always go to (0,0,0)

	callback_function = partial(retrieveUpdateRobotSecond, parameters)
	db.robot.update({ "_id" : parameters[4] }, { "$set" : { "robotTaken" : False, "itemID" : None } })


def retrieveUpdateRobotSecond(parameters, result, error):
	print('Robot available for new work, caution')

	callback_function = partial(retrieveRemoveItem, parameters)
	db.item.delete_many({ "_id" : parameters[0] }, callback=callback_function)


def retrieveRemoveItem(parameters, result, error):
	print('Item removed from database')
	print('Robot will now get task')
	coords = [int(parameters[2]),int(parameters[3]),0,0,0,0]

	response = sendCoords(coords)
	# As we do not expect any return value, we just send it and hope it works. Usually does.
	print('Coordinates sent to robot')
	ioloop.IOLoop.current().stop()



# # # # # # # # # # # # # # # # # #
# MARK - Robot interaction
# # # # # # # # # # # # # # # # # #

bd_addr = "00:16:53:52:1E:34" #EV3 robot bluetooth address

rob_conn = robot_conn.RobotConnection(bd_addr) # Uses robot_conn.py to initiate connection to the EV3 robot

def asyncSendCoords(coords, callback=None):
	return callback(rob_conn.send_coords(coords))

@gen.engine
def sendCoords(coords):
	gen.Task(asyncSendCoords, coords)

def asyncGetTaskDone():
	return callback(rob_conn.recv_int())

@gen.engine
def getTaskDone():
	gen.task(asyncGetTaskDone)


# # # # # # # # # # # # # # # # # #
# MARK - Arduino connection
# # # # # # # # # # # # # # # # # #

# Retrieve light / temperature and update the slots in the database.
# TODO

# def asyncUpdateSlotDB(callback=None):
# 	# Create ardunit
# 	# ard = ardunit("?", 57600, "at")
# 	# Should be arduino measurements instead of temps.
# 	# temptemp = ard.get_temp()
# 	# templight = ard.getvl()
# 	temptemp = 20
# 	templight = 800
# 	listOfSlots = yield db.slot.find({}).to_list(None)
# 	for x in range(0,len(listOfSlots))
# 		db.slot.update({ "_id" : listOfSlots[x]['_id'] }, { "$set" : { "temperature" : temptemp, "lightSensitivity" : templight }})
# 	return callback("done")

# @gen.engine
# def updateSlotDB():
# 	gen.Task(asyncUpdateSlotDB)


# # # # # # # # # # # # # # # # # #
# MARK - Misc.
# # # # # # # # # # # # # # # # # #

# def asyncGetItems(callback=None):
# 	temp = yield db.slot.find({}).to_list(None)
# 	amt = len(temp)
# 	itemsInDB = []
# 	for x in range(0,amt):
# 		itemsInDB.append([str(temp[x]['_id']), str(temp[x]['itemName']), str(temp[x]['xCoord']), str(temp[x]['yCoord'])])
# 	return callback(itemsInDB)

# @gen.engine
# def getAllItems():
# 		gen.Task(asyncGetItems)

# # # # # # # # # # # # # # # # # #
# MARK - Main
# # # # # # # # # # # # # # # # # #
if __name__ == '__main__':

	#getAllItems()

	server = SimpleWebSocketServer('', 9000, SimpleEcho)
	server.serveforever()
