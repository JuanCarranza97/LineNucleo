import mbed as mbed
import argparse
import time
from tkinter import *
from tkinter import ttk
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def receive_a(digits):
    print("G: Se recibio {}".format(digits))

def receive_max(digits):
    app.update_calibrated_values(maxValues=digits)

def receive_min(digits):
    app.update_calibrated_values(minValues=digits)




class main_window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.size = []
        self.init_window()
    
    def init_window(self):
        self.master.title(" Line Follower NUCLEO")
        self.pack(fill=BOTH,expand=1)

        self.minValues_label=[]
        self.maxValues_label=[]
        for i in range(17):
            if(i == 0):
                self.minValues_label.append(ttk.Label(root, text="Min: "))
                self.minValues_label[i].place(x=20+50*i, y=620)
                self.maxValues_label.append(ttk.Label(root, text="Max: "))
                self.maxValues_label[i].place(x=20+50*i, y=640)
            else:
                self.minValues_label.append(ttk.Label(root, text="----"))
                self.minValues_label[i].place(x=20+50*i, y=620)
                self.maxValues_label.append(ttk.Label(root, text="----"))
                self.maxValues_label[i].place(x=20+50*i, y=640)

        nombres = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        datos = [100,200,300,400,500,600,700,800,800,700,600,500,400,300,200,100]
        xx=range(len(datos))        

        figure1 = plt.Figure(figsize=(8,5), dpi=100)
        ax = figure1.add_subplot(111)
        bar = FigureCanvasTkAgg(figure1, self)
        barobject = bar.get_tk_widget()
        barobject.place(x=50,y=80)
        ax.bar(xx, datos, width=.5, align='center')
        ax.set_ylim([0,1000])
        ax.set_xticks(xx)
        ax.set_xticklabels(nombres)
        
        self.read_calibration = Button(self,text="read calibration",command=self.read_calibration_function)
        self.read_calibration.place(x=10,y=0)

        self.calibrate_sensors = Button(self,text="Calibrate",command=self.calibrate_sensors_function)
        self.calibrate_sensors.place(x=200,y=0)

        self.show_sensors = Button(self,text="show",command=self.show_sensors_function)
        self.show_sensors.place(x=300,y=0)

        self.exit_button = Button(self,text="EXIT",command=self.exit_function)
        self.exit_button.place(x=860,y=665)

    def calibrate_sensors_function(self):
        mbed.send_data(serial_port,"c")

    def read_calibration_function(self):
        mbed.send_data(serial_port,"s")
    
    def show_sensors_function(self,values):
        plt.plot([1,2,3,4,6,7,8,9,10,11,12,13,14,15,16], [values], 'ro')
        plt.axis([0, 16, 0, 1000])
        plt.show()

    def exit_function(self):
        logging.info("Closing port ...")
        action_port.close()
        serial_port.close()
        exit(0)

    def update_calibrated_values(self,minValues=0,maxValues=0):
        for i in range(16):
            try:
                self.minValues_label[i+1].config(text=minValues[i])
            except:
                pass
            try:
                self.maxValues_label[i+1].config(text=maxValues[i])
            except:
                pass

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p","--port",required=True,
                            help="Specify serial COM port where board is connected (Windows: COMX - Linux: ttySX")

        args = parser.parse_args()

        serial_port = mbed.configure_port(args.port)
        
        whenchar = [mbed.receiver("a",receive_a),
                    mbed.receiver("m",receive_min),
                    mbed.receiver("M",receive_max)]
        
        action_port = mbed.receiver_port(serial_port,whenchar)

        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        
        root = Tk()
        root.geometry("900x700")

        

        app = main_window(root)
        ##app.update_calibrated_values([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])
        root.mainloop()
        """while True:
            print("LED ON")
            mbed.send_data(serial_port,"l",[1])
            time.sleep(.5)
            print("LED OFF")
            mbed.send_data(serial_port,"l",[0])
            time.sleep(.5)
            """   
    except KeyboardInterrupt:
        action_port.close()
        serial_port.close()
        
