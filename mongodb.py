from pymongo import MongoClient
#import bson


client = MongoClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)

# Makes sure db is our 'gspd'-database
db = client.gspd

# The collection 'slot' is stored in variable 'slots'
slots = db.slot
#print slots.find_one() # Prints one item from slots

# if _id is not defined, it will be given an id.
#post = {"xCoord" : 25, "yCoord" : 125, "slotTaken" : False}
#post_id = slots.insert_one(post).inserted_id # Inserts post into slots, and id is stored to post_id.

# Robot has 7 attributes
# Item has 11 attributes
# Slot has 7 attributes

# A query, where the keyvaluepair is the equivalence to 'WHERE'-part in a SQL-command.
# eg: keyvaluepair = {"xCoord" : 25} -- Important, no quotation marks before/after {}
# Will return an array, length depending on the collection. Look at drive-database-document to see structure
def getDocument(coll,jsonquery):
	if coll == "robot":
		if jsonquery == "":
			temp = db.robot.find_one()
		else:
			temp = db.robot.find_one(jsonquery)
		
		if temp != None:
			resp = [temp['_id'], temp['robotName'], temp['xCoord'], temp['yCoord'], temp['state'], temp['robotTaken'], temp['itemID']]
			return resp
		else:
			return "No such document"

	elif coll == "item":
		if jsonquery == "":
			temp = db.item.find_one()
		else:
			temp = db.item.find_one(jsonquery)

		if temp != None:
			
			resp = [temp['_id'], temp['itemName'], temp['xCoord'], temp['yCoord'], temp['tempMin'], temp['tempMax'], temp['lightMin'], temp['lightMax'], temp['itemTaken'], temp['robotID'], temp['slotID']]
			return resp
		else:
			return "No such document"

	elif coll == "slot":
		if jsonquery == "":
			temp = db.slot.find_one()
		else:
			temp = db.slot.find_one(jsonquery)
		
		if temp != None:
			resp = [temp['_id'], temp['xCoord'], temp['yCoord'], temp['slotTaken'], temp['lightSensitivity'], temp['temperature'], temp['itemID']]
			return resp
		else:
			return "No such document"

	else:
		return "error, unknown collection"


# Inserts Document into Collection in Database. 
# Will return error if array is missing elements
# Enter an array that contains the values wanted for the document.
# IMPORTANT: _ID is set automatically, so only enter the other values.
# Ex: [25,125,False,755,20,4234982341] (xCoord,yCoord,slotTaken,Light,Temp,itemID) for slot
# Robot expects 6 values, item 10, slot 6.
def postDocument(coll,array):
	if coll == "robot":
		if len(array) != 6:
			return "Wrong number of values for Robot"
		else:
			doc = { "robotName" : array[0], "xCoord" : array[1], "yCoord" : array[2], "state" : array[3], "robotTaken" : array[4], "itemID" : array[5] }
	elif coll == "item":
		if len(array) != 10:
			return "Wrong number of values for Item"
		else:
			doc = { "itemName" : array[0], "xCoord" : array[1], "yCoord" : array[2], "tempMin" : array[3], "tempMax" : array[4], "lightMin" : array[5], "lightMax" : array[6], "itemTaken" : array[7], "robotID" : array[8], "slotID" : array[9] }
	elif coll == "slot":
		if len(array) != 6:
			return "Wrong number of values for Slot"
		else:
			doc = { "xCoord" : array[0], "yCoord" : array[1], "slotTaken" : array[2], "lightSensitivity" : array[3], "temperature" : array[4], "itemID" : array[5] }
	else:
		return "No valid collection"
	resp_id = coll.insert_one(doc).inserted_id
	return resp_id


# Replace the document that has oldDocID with the newArray.
# Must contain the right amount of elements, robot 6, item 10, slot 6
def updateDocument(coll,oldDocID,newArray):
	if coll == "robot":
		if len(newArray) != 6:
			return "Wrong number of values for Robot"
		else:
			oldDocTemp = getDocument("robot", { "_id" : oldDocID })
			oldDoc = { "robotName" : oldDocTemp[0], "xCoord" : oldDocTemp[1], "yCoord" : oldDocTemp[2], "state" : oldDocTemp[3], "robotTaken" : oldDocTemp[4], "robotID" : oldDocTemp[5] }
			newDoc = { "robotName" : newArray[0], "xCoord" : newArray[1], "yCoord" : newArray[2], "state" : newArray[3], "robotTaken" : newArray[4], "robotID" : newArray[5] }
			result = db.robot.replace_one(oldDoc, newDoc)
	
	elif coll == "item":
		if len(newArray) != 10:
			return "Wrong number of values for Item"
		else:
			oldDocTemp = getDocument("item", { "_id" : oldDocID })
			oldDoc = { "itemName" : oldDocTemp[0], "xCoord" : oldDocTemp[1], "yCoord" : oldDocTemp[2], "tempMin" : oldDocTemp[3], "tempMax" : oldDocTemp[4], "lightMin" : oldDocTemp[5], "lightMax" : oldDocTemp[6], "itemTaken" : oldDocTemp[7], "robotID" : oldDocTemp[8], "slotID" : oldDocTemp[9] }
			newDoc = { "itemName" : newArray[0], "xCoord" : newArray[1], "yCoord" : newArray[2], "tempMin" : newArray[3], "tempMax" : newArray[4], "lightMin" : newArray[5], "lightMax" : newArray[6], "itemTaken" : newArray[7], "robotID" : newArray[8], "slotID" : newArray[9] }
			result = db.item.replace_one(oldDoc, newDoc)
	elif coll == "slot":
		if len(newArray) != 6:
			return "Wrong number of values for Slot"
		else:
			oldDocTemp = getDocument("slot", { "_id" : oldDocID })
			oldDoc = { "xCoord" : oldDocTemp[0], "yCoord" : oldDocTemp[1], "slotTaken" : oldDocTemp[2], "lightSensitivity" : oldDocTemp[3], "temperature" : oldDocTemp[4], "itemID" : oldDocTemp[5] }
			newDoc = { "xCoord" : newArray[0], "yCoord" : newArray[1], "slotTaken" : newArray[2], "lightSensitivity" : newArray[3], "temperature" : newArray[4], "itemID" : newArray[5] }
			result = db.slot.replace_one(oldDoc, newDoc)
	else:
		return "No valid collection"
	return result.acknowledged

# Will delete document from collection. If result == 1, one entry has been deleted.
def deleteDocument(coll,docID):
	if coll == "robot":
		res = db.robot.delete_one({ "_id" : docID })
	elif coll == "item":
		res = db.item.delete_one({ "_id" : docID})
	elif coll == "slot":
		res = db.slot.delete_one({ "_id" : docID })
	else:
		return "No valid collection"
	return res.deleted_count