import serial,platform,argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-p","--port",required=True,
                    help="Specify serial COM port where board is connected (Windows: COMX - Linux: ttySX")

args = parser.parse_args()

if args.port:
    if platform.system() == "Windows":
        if args.port.startswith("COM"):
            port_name=args.port
        else:
            print("Windows only support COMX ports")
            exit(2)
    else:
        print("Is not windows")

serial_port = serial.Serial(args.port,baudrate=115200)

if not serial_port.is_open:
    try:
        serial_port.open()
    except:
        print("No able to open port")
        exit(2)
else:
    print("Serial port already open :)")



while True:
    try:
        if serial_port.inWaiting() > 0:
            message = serial_port.readline()[:-1].decode("utf-8") 
            print("Se recibio: --{}--".format(message))
    except KeyboardInterrupt:
        print("Serial sesion ending...")
        time.sleep(1)
        serial_port.close()
        break

