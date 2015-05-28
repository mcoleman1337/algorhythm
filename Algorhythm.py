#!/usr/bin/python

from classes.Terminal import Terminal
from Tkinter import *

class Algorhythm:
    root = Tk()

    def __init__(self):
        aoeu = Terminal(self.root)
        aoeu.term.pack(side = "bottom", fill = "both")
        self.root.mainloop()


main = Algorhythm()
