import serial 
from serial.tools import list_ports
import keyboard
from clean_data import *
# from graphs import 
import graphs
# from clean_data import find_data

class SerialConnection():
    
    def __init__(self) -> None:
        
        
        self.__port=None
        self.__baudrate=9600
        self.__parity=serial.PARITY_NONE
        self.__stopbits=serial.STOPBITS_ONE
        self.__bytesize=serial.EIGHTBITS
        self.__timeout=1

        self.__Serial = serial.Serial(port=self.__port, baudrate=self.__baudrate, parity=self.__parity, stopbits=self.__stopbits, bytesize=self.__bytesize, timeout=self.__timeout )

    def __str__(self) -> str:
        return f'{self.__Serial}'
    
    
    def set_port(self,port):
        '''
        use to set port for conn 
        return None 
        '''
        self.__Serial.port = port
        print(f'connected to {self.__Serial.portstr}')
        
    def get_port (self):
        '''
        Return curr connected port 
        '''
        port  = self.__Serial.port
        return port 

    def check_activite_conn(self):

        avai =  list_ports.comports() 
        for i in range(len(avai)):
            cur =  str(avai[i])
            if 'CH340' in cur:
                a = cur[:4]
                return a 

    
    def get_all_ports_old(self):
        '''
        Returns a dictionary containg all avaialable ports  
        Input : None 
        Output : A dict {key->int : value->str}
               : if ports are not available it return False -> bool
        '''
        avai =  list_ports.comports() 
        
        if len(avai) > 0:
            new_avai = []
        
            for i in range(len(avai)):
                cur_port =  str(avai[i])
                a = cur_port[:4]
                new_avai.append(a)

            l = [i for i in range (1,len(avai)+1)]
        
            avai_dict = {}

            for i , v in zip(l,new_avai):
                avai_dict.update({i:v})

            return avai_dict
        else: 
            return False    
    def get_all_ports(self):
        '''
        Returns a dictionary containg all avaialable ports  
        Input : None 
        Output : A dict {key->int : value->str}
               : if ports are not available it return False -> bool
        '''
        avai =  list_ports.comports() 
        
        if len(avai) > 0:
            new_port = []
            new_name= []
            for i in range(len(avai)):
                cur_port =  str(avai[i])
                port = cur_port[:4]
                name = cur_port[6:]
                new_port.append(port)
                new_name.append(name)

            l = [i for i in range (1,len(avai)+1)]
        
            avai_port_dict = {}
            avai_name_dict ={}
            for i , port in zip(l,new_port):
                avai_port_dict.update({i:port})

            for i , name in zip(l,new_name):
                avai_name_dict.update({i:name})

        # yield avai_port_dict        
        # yield avai_name_dict

        return [avai_port_dict,avai_name_dict]            
    
    def __start_conn (self):
        '''
        Start the serial conn with current port specified
        Returns a Boolean Value True if conn is open else False   
        '''
        self.__Serial.open()
        res = self.__Serial.is_open
        return res

    def __close_conn(self):
        '''
        Close the serial conn 
        Returns a Boolean Value False if conn is Closed 
        else True if conn is open
        '''

        self.__Serial.close()
        
        return self.__Serial.is_open
 
    def __read_data(self):

        """Read data line by line and return it """

        line = self.__Serial.readline()
        line = line.decode('utf-8')

        clean_line = find_data(line[12:]) 
        
        print(clean_line)
        return clean_line

        # return line

    def main(self):

        try :     
            all = self.get_all_ports()
            if all != False:
                ports = all[0]
                names = all[1]
                for k,v in zip(names.keys(),names.values()):
                    print(f'{k}) {v}')
                try:
                    i = None
                    i = int(input('Select any Port Press respective Number (1-9) : '))
                    if type(i) != int:
                       i = int(i)           
                except :
                    print('input should be integer only (1-9)')
                
                if (type(i) == int) and (i in range (1,10)):
                    port = None
                    port = ports.get(i)

                    if port :
                        self.set_port(port)

                        try : 
                            a = self.__start_conn()
                            if a:
                                while self.__Serial.is_open: 
                                    print(self.__read_data())
                                    if keyboard.is_pressed('q'):
                                        res = self.__close_conn()

                                
                                # if res == False:
                                #     print('Connection is Closed')

                                
                                if res == False:
                                    print('Connection is Closed')

                        except ValueError: 
                    
                            print(f'Error in starting connection to port {port}')        

                    else : 
                        print('Invalid Port Selected')
                else :
                    print('Error in user input')
            else:
                print('No Ports available')
        except ValueError:
            print('test')


        
            


if __name__ == '__main__':
    
    # ser = serial.Serial()
    # ser.port = 'COM6'
    # ser.open()
    # ser.close()
    #print(ser.is_open)
    ser = SerialConnection()
    
    ser.main()