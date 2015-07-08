import re, math
from decimal import *

class Note:
    
    #note has three parameters:
    #pitch: base frequency in HZ
    #duration: length of time either relative to the tempo (such as quarter note, half, etc or absolute (in ms)
    general_pitch_regex = re.compile(r"!([A-Za-z0-9\-+#]*)")

    valid_non_numeric_pitch_input_regex = re.compile(r"^([A-Ga-g][b#]?\d([+-]\d+[ch])?)$")

    valid_duration_input_regex = re.compile(r"^(\d+([./]\d+)?)(ms|[whqes])$")

    note_map = dict([("Ab",11),("A",0),("A#",1),
                     ("Bb",1),("B",2),("B#",3),
                     ("Cb",2),("C",3),("C#",4),
                     ("Db",4),("D",5),("D#",6),
                     ("Eb",6),("E",7),("E#",8),
                     ("Fb",7),("F",8),("F#",9),
                     ("Gb",9),("G",10),("G#",11)])
                     

    def __init__(self,pitch,duration,tempo):
        
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


        try:
            tempo_ = float(tempo)
            if (tempo_ <= 0):
                raise InvalidTempoException(tempo)
        except ValueError:
            raise InvalidTempoException(tempo)

        r = self.valid_duration_input_regex.search(duration)
        if r:
            import __future__
            n = eval(compile(r.group(1), '<string>', 'eval', __future__.division.compiler_flag))
            if r.group(3) == 'ms':
                self.duration = n
            elif r.group(3) == "w":
                self.duration = 4.00000000 / float(tempo) * 60.0000000 * n
            elif r.group(3) == "h":
                self.duration = 2.00000000 / float(tempo) * 60.0000000 * n
            elif r.group(3) == "q":
                self.duration = 1.00000000 / float(tempo) * 60.0000000 * n
            elif r.group(3) == "e":
                self.duration = 0.50000000 / float(tempo) * 60.0000000 * n
            elif r.group(3) == "s":
                self.duration = 0.25000000 / float(tempo) * 60.0000000 * n
            else:
                raise InvalidDurationException(duration+": Ian screwed something up in the parsing")
#            self.duration = duration #need to specify syntax for declaring note duration
        else:
            raise InvalidDurationException(duration)
        #thinking about letter suffixes: ms for milliseconds, q for quarter note, s for sixteenth, e for eighth, etc.
        print repr(self.pitch)+" "+repr(self.duration)

    def freq_from_note_and_modifier(self,note,sign,modval,modtype):
        if (modtype == 'c'):
            if (sign == '+'):
                return self.freq_from_note(note,modval)
            elif (sign == "-"):
                return self.freq_from_note(note,0-int(modval))
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


        half_step_shift = Decimal(octave_diff*12 + basenote + float(multiplier)*0.01)

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
        
class InvalidDurationException(Exception):

    def __init__(self,value):
        self.value = value

    def __str__(self):
        
        errorstr = "\n\tInvalid duration string \"%s\"" % self.value
        errorstr+= "\n\tString must follow the following format:"
        errorstr+= "\n\tn[ms|w|h|q|e|s], where"
        errorstr+= "\n\tn -> an integer, float, or fraction"
        errorstr+= "\n\t[ms|w|h|q|e|s] -> the subdivision to use, where"
        errorstr+= "\n\t\tms -> milliseconds (tempo indepedent)"
        errorstr+= "\n\t\tw -> a whole note (tempo dependent)"
        errorstr+= "\n\t\th -> a half note"
        errorstr+= "\n\t\tq -> a quarter note"
        errorstr+= "\n\t\te -> an eighth note"
        errorstr+= "\n\t\ts -> a sixteenth note"
                               
        return errorstr
        
class InvalidTempoException(Exception):

    def __init__(self,value):
        self.value = value

    def __str__(self):

        errorstr = "\n\tInvalid tempo \"%s\"" % self.value
        errorstr+= "\n\tTempo must be a valid floating point number!"
        return errorstr
