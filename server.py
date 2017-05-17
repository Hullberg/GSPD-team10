import socket
import string
import mongodb


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


if __name__ == '__main__':

	
	HOST, PORT = '', 8888

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
			tempMINindex = args.find(",",0,len(args))
			tempMAXindex = args.find(",",tempminindex+1,len(args))
			lightMINindex = args.find(",",tempMAXindex+1,len(args))
			lightMAXindex = args.find(",",lightMINindex+1,len(args))
			itemName = args[0:tempMINindex]
			tempMin = args[tempMINindex+1:tempMAXindex]
			tempMax = args[tempMAXindex+1:lightMINindex]
			lightMin = args[lightMINindex+1:lightMAXindex]
			lightMax = args[lightMAXindex+1:len(args)]
			print itemName
			print tempMin
			print tempMax
			print lightMin
			print lightMax

			tempbody = "Item: " + itemName + ", tempMin: " + tempMin + ", tempMax: " + tempMax + ", lightMin: " + lightMin + ", lightMax: " + lightMax
			send_http(tempbody, client_connection)

			# Find good spot with requirements fullfilled and slot free.
			slot = getDocument("slot", { "lightSensitivity" : lightReq, "temperature" : tempReq, "slotTaken" : False })
			
			# Create item object, set it's coordinates to same as slots.
			item = [itemName, slot[1], slot[2], tempReq, lightReq, False, "", slot[0]] # Set slotID to slot's ID.
			res1 = postDocument("item", item) # returns ID of object.
			
			# Update slot so it is taken
			updSlot = [slot[1], slot[2], True, slot[4], slot[5], res1]
			res = updateDocument("slot", slot[0], updSlot) # Returns true if success
			# Should also adjust to tempReq and lightReq, with a reasonable range, but that is not decided yet.
			
			# #
			# Send this to the robot
			# #

		elif req[0:8] == 'retrieve':
			print 'retrieve, args: ' + req[8:]
			args = req[8:]
			# Only itemName
			itemName = args[1:len(args)-1]
			item = getDocument("item", { "itemName" : itemName })
			slot = getDocument("slot", { "_id" : item[8]}) # Should be slotID
			
			# #
			# Send this information to the robot
			# #

			# Set the slot to slotTaken = False, as we take away the item.
			updSlot = [slot[1], slot[2], False, slot[4], slot[5], ""]
			res = updateDocument("slot", slot[0], updSlot) # Returns true if success

			# Remove the item from the database, as it has been taken out.
			res1 = deleteDocument("item", item[0])
			

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
