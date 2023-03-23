from myserial import MySerial


class RadioController:
    """to control ratio via serial"""
    def __init__(self) -> None:
        self.serial = MySerial()

    def radioHandShake(self):
        if self.serial.writeData() == 1:
            print("Error in radio handshake")
            exit()
        else:
            print("handShake Done")

    def changeFrequency(self):
        self.serial.writeData("")
