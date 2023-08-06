from tkinter.filedialog import askopenfilename
import tkinter
from tkinter import ttk

def open_file():
    tkinter.Tk().withdraw()
    file = askopenfilename()
    if file:
        print(file)
    else:
        print('Cancelled')
