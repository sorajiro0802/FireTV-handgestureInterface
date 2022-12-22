import serial

class ArduinoController:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, 9600)
        self.gesture_order_map = {  'On': "1",
                                    'Off': "0"}

    
    def connect(self):
        self.ser = serial.Serial(self.port, 9600)
        return 0
        
    def command(self, key):
        self.ser.write(self.gesture_order_map[key].encode())
    
    def kill(self):
        print("serialPort closed")
        self.ser.close()
    
    def restart(self):
        pass
    
    
if __name__=="__main__":
    pass