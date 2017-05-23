import bluetooth, struct, readchar, time


#see API document in the drive for more info on the functions

class RobotConnection():

    # def connect(address):
#     sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#     sock.connect((address, 1))
#     return sock

    def __init__(self, address):
        self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.sock.connect((address, 1))


    def close_conn(self):
        self.sock.close()


    def send_coords(self, coords):
        assert len(coords) == 6
        self.sock.send(struct.pack(">6i", *coords))

    def recv_coords(self):
        nums = struct.unpack(">i", self.sock.recv(12))
        assert len(coords) == 3
        return nums

    def recv_int(self):
        num = struct.unpack(">i", self.sock.recv(4)[0])
        return num
