#!/usr/bin/env python

import gtts
import math
import sox
import tempfile

class level():
    '''
    TONE SEQUENCE

    In old Course Navette recordings, the sequence follow neither a diatonic, 
    nor a chromatic or tone scale. Tones are not adjusted to a equal-tempered 
    scale, so we will generate our own sequence. Tone sequence will start on 
    F#3, going up chromatically in and equal tempered scale having A4 = 440 Hz.
    '''
    # Half-tone frequency step
    def nroot(rad, ind):
        # nroot(y, x) = e^( ln(y)/x )
        return math.exp( math.log( float(rad) ) / ind )
    f_step = nroot(2.0, 12)
    # Level 0 frequency = F3 frequency
    freq_0 = 440.0 / f_step ** 16

    # Speed step
    s_step = 0.5
    # Level 0 speed = 8 km/h
    speed_0 = 8.0

    # Run distance = 20 m
    run_dist = 20.0

    # Level minimum duration = 60s
    l_mindur = 60.0

    def __init__(self, stage):
        self.stage = stage
        self.tone_freq = level.freq_0 * level.f_step ** stage
        self.l_speed = level.speed_0 + level.s_step * stage
        # Time, in seconds, to cover the distance. 'spd' is in km/h
        # factor 3.6 (km/m)*(s/h)
        self.run_time = level.run_dist * 3.6 / self.l_speed
        self.laps = math.ceil(level.l_mindur / self.run_time)

    def laps_first_half():
        return math.floor(self.laps/2)
    
    def laps_second_half():
        return math.ceil(self.laps/2)

    def msg_first_half(self):
        self.tts = gtts.gTTS(text= str(self.stage-1) + ' and a half', lang='en')
        self.mfh = tempfile.TemporaryFile()
        self.tts.write_to_fp(self.mfh)
        self.tts.save('/tmp/mfh.mp3')
        return self.mfh

    def msg_second_half(self):
        self.tts = gtts.gTTS(text= 'End of period ' + str(self.stage), lang='en')
        self.msh = tempfile.TemporaryFile()
        self.tts.write_to_fp(self.msh)
        self.tts.save('/tmp/msh.mp3')
        return self.msh



lev = [level(i) for i in range(1,2)]
for i in lev:
    i.msg_first_half()
    i.msg_second_half()
    print i.stage, i.tone_freq, i.l_speed, i.run_time, i.laps

