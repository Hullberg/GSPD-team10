import bluetooth
import struct
import readchar
import time
import robot_conn

bd_addr = "00:16:53:52:1E:34" #EV3 robot address

connected = False

conn = robot_conn.RobotConnection(bd_addr)


coords = [x for x in range(0,6)]

conn.send_coords(coords)


num = conn.recv_int()

nums = conn.recv_coords()

print("the answer is " + str(num))

print("nums are " + str(nums))
conn.close_conn()
