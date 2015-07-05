#!/usr/bin/python

from classes.Terminal import Terminal
from Tkinter import *

class Algorhythm:
    root = Tk()

    def __init__(self):
        yscrollbar = Scrollbar(self.root)
        terminal = Terminal(self.root)
        terminal.term.configure(yscrollcommand = yscrollbar.set)
        yscrollbar.configure(command = terminal.term.yview)
        yscrollbar.pack(side = RIGHT, fill = Y)
        terminal.term.pack(side = "bottom", fill = "both")
        self.root.mainloop()


main = Algorhythm()
