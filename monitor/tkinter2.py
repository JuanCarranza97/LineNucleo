from tkinter import *
from tkinter import ttk

def clicked():
    namelbl.configure(text="Cambio!!")
    print("Se clicko :)")

def cancel_command():
    print("Closing app ...")
    exit(0)


root = Tk()
content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=5, relief="sunken")#, width=500, height=100)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()
onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay",command=clicked)
cancel = ttk.Button(content, text="Cancel",command=cancel_command)

content.grid(column=0, row=0)
frame.grid(column=0, row=0)# columnspan=3, rowspan=2)
namelbl.grid(column=1, row=0)#, columnspan=2)
name.grid(column=3, row=1, columnspan=2)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.mainloop()