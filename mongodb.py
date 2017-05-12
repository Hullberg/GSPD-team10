from pymongo import MongoClient
import bson


client = MongoClient("mongodb://root:root@ds135798.mlab.com:35798/gspd",connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)

# Makes sure db is our 'gspd'-database
db = client.gspd

# The collection 'slot' is stored in variable 'slots'
slots = db.slot
#print slots.find_one() # Prints one item from slots

# if _id is not defined, it will be given an id.
#post = {"xCoord" : 25, "yCoord" : 125, "slotTaken" : False}
#post_id = slots.insert_one(post).inserted_id # Inserts post into slots, and id is stored to post_id.

#print post_id

# Inserts Document into Collection in Database. Returns ID of said document.
def postDocument(coll,doc):
	#coll = db.coll1
	post = doc
	resp = coll.insert_one(post)
	return resp.inserted_id, resp.raw_input

# A query, where the keyvaluepair is the equivalence to 'WHERE'-part in a SQL-command.
# eg: keyvaluepair = '{"xCoord" : 25}'
def getDocument(coll,keyvaluepair):
	#coll = db.coll1
	return coll.find_one(keyvaluepair)

# Needs the old document, and replaces it with the new document.
# Any document that matches with oldDoc will be replaced.
# IMPORTANT: Must include all attributes in newDoc, or they will be lost.
# Every document is a dictionary. To get an value of a document, use doc['value']
# Example. doc['_id'] will return the _id-value.
def updateDocument(coll,oldDoc,newDoc):
	#coll = db.coll1
	coll.replace_one(oldDoc,newDoc)
	return newDoc


doc = getDocument(slots,{"slotTaken":True})
print doc['_id']
print updateDocument(slots,{"slotTaken":False},{"xCoord":75,"yCoord":125,"slotTaken":True})


## Use mongoclient-driver instead of RestAPI below. Was easier, when I finally got the driver to work.
#import httplib
# def getDatabases(conn):
# 	# Should get the databases linked to the account
# 	conn.request("GET", "/api/1/databases?apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z")
# 	r = conn.getresponse()
# 	print r.status, r.reason # Hopefully '200 OK'
# 	data = r.read()
# 	return data

# def getCollections(conn):
# 	# Should retrieve all collections (tables) connected to the 'GSPD'-database
# 	conn.request("GET", "/api/1/databases/gspd/collections?apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z")
# 	r = conn.getresponse()
# 	print r.status, r.reason
# 	data = r.read()
# 	return data

# def getDocuments(conn,collection,query):
# 	# Should retrieve all documents (entries) in a collection (table), the 'query' works as 'WHERE'
# 	if query == "":
# 		string = "/api/1/databases/gspd/collections" + collection + "?apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z"
# 		conn.request("GET", string)
# 	else:
# 		# Example: SELECT * FROM item WHERE "itemName" : "golfball" (JSON-format)
# 		# then the query is '"itemName" : "golfball"'
# 		string = "/api/1/databases/gspd/collections" + collection + "?q={" + query + "}&apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z"
# 		conn.request("GET", string)
# 	r = conn.getresponse()
# 	print r.status, r.reason # Hopefully '200 OK'
# 	data = r.read()
# 	return data

# def postDocument(conn,collection,JSON):
# 	# Inserts a document (JSON) into the collection
# 	# Example: postDocument(conn,"item",'{"itemName":"golfball","xCoord":"blah"....}')
# 	post = "/api/1/databases/gspd/collections/" + collection + "?apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z"
# 	# request(POST,post,body,header)
# 	conn.request("POST", post, JSON, {"Content-type" : "application/json"})
# 	r = conn.getresponse()
# 	print r.status, r.reason # Hopefully '200 OK'
# 	data = r.read()
# 	return data

# def updateDocument(conn,collection,query,JSON):
# 	# Updates a document, where the query decides which document to update. Example is query = '_id':3
# 	post = "/api/1/databases/gspd/collections" + collection + "?apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z&q={" + query + "}"
# 	# The JSON could then be '{ "$set" : { "xCoord" : 25 , "yCoord" : 175 } }'
# 	# If you wish to say move the item with id = 3 from a certain slot to (25,175)
# 	conn.request("PUT", post, JSON, {"Content-type" : "application/json"})
# 	r = conn.getresponse()
# 	print r.status, r.reason # Hopefully '200 OK'
# 	data = r.read()
# 	return data

# def deleteDocument(conn,collection,query,JSON):
# 	# Removes a document from a collection. Query identifies the document.
# 	post = "/api/1/databases/gspd/collections" + collection + "?apiKey=_X9Ac2x8QqrXbCgQU4BkemKJi85wy21Z&q={" + query + "}"
# 	conn.request()

# if __name__ == '__main__':
# 	# Creates a connection to base URL path
# 	conn = httplib.HTTPSConnection("api.mlab.com")

# 	collections = getCollections(conn)
# 	print collections

# 	conn.close()