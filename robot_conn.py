import bluetooth, struct, readchar, time


#see API document in the drive for more info on the functions

def connect(address):
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((address, 1))
    return sock

def close_conn(sock):
    sock.close


def send_coords(sock, coords):
    assert len(coords) == 6
    sock.send(struct.pack(">6i", *coords))



def recv_int(sock):
    num = struct.unpack(">i", sock.recv(10)[0])
    return num


def command_mode():
    pass
