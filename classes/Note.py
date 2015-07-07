import re, math
from decimal import *

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
                     

    def __init__(self,pitch,duration,absoluteduration=True):
        
        try:
            self.pitch = Decimal(pitch)


        except InvalidOperation as e:

            pitch = pitch.capitalize()
            
            if self.valid_non_numeric_pitch_input_regex.search(pitch):
                
                if "-" in pitch or "+" in pitch:
#                    print pitch
                    r = re.search(r"^([A-Ga-g][b#]?\d)([+-])(\d+)([ch])",pitch)
                    self.pitch = self.freq_from_note_and_modifier(r.group(1),r.group(2),r.group(3),r.group(4))
                    
                else:
                    print pitch
                    self.pitch = self.freq_from_note(pitch)
            else:                    
                raise InvalidPitchException(pitch)

            print self.pitch

    def freq_from_note_and_modifier(self,note,sign,modval,modtype):
        if (modtype == 'c'):
            if (sign == '+'):
                return self.freq_from_note(note,modval)
            elif (sign == "-"):
                return self.freq_from_note(note,0-modval)
        elif (modtype == 'h'):
            if (sign == '+'):
                return self.freq_from_note(note) + int(modval)
            elif (sign == '-'):
                return self.freq_from_note(note) - int(modval)
        else:
            return self.freq_from_note(note)

    def freq_from_note(self,note,multiplier=0):
        basenote = self.note_map[note[:-1]]
        
        octave = int(note[-1:])

        octave_diff = octave-4


        half_step_shift = Decimal(octave_diff*12 + basenote + int(multiplier)/100)
        return float(440)*math.pow(math.pow(2,0.083333333333333),half_step_shift)

class InvalidPitchException(Exception):


    def __init__(self,value):
        self.value = value
    
    def __str__(self):
        
        errorstr = "\n\tInvalid pitch string %s" % self.value
        errorstr+= "\n\tString must follow one of the following formats:"
        errorstr+= "\n\t\"d\" where d is a positive, non-zero integer,"
        errorstr+= "\n\t[A-G][b|#]d, specifying a note on a standard keyboard,"
        errorstr+= "\n\twith C4 representing middle C."
        errorstr+= "\n\tWith a keyboard note, you may optionally specify an offset of"
        errorstr+= "\n\t[+-]d[h|c], where d is any integer, and h|c indicates"
        errorstr+= "\n\teither Hertz or cents as an offset from the supplied note.\n"
        
        return errorstr
        
