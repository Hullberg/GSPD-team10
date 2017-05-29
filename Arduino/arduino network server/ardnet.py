import serial
import time
import sys, getopt
import subprocess
from bottle import run, post, request, response, get, route

class ardunit(object):

    last_Temp = -1
    last_vl = -1
    last_ul = -1
    last_rh = -1
    
    def __init__(self, port, bauderate, position):
        self.ser = serial.Serial("COM7", 57600, timeout=0)
        self.location = position
    def get_temp(self):

        try:
            self.ser.write('t')
            time.sleep(1)
            self.last_Temp = self.ser.readline()
            return self.last_Temp
        
        except self.ser.SerialTimeoutException:
            print('Data could not be read')

    def get_vl(self):
        
        try:
            self.ser.write('v')
            time.sleep(1)
            self.last_vl = self.ser.readline()
            return self.last_vl
        
        except self.ser.SerialTimeoutException:
            print('Data could not be read')

    def get_uv(self):
        print("TODO");
    def get_rh(self):
        print("TODO");
        
class ardnet(object):

    def __init__(self):
        self.units = []
        
    def new_arduino(self,port,bauderate,position):
        self.units.append(ardunit(port,bauderate,position))
        return 1
    
    def get_temperature(self,location):
        for x in self.units:
            if x.location == location:
                return x.get_temp()
    
    def get_visual_light(self,location):
        for x in self.units:
            if x.location == location:
                return x.get_vl()

    def list_all(self):
        retval = []
        for x in self.units:
            retval.append(x.location)
        return "".join(retval)
            
def main(argv):
    mynet = ardnet()
    baude = 57600
    i = 0
    while i < len(argv):
        mynet.new_arduino(argv[i],baude,argv[i+1])
        i+=2
    
    @get('/get_temp')
    def get_temp():
        pos = request.params.getunicode('location')
        return mynet.get_temperature(pos)

    @get('/get_vl')
    def get_vl():
        pos = request.params.getunicode('location')
        return mynet.get_visual_light(pos)

    @get('/add_arduino')
    def add_arduino():
        port = request.params.getunicode('port')
        baude = request.params.getunicode('baude')
        pos = request.params.getunicode('location')       
        return mynet.new_arduino(port,int(baude),pos)

    @get('/get_arduinos')
    def get_arduino():
        return mynet.list_all()


        
    run(host='localhost', port=8080, debug=True)

    
    
    print argv[0]


            
if __name__ == '__main__':
    main(sys.argv[1:])
    
