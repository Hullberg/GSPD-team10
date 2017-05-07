import bluetooth

bd_addr = "00:16:53:52:1E:34" #EV3 robot address

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send(b'52') # send bytestream, possibly use packed struct instead

num =  int.from_bytes(sock.recv(1024), byteorder='big') # decode bytestream from robot

print("the answer is " + str(num))

sock.close()
