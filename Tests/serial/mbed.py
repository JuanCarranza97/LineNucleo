import serial,platform,argparse
import time
import threading
import re

serialThreadStatus = False

def thread_serial(serial_port):
    global serialThreadStatus
    serialThreadStatus=True

    print("Serial Thread Listening")
    while serialThreadStatus:
        if serial_port.inWaiting() > 0:
            message = serial_port.readline()[:-1].decode("utf-8") 
            print("Se recibio: --{}--".format(message))

            matcher = re.compile(r'[A-Za-z][-]?[0-9]+([,][-]?[0-9]+)*$')
            
            if matcher.match(message):
                char = message[0]
                digits = message[1:]

                if digits.find(','):
                    digits = digits.split(',')
                print("Char: {}, Digits: {}".format(char,digits))
            else:
                print("Expression doesn't match")
                print(message)

    print("Serial Thread: finishing")

def send_data(port,caracter,data):
    if not port.is_open:
        print("Port is closed, opening port to send message")
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
            print("Windows only support COMX ports")
            exit(2)
    else:
        print("Is not windows")

    serial_port = serial.Serial(port_name,baudrate=115200)
    if not serial_port.is_open:
        try:
            serial_port.open()
        except:
            print("No able to open port")
            exit(2)
    else:
        print("Serial port already open :)")

    return serial_port

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
        

    