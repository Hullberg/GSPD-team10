import bluetooth, struct, readchar, time


#see API document in the drive for more info on the functions

class RobotConnection():

    def __init__(self, address):
        connected = False
        while not connected:
            try:
                self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                self.sock.connect((address, 1))
                connected = True
            except Exception as e:
                time.sleep(2)
                continue

    def close_conn(self):
        self.sock.close()


    def send_coords(self, coords):
        assert len(coords) == 6
        self.sock.send(struct.pack(">6i", *coords))

    def recv_coords(self):
        nums = struct.unpack(">3i", self.sock.recv(12))
        assert len(nums) == 3
        return list(nums)

    def recv_int(self):
        num = struct.unpack(">i", self.sock.recv(4))[0]
        return num
