from serial import Serial
from serial.tools import list_ports
import time

class MySerial:
    """class used to interface python serial port"""
    def __init__(self, boud_rate=9600):
        """auto called, provide boud_rate if required"""
        self.boud_rate = boud_rate

        # auto detect available serial ports and connect them, provide options if multiple ports found
        available = list_ports.comports()
        port = None
        if len(available) == 0:
            print("No device found")
        elif len(available) == 1:
            print(available[0], " selected")
            port = available[0][0]
        else:
            print("following devices found")
            for i in range(len(available)):
                print(i + 1, available[i])
            ip = int(input('please enter the correct index :'))-1
            print(available[ip], ' selected')
            port = available[ip][0]

        if port == None:
            exit()
        else:
            self.port = port
            self.__startConnection()

    def __startConnection(self):
        self.conn = Serial(self.port,self.boud_rate)

    def closeConnection(self):
        self.conn.close()

    def readData(self)-> str:
        """Read data and return it""" 
        line = self.conn.readline()
        line = line.decode('utf-8')
        return line

    def writeData(self, msg):
        self.conn.write(msg.encode())

    def getRepose(self, msg):
        time.sleep(.05)
        self.writeData(msg)
        # time.sleep(.4)
        return self.readData()


def test_Serial():
    mySerial = MySerial()

    while True:
        # mySerial.writeData("hello")
        # time.sleep(.1)
        print(mySerial.readData())

    # print(mySerial.writeData("on"))
    # print(mySerial.readData())
    # print(mySerial.writeData("off"))
    # print(mySerial.readData())
    # print(mySerial.writeData("on"))
    # print(mySerial.readData())
    # print(mySerial.writeData("off"))
    # print(mySerial.readData())
    # print(mySerial.writeData("on"))
    # print(mySerial.readData())

    # print(mySerial.writeData('off'))
    # time.sleep(2)
    # print(mySerial.writeData('on'))
    # # time.sleep(2)
    # print(mySerial.readData())
    # print(mySerial.writeData('off'))
    # time.sleep(2)
    # print(mySerial.writeData('on'))

    mySerial.closeConnection()


if __name__ == '__main__':
    test_Serial()
