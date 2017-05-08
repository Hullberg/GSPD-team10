import socket
import string
import MySQLdb
# import websocket
# import thread
# import time



HOST, PORT = '', 8888

# Bind a socket to allow connection to web client.
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

# Create database connection, and prepare cursor
#db = MySQLdb.connect("localhost","user","password", "dbname")
#cursor = db.cursor()

# SQL-calls can now be made with cursor.execute('SELECT * FROM table'), example:
# sql = "SELECT * FROM Slot"
# cursor.execute(sql)

print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)

    # Handle request
    getindex = request.find("GET", 0, len(request))
    httpindex = request.find("HTTP", 0, len(request))
    # request[getindex+5:httpindex-1] will return 'hello' from localhost:8888/hello
    # as it removes 'GET /' and ' HTTP/1.1'
    req = request[getindex+5:httpindex-1]

    # Assuming the requests are like store(itemName,tempReq,lightReq), or moveUp(workID)
    if req[0:5] == 'store':
    	print 'store, args: ' + req[5:]
    	args = req[5:]
    	args = args[1:len(args)-1]
    	#itemindex is always 0
    	tempindex = args.find(",",0,len(args))
    	lightindex = args.find(",",tempindex+1,len(args))
    	itemName = args[0:tempindex]
    	tempReq = args[tempindex+1:lightindex]
    	lightReq = args[lightindex+1:len(args)]
    	print itemName
    	print tempReq
    	print lightReq


    	# Should also adjust to tempReq and lightReq, with a reasonable range, but that is not decided yet.
    	#sql = "SELECT * FROM Slot WHERE slotTaken = 'FALSE'"

    	#try: 
    	#	cursor.execute(sql)
    	#	results = cursor.fetchall()
    	#	for row in results:
    	#		slotID = row[0]
    	#		xCoord = row[1]
    	#		yCoord = row[2]
    	#		slotTaken = row[3]
    	#		item__slot = row[4]
    	#except:
   		#	print "Error: unable to fecth data"

    elif req[0:8] == 'retrieve':
    	print 'retrieve, args: ' + req[8:]
    	args = req[8:]
    	# Only itemName
    	itemName = args[1:len(args)-1]

    	#sql = "SELECT * FROM Item WHERE itemName = '%s'" % itemName
    	#try:
    	#	cursor.execute(sql)
    	#	results = cursor.fetchall()
    	#	for row in results:
    	#		itemID = row[0]
    	#		itemName = row[1]
    	#		xCoord = row[2]
    	#		yCoord = row[3]
    	#		tempReq = row[4]
    	#		lightReq = row[5]
    	#		itemTaken = row[6]
    	#		robot__item = row[7]
    	#		item__slot = row[8]
    	


    elif req[0:7] == 'moveUp':
    	print 'moveUp, args: ' + req[7:]
    	args = req[7:]
    	workID = args[1:len(args)-1]
    	# Swap two tasks in the work queue


    elif req[0:8] == 'moveDown':
    	print 'moveDown, args: ' + req[8:]
    	args = req[8:]
    	workID = args[1:len(args)-1]
    	# Swap two tasks in the work queue


    elif req == 'favicon.ico':
    	pass
    else:
    	print 'req: ' + req
    

    # What to send back to the server
    http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    client_connection.close()

db.close()

# def on_message(ws, message):
#     print message

# def on_error(ws, error):
#     print error

# def on_close(ws):
#     print "### closed ###"

# def on_open(ws):
#     def run(*args):
#         for i in range(3):
#             time.sleep(1)
#             ws.send("Hello %d" % i)
#         time.sleep(1)
#         ws.close()
#         print "thread terminating..."
#     thread.start_new_thread(run, ())

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("ws://echo.websocket.org/",
#                               on_message = on_message,
#                               on_error = on_error,
#                               on_close = on_close)
#     ws.on_open = on_open
#     ws.run_forever()