#!/usr/bin/python

from Tkinter import *

class Terminal:
    
    def __init__(self, root):
        
        self.term = Text(root, width = 150, height = 10, foreground = "#FFFFFF", background = "#000000", insertbackground = "#FFFFFF")
        self.term.focus()
        self.term.bind("<Up>",self.up_bind)
        self.term.insert(END,"> ","prompt")
        self.term.tag_config("prompt", foreground = "#00FF00")
        

    def up_bind(self,event):
        return "break"
