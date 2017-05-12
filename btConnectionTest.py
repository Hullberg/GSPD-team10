import bluetooth
import struct

bd_addr = "00:16:53:52:1E:34" #EV3 robot address

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )


sock.connect((bd_addr, port))
connected = False

# while not connected:
#     try:
#         sock.connect((bd_addr, port))
#         connected = True
#     except Exception as e:
#         pass



sock.send(struct.pack(">8s", "42,43,44")) # 8 is for the length of the string


num = struct.unpack(">I", sock.recv(1024))[0]
#int.from_bytes(sock.recv(1024), byteorder='big') # decode bytestream from robot

print("the answer is " + str(num))

sock.close()
