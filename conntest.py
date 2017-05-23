import bluetooth
import struct
import readchar
import time
import robot_conn

bd_addr = "00:16:53:52:1E:34" #EV3 robot address

port = 1

#sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )


#sock.connect((bd_addr, port))

sock = robot_conn.connect(bd_addr) # uses connect function from robot_conn

connected = False

# try to connect in a loop

# while not connected:
#     try:
#         sock.connect((bd_addr, port))
#         connected = True
#     except Exception as e:
#         sleep(1)
#         pass

# use this for sending three movement commands to the robot

for x in range(0,3):

    key = readchar.readkey()
    sock.send(struct.pack(">i", int(key)))
    print(key)


# use this to send a set of three coordinates to the robot
#sock.send(struct.pack(">3i", 3,3,44)) #

coords = [x in range(0,6)]

robot_conn.send_coords(sock, coords)


num = robot_conn.recv_int(sock)

print("the answer is " + str(num))

sock.close()
