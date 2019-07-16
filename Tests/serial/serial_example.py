import serial,platform,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p","--port",help="Specify serial COM port where board is connected (Windows: COMX - Linux: ttySX")

parser.parse_args()