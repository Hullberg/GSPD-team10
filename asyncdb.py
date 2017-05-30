from motor import motor_tornado
from tornado import gen, ioloop
import time
from bson.objectid import ObjectId

mc_client = motor_tornado.MotorClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
	
# Makes sure db is our 'gspd'-database
db = mc_client.gspd

#ioloop = ioloop.IOLoop.current()

# def my_callback(result, error):
# 	print('result %s error %s' % (repr(result), repr(error)))
# 	IOLoop.current().stop()

# # #
# GET-functions - Will return the object asked for in query.
# # #
# Usage: slot = yield getSlot(query)
@gen.coroutine
def getSlot(query):
	result = yield db.slot.find_one(query)
	if result != None:
		res = [result['_id'], result['xCoord'], result['yCoord'], result['slotTaken'], result['lightSensitivity'], result['temperature'], result['itemID']]
		raise gen.Return(res)
	else:
		raise gen.Return("No result")

# robot = yield getRobot(query)
@gen.coroutine
def getRobot(query):
	result = yield db.robot.find_one(query)
	if result != None:
		res = [result['_id'], result['robotName'], result['xCoord'], result['yCoord'], result['state'], result['robotTaken'], result['itemID']]
		raise gen.Return(res)
	else:
		raise gen.Return("No result")

@gen.coroutine
def getItem(query):
	result = yield db.item.find_one(query)
	if result != None:
		res = [result['_id'], result['itemName'], result['xCoord'], result['yCoord'], result['tempMin'], result['tempMax'], result['lightMin'], result['lightMax'], result['itemTaken'], result['robotID'], result['slotID']]
		raise gen.Return(res)
	else:
		raise gen.Return("No result")


# # #
# POST-functions - Will return the ID of the inserted object
# # #

@gen.coroutine
def postSlot(array):
	if len(array) != 6:
		raise gen.Return("Wrong format. [xCoord,yCoord,slotTaken,lightSensitivity,temperature,itemID]")
	else:
		doc = { "xCoord" : array[0], "yCoord" : array[1], "slotTaken" : array[2], "lightSensitivity" : array[3], "temperature" : array[4], "itemID" : array[5]}
		result = yield db.slot.insert_one(doc)
		raise gen.Return(result.inserted_id)

@gen.coroutine
def postRobot(array):
	if len(array) != 6:
		raise gen.Return("Wrong format. [robotName,xCoord,yCoord,state,robotTaken,itemID]")
	else:
		doc = { "robotName" : array[0], "xCoord" : array[1], "yCoord" : array[2], "state" : array[3], "robotTaken" : array[4], "itemID" : array[5]}
		result = yield db.robot.insert_one(doc)
		raise gen.Return(result.inserted_id)

@gen.coroutine
def postItem(array):
	if len(array) != 10:
		raise gen.Return("Wrong format. [itemName,xCoord,yCoord,tempMin,tempMax,lightMin,lightMax,itemTaken,robotID,slotID]")
	else:
		doc = { "itemName" : array[0], "xCoord" : array[1], "yCoord" : array[2], "tempMin" : array[3], "tempMax" : array[4], "lightMin" : array[5], "lightMax" : array[6], "itemTaken" : array[7], "robotID" : array[8], "slotID" : array[9]}
		result = yield db.item.insert_one(doc)
		raise gen.Return(result.inserted_id)

# # #
# UPDATE-functions - Will return amount of rows affected. Replaces the document with array.
# # # 

@gen.coroutine
def updateSlot(ID,array):
	if len(array) != 6:
		raise gen.Return("Wrong format. [xCoord,yCoord,slotTaken,lightSensitivity,temperature,itemID]")
	else:
		doc = { "xCoord" : array[0], "yCoord" : array[1], "slotTaken" : array[2], "lightSensitivity" : array[3], "temperature" : array[4], "itemID" : array[5]}
		result = yield db.slot.replace_one({ '_id' : ID }, doc)
		raise gen.Return(result.modified_count)

@gen.coroutine
def updateRobot(ID,array):
	if len(array) != 6:
		raise gen.Return("Wrong format. [robotName,xCoord,yCoord,state,robotTaken,itemID]")
	else:
		doc = { "robotName" : array[0], "xCoord" : array[1], "yCoord" : array[2], "state" : array[3], "robotTaken" : array[4], "itemID" : array[5]}
		result = yield db.robot.replace_one({ '_id' : ID }, doc)
		raise gen.Return(result.modified_count)

@gen.coroutine
def updateItem(ID,array):
	if len(array) != 10:
		raise gen.Return("Wrong format. [itemName,xCoord,yCoord,tempMin,tempMax,lightMin,lightMax,itemTaken,robotID,slotID]")
	else:
		doc = { "itemName" : array[0], "xCoord" : array[1], "yCoord" : array[2], "tempMin" : array[3], "tempMax" : array[4], "lightMin" : array[5], "lightMax" : array[6], "itemTaken" : array[7], "robotID" : array[8], "slotID" : array[9]}
		result = yield db.item.replace_one({ '_id' : ID }, doc)
		raise gen.Return(result.modified_count)

# # #
# MAIN
# # #
@gen.coroutine
def main():
	# start = time.time()
	# #res2 = yield getSlot({ "_id" : 591442da81aa9d5700e68cdb })
	# res = yield db.slot.find_one()
	# #print res['_id']
	# res2 = yield db.slot.find_one({"_id" : {"$oid" : "591442da81aa9d5700e68cdb"}}) 
	# print res2
	# print "Hopefully gets item with 700 < light < 800"
	# #print res2['_id'] # No result, as Item is currently empty
	# #res = yield getSlot({"itemID" : ""})
	# #print res
	# end = time.time()
	# print (end-start)
	#res = yield db.robot.insert_one({ "robotName" : "someBTAddr", "xCoord" : 137, "yCoord" : 78, "state" : True, "robotTaken" : False, "itemID" : None })
	
	# USE THIS TO FIND ITEMS WHEN STARTING CLIENT
	res = yield db.item.find({}).to_list(None) # No requirement on length
	print(res)
	l = len(res)
	arr = []
	for x in range (0,l):
		itemid = str(res[x]['_id'])
		#print(itemid + "," + res[x]['itemName'] + "," + str(res[x]['xCoord']) + "," + str(res[x]['yCoord'])) # Here we can retrieve whatever attributes we want and send to client.
		arr.append([itemid, str(res[x]['itemName']), str(res[x]['xCoord']), str(res[x]['yCoord'])])
	

if __name__ == '__main__':
	ioloop.IOLoop.instance().run_sync(main)