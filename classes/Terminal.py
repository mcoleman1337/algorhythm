#!/usr/bin/python

from Tkinter import *
import time
import thread 
import re

class Terminal:
    
    terminal_history = []

    def __init__(self, root):
        
        self.term = Text(root, width = 150, height = 10, foreground = "#FFFFFF", background = "#000000", insertbackground = "#FFFFFF")

        self.term.focus()

        self.term.bind("<Up>",self.up_bind)

        self.term.bind("<Down>",self.down_bind)

        self.term.bind("<Left>",self.protect_prompt_bind)

        self.term.bind("<BackSpace>",self.protect_prompt_bind)
        
        self.term.bind("<Return>",self.return_bind)

        self.term.insert(END,"> ","prompt")

        self.term.tag_config("prompt", foreground = "#00FF00")

        
    
    def up_bind(self,event):
        return "break"

    def down_bind(self,event):
        return "break"

    def protect_prompt_bind(self,event):
        index = self.term.index("insert-1c").split(".")
        if int(index[1]) < 2:
            return "break"
        
    
    def return_bind(self,event):

        self.term.tag_remove('prompt', '{0}.{1}'.format(len(self.terminal_history)+1,0), '{0}.{1}'.format(len(self.terminal_history)+1,2))
        self.process_input(re.sub("^> ","",self.term.get(str(len(self.terminal_history))+".2","end").strip()))
        self.term.insert("end","\n> ",'prompt')
        self.terminal_history.append(self.term.get(str(len(self.terminal_history))+".2","end"))

        return "break"

    def process_input(self,input_str):
        print input_str
