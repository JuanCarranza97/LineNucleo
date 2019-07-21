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

def receive_b(digits):
    print("B: Se recibio {}".format(digits))

def receive_d(digits):
    print("BARRA RECIBIDA: {}".format(digits))

def exit_command():
    print("CLossing APP ..")
    action_port.close()
    serial_port.close()
    exit(0)

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

        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        
        root = Tk()
        root.geometry("200x100")
        #content = ttk.Frame(root)
        namelbl = ttk.Label(root, text="Name")
        name = ttk.Entry(root)
        
        minValues = []
        maxValues = []
        #minValues.append(ttk.Label(root, text="Min {}".format(0)))
        #minValues[0].place(y=10, x=10)
        #minValues[0].pack()
        #for i in range(16):
        #    minValues.append(ttk.Label(root, text="Min {}".format(i)))
        #    minValues[i].place(y=10, x=10)
        #    minValues[i].pack()
            #maxValues.append(ttk.Label(root, text="Max {}".format(i)))
            #maxValues[i].place(y=i*10, x=50)
            #maxValues[i].pack()

        #onevar = BooleanVar()
        #twovar = BooleanVar()
        #threevar = BooleanVar()
        #onevar.set(True)
        #twovar.set(False)
        #threevar.set(True)

        #one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
        #two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
        #three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
        """nombres = ['Sen 1','Sen 2','Sen 3','Sen 4','Sen 5','Sen 6','Sen 7','Sen 8','Sen 9','Sen 10','Sen 11','Sen 12','Sen 13','Sen 14','Sen 15','Sen 16']
        datos = [100,200,300,400,500,600,700,800,800,700,600,500,400,300,200,100]
        xx=range(len(datos))

        figure1 = plt.Figure(figsize=(10,5), dpi=100)
        ax = figure1.add_subplot(111)
        bar = FigureCanvasTkAgg(figure1, root)
        bar.get_tk_widget().pack(side=LEFT, fill=BOTH)
        ax.bar(xx, datos, width=.5, align='center')
        ax.set_ylim([0,1000])
        ax.set_xticks(xx)
        ax.set_xticklabels(nombres)"""

        ok = ttk.Button(root, text="Okay")
        cancel = ttk.Button(root, text="EXIT",command=exit_command)
        cancel.place(x=0,y=0)
        cancel.pack()
        #content.grid(column=0, row=0)
        #frame.grid(column=0, row=0)# columnspan=3, rowspan=2)
        #name.grid(column=0, row=0)
        #cancel.grid(column=1, row=0)
        """namelbl.grid(column=1, row=0)#, columnspan=2)
        name.grid(column=3, row=1, columnspan=2)
        one.grid(column=0, row=3)
        two.grid(column=1, row=3)
        three.grid(column=2, row=3)
        ok.grid(column=3, row=3)
        """

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
        
