#!/usr/bin/python

import re,math
from decimal import *


class InferenceEngine:

    def __init__(self,term):
        
        self.terminal = term
        print "Inference Engine Created"

    def parse_input(self,input_text):
        
        note_regex = re.compile("<(.*?)>")

        for note in note_regex.findall(input_text):
            try:
                Note(note)
            except TooDamnManyPitchesException as tdmpe:
                print tdmpe.value
            except NoDamnPitchException as ndpe:
                print ndpe.value
            except InvalidDamnPitchException as idpe:
                print idpe.value
        
            
class Note:

    general_pitch_regex = re.compile(r"!([A-Za-z0-9\-+#]*)")
    valid_non_numeric_pitch_input_regex = re.compile(r"^([A-Ga-g][b#]?\d([+-]\d+[ch])?)$")
    note_map = dict([("Ab",11),("A",0),("A#",1),
                     ("Bb",1),("B",2),("B#",3),
                     ("Cb",2),("C",3),("C#",4),
                     ("Db",4),("D",5),("D#",6),
                     ("Eb",6),("E",7),("E#",8),
                     ("Fb",7),("F",8),("F#",9),
                     ("Gb",9),("G",10),("G#",11)])
                     

    def __init__(self,input_text):
        
        pitches = self.general_pitch_regex.findall(input_text)
        
        if (len(pitches) == 0):

            raise NoDamnPitchException("Error: NO DAMN PITCHES in note group \""+input_text+"\"")

        elif (len(pitches) > 1):

            raise TooDamnManyPitchesException("Error: TOO DAMN MANY PITCHES in note group \""+input_text+"\"")
        else:

            try:
                self.pitch = Decimal(pitches[0])

            except InvalidOperation as ve:
                pitches[0] = pitches[0].capitalize()

                if self.valid_non_numeric_pitch_input_regex.search(pitches[0]):
                    
                    if "-" in pitches[0]:
                        note,suffix = pitches[0].split("-",2)
                        self.pitch = self.freq_from_note_and_modifier(note,suffix)
                        
                    else:
                        note = pitches[0]
                        self.pitch = self.freq_from_note(note)
                else:                    
                    raise InvalidDamnPitchException("Error: Invalid pitch string in note group \""+input_text+"\"")
        print self.pitch

    def freq_from_note_and_modifier(self,note,mod):
        return self.freq_from_note(note)

    def freq_from_note(self,note):
        basenote = self.note_map[note[:-1]]
        
        octave = int(note[-1:])

        octave_diff = octave-4


        half_step_shift = Decimal(octave_diff*12 + basenote)
        return float(440)*math.pow(math.pow(2,0.083333333333333),half_step_shift)


        
class NoDamnPitchException(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class TooDamnManyPitchesException(Exception):
    
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidDamnPitchException(Exception):

    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class MismatchedDamnBracketsException(Exception):

    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)
