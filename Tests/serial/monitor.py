import mbed as mbed
import argparse
import time
import threading
import re

def receive_a(digits):
    print("G: Se recibio {}".format(digits))

def receive_b(digits):
    print("B: Se recibio {}".format(digits))

def receive_d(digits):
    print("BARRA RECIBIDA: {}".format(digits))

    
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p","--port",required=True,
                            help="Specify serial COM port where board is connected (Windows: COMX - Linux: ttySX")

        args = parser.parse_args()

        serial_port = mbed.configure_port(args.port)
        
        whenchar = [mbed.receiver("a",receive_a),
                    mbed.receiver("b",receive_b),
                    mbed.receiver("d",receive_d)]
        
        action_port = mbed.receiver_port(serial_port,whenchar)

        while True:
            """print("LED ON")
            mbed.send_data(serial_port,"l",[1])
            time.sleep(.5)
            print("LED OFF")
            mbed.send_data(serial_port,"l",[0])
            time.sleep(.5)
            """
            mbed.send_data(serial_port,"t")
            time.sleep(.5)

    except KeyboardInterrupt:
        action_port.close()
        print("Closing port ...")
        serial_port.close()
        