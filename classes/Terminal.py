#!/usr/bin/python

from Tkinter import *
import time
import thread 
import re

class Terminal:
    
    terminal_history = []

    history_level = 0
    
    def __init__(self, root):
        
        self.term = Text(root, width = 150, height = 10, foreground = "#FFFFFF", background = "#000000", insertbackground = "#FFFFFF")

        self.term.focus()

        self.term.bind("<Up>",self.up_bind)

        self.term.bind("<Down>",self.down_bind)

        self.term.bind("<Left>",self.protect_prompt_bind)

        self.term.bind("<BackSpace>",self.protect_prompt_bind)
        
        self.term.bind("<Return>",self.return_bind)

        self.term.insert(END,"> ","prompt")

        self.term.mark_set("input_start","end-1c")

        self.term.tag_config("prompt", foreground = "#00FF00")

        
    
    def up_bind(self,event):
#        print self.terminal_history[len(self.terminal_history)-self.history_level]
        a, b = self.history_level , len(self.terminal_history)
        i = b - a - 1

        if i > 0:
            self.history_level+=1

        self.process_input( self.terminal_history[i])
        return "break"

    def down_bind(self,event):



        a, b = self.history_level , len(self.terminal_history)
        i = b - a - 1
        if i < len(self.terminal_history)-1:
            self.history_level-=1

        self.process_input( self.terminal_history[i])

        return "break"

    def protect_prompt_bind(self,event):
        index = self.term.index("insert-1c").split(".")
        if int(index[1]) < 2:
            return "break"
        
    

    def return_bind(self,event):
        self.history_level = 0
        self.term.tag_remove('prompt', "1.0", "end")
        temp_index = self.term.index("end-1l")[:2]+"2"
        self.term.mark_set("input_start",temp_index)
        term_input = self.term.get('input_start','end').rstrip()
        self.term.insert("end","\n> ",'prompt')
        self.terminal_history.append(term_input)

        return "break"

    def process_input(self,input_str):
        self.term.delete('input_start+1l','end-1c')
        self.term.insert('input_start+1l',input_str)
