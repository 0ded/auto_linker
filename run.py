from datetime import datetime
from data_scheduler import *
from time import *
import webbrowser
import tkinter as tk
from tkinter import *


def mainloop(past_link):
    day = datetime.now().isoweekday() & 7
    hour = datetime.now().hour
    minute = datetime.now().minute
    link = dh.get(0, minute, hour, day)
    if link is not None and link != past_link:
        webbrowser.open(link)
        past_link = link
    root.after(6000, mainloop, past_link)


if __name__ == '__main__':
    past_link = "Totallynotalink"
    dh = DataHandler("data.json")
    root = tk.Tk()
    root.resizable(False, False)
    root.title("auto linker")
    root.iconbitmap("icon.ico")
    root.protocol("WM_DELETE_WINDOW", root.iconify)

    text = tk.StringVar()
    text.set("insert time and link, than press 'add'\r\n use reset data to wipe all the links")

    row = tk.Frame(root)
    lab = tk.Label(row, text="Links will be open automatically when this window is open\r\n", anchor='w')
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    lab.pack(side=tk.LEFT)

    b2 = tk.Button(root, text='quit',
                   command=(lambda: root.quit()))
    b2.pack(side=tk.BOTTOM)
    mainloop(past_link)
    root.mainloop()


