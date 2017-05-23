import robot_conn

bd_addr = "00:16:53:52:1E:34" #EV3 robot address

connected = False

# create connection
conn = robot_conn.RobotConnection(bd_addr)

# fake coordinates
coords = [x for x in range(0,6)]

#test to send coords
conn.send_coords(coords)

#test to receive int
num = conn.recv_int()

#test to receive coords
nums = conn.recv_coords()

# print single received int
print("the answer is " + str(num))

# print received list of coordinates
print("nums are " + str(nums))
conn.close_conn()
