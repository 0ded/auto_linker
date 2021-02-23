import tkinter as tk
from tkinter import *
from data_scheduler import DataHandler, Timeframe
from datetime import datetime

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def add_to_data(entries, dh):
    dh.append(entries["link"].get(), 0, int(entries["minute"].get()),
              int(entries["hour"].get()), days.index(entries["day"].get()))
    text.set("added link \r\n" + entries["hour"].get() + ":" + entries["minute"].get())


def reset_file():
    DataHandler("data.json", Timeframe("days", 7))
    text.set("all links removed")


def make_app(root):
    entries = {}
    row = tk.Frame(root)
    lab = tk.Label(row, text="day" + ": ", anchor='w')

    variable = StringVar(root)
    variable.set(days[datetime.now().isoweekday() & 7])  # default value
    ent = OptionMenu(row, variable, *days)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)

    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.LEFT)

    entries["day"] = variable

    row = tk.Frame(root)
    lab = tk.Label(row, text="hour" + ": ", anchor='w')
    ent = tk.Entry(row)
    ent.insert(0, datetime.now().hour)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.LEFT)

    entries["hour"] = ent

    lab = tk.Label(row, text="minute" + ": ", anchor='w')
    ent = tk.Entry(row)
    ent.insert(0, datetime.now().minute)

    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.LEFT)

    entries["minute"] = ent

    row = tk.Frame(root)
    lab = tk.Label(row, text="Link" + ": ", anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.LEFT)

    row = tk.Frame(root)
    lab = tk.Label(row, textvariable=text, anchor='w')
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    lab.pack(side=tk.LEFT)

    entries["link"] = ent
    return entries


if __name__ == '__main__':
    dh = DataHandler("data.json")
    if not dh.is_init():
        dh = DataHandler("data.json", Timeframe("days", 7))
    root = tk.Tk()
    root.resizable(False, False)
    root.title("configure links")
    root.iconbitmap("icon.ico")

    text = tk.StringVar()
    text.set("insert time and link, than press 'add'\r\n use reset data to wipe all the links")

    ents = make_app(root)
    b1 = tk.Button(root, text='add',
           command=(lambda e=ents: add_to_data(e, dh)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='reset data',
                   command=(lambda: reset_file()))
    b2.pack(side=tk.RIGHT)
    root.mainloop()
