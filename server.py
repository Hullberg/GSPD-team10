import socket
import string
import MySQLdb


def send_http(HTTPBODY,connection):
	response_proto = 'HTTP/1.1'
	response_status = '200'
	response_status_text = 'OK'

	#response_body = [
		#'<html><body><h1>Hello, world!</h1>'#,
		#'<p>This page is in location %(request_uri)r, was requested ' % locals(),
		#'using %(request_method)r, and with %(request_proto)r.</p>' % locals(),
		#'<p>Request body is %(request_body)r</p>' % locals(),
		#'<p>Actual set of headers received:</p>',
		#'<ul>',
	#]
	response_body = ['<html><body>']
	response_body.append(HTTPBODY)
	response_body.append('</body></html>')
	response_body_raw = ''.join(response_body)

	response_headers = {
		'Content-Type': 'text/html; encoding=utf8',
		'Content-Length': len(response_body_raw),
		'Connection': 'keep-alive',
	}

	response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())

	connection.send('%s %s %s' % (response_proto, response_status, response_status_text))
	connection.send(response_headers_raw)
	connection.send('\n')
	connection.send(response_body_raw)



#SQL-calls can now be made with cursor.execute('SELECT * FROM table'), example:
#sql = "SELECT * FROM Slot"
#cursor.execute(sql)

if __name__ == '__main__':

	# Create database connection, and prepare cursor
	db = MySQLdb.connect('localhost','root','', 'gspd')
	cursor = db.cursor()

	# mysql.server start (in console)
	# mysql -h localhost -u root -p (leave password blank)

	HOST, PORT = '', 8889

	# Bind a socket to allow connection to web client.
	listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listen_socket.bind((HOST, PORT))
	listen_socket.listen(1)

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

			tempbody = "Item: " + itemName + ", temp: " + tempReq + ", light: " + lightReq
			send_http(tempbody, client_connection)


			# Should also adjust to tempReq and lightReq, with a reasonable range, but that is not decided yet.
			#sql = "SELECT * FROM Slot WHERE slotTaken = 'FALSE'"

			try: 
				cursor.execute(sql)
				results = cursor.fetchall()
				for row in results:
					slotID = row[0]
					xCoord = row[1]
					yCoord = row[2]
					slotTaken = row[3]
					item__slot = row[4]
			except:
				print "Error: unable to fecth data"

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
		#http_response = """\
#	HTTP/1.1 200 OK
#	Hello, World!
#	"""
		#send_http("poop",client_connection)
		client_connection.close()



	db.close()
