import serial,platform,argparse
import time
import threading
import re
import logging 

serialThreadStatus = False
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def thread_serial(serial_port):
    global serialThreadStatus
    serialThreadStatus=True

    logging.debug("Serial Thread Listening")
    while serialThreadStatus:
        if serial_port.inWaiting() > 0:
            message = serial_port.readline()[:-1].decode("utf-8") 
            logging.debug("Se recibio: --{}--".format(message))

            matcher = re.compile(r'[A-Za-z][-]?[0-9]+([,][-]?[0-9]+)*$')
            
            if matcher.match(message):
                char = message[0]
                digits = message[1:]

                if digits.find(',') :
                    digits = digits.split(',')
                logging.debug("Char: {}, Digits: {}".format(char,digits))
            else:
                logging.error("Expression doesn't match")
                logging.error(message)

    logging.debug("Serial Thread: finishing")

def send_data(port,caracter,data=[0]):
    if not port.is_open:
        logging.info("Port is closed, opening port to send message")
        port.open()
    
    message = caracter
    for current_data in data:
        message+=str(current_data)+","
    message = message[:-1]
    message+="\n"
    port.write(message.encode('utf-8'))

def configure_port(port_name):  
    if platform.system() == "Windows":
        if not port_name.startswith("COM"):
            logging.error("Windows only support COMX ports")
            exit(2)
    else:
        logging.error("Is not windows")

    serial_port = serial.Serial(port_name,baudrate=115200)
    if not serial_port.is_open:
        try:
            serial_port.open()
        except:
            logging.error("No able to open port")
            exit(2)
    else:
        logging.info("Serial port already open :)")

    return serial_port

class receiver:
    def __init__(self,caracter,function):
        self.caracter = caracter
        self.function = function
    
class receiver_port:
    def __init__(self,serial_port,receiver):
        self.caracters = []
        self.receiver = receiver

        serialThread = threading.Thread(target=self.thread_serial, args=(serial_port,))
        serialThread.start()

    def thread_serial(self,serial_port):
        global serialThreadStatus
        serialThreadStatus=True

        logging.debug("Serial Thread Listening")
        while serialThreadStatus:
            if serial_port.inWaiting() > 0:
                message = serial_port.readline()[:-1].decode("utf-8") 
                logging.debug("Se recibio: --{}--".format(message))

                matcher = re.compile(r'[A-Za-z][-]?[0-9]+([,][-]?[0-9]+)*$')

                if matcher.match(message):
                    char = message[0]
                    digits = message[1:]

                    if digits.find(',') :
                        digits = digits.split(',')
                    logging.debug("Char: {}, Digits: {}".format(char,digits))
                    char_found = False
                    for i in self.receiver:
                        if i.caracter == char:
                            logging.debug("El caracter {} fue encontrado".format(char))
                            i.function(digits)
                            char_found=True
                    
                    if not char_found:
                        logging.info("Caracter '{}' was not found".format(char))

                else:
                    if message.startswith("ERROR:"):
                        logging.error("BOARD: {}".format(message.replace("ERROR: ","")))
                    elif message.startswith("DEBUG:"):
                        logging.error("BOARD: {}".format(message.replace("DEBUG: ","")))
                    elif message.startswith("INFO:"):
                        logging.error("BOARD: {}".format(message.replace("INFO: ","")))

    def close(self):
        global serialThreadStatus
        serialThreadStatus = False

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p","--port",required=True,
                            help="Specify serial COM port where board is connected (Windows: COMX - Linux: ttySX")

        args = parser.parse_args()

        serial_port = configure_port(args.port)
        
        serialThread = threading.Thread(target=thread_serial, args=(serial_port,))
        serialThread.start()

        while True:
            user_input = input("\nEnter a command:\n")
            
            if user_input == "send":
                message = input("Enter message:\n")
                matcher = re.compile(r'[A-Za-z][-]?[0-9]+([,][-]?[0-9]+)*$')
            
                if matcher.match(message):
                    char = message[0]
                    digits = message[1:]

                    if digits.find(','):
                        digits = digits.split(',')
                        send_data(serial_port,char,digits)
                        print("MESSAGE SEND: Char: {}, Digits: {}".format(char,digits))
                else:
                    print("Expression doesn't match")
                    print(message)

    
            else:
                print("Command not defined")
        
    except KeyboardInterrupt:
        serialThreadStatus = False
        print("Closing port ...")
        serial_port.close()
        

    