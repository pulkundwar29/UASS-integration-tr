from myserial import MySerial


class FrequencySetup:
    def __init__(self, serial: MySerial) -> None:
        "It will be used to change oeprating frequency of "
        self.serial = serial

    def setFrequency(self, frequency: float):
        "return 0 on successful completion else 1, need to be called within 2 sec of connection initialization"
        try:
            if 400 <= frequency <= 405:
                self.serial.writeData("RadioSonde DAS")
                if self.serial.readData().find("RadioSonde DAS") == -1:
                    print("handshake error")
                    return 1
                frequency = int(frequency*100)
                self.serial.writeData(str(frequency))
                if self.serial.readData().find(str(frequency)):
                    print("handshake error")
                    return 1
                print(
                    f"succesfully saved frequnecy of {frequency/100} MHz in Radiosonde")
                return 0
            else:
                print("enter valid frequency")
                return 1
        except Exception as e:
            print(e)


if __name__ == '__main__':
    frequency_setup = FrequencySetup(MySerial())

    while True:
        frequency = float(input("enter frequnecy in MHz : "))
        if frequency_setup.setFrequency(frequency) == 0:
            break
