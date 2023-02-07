import pyb
from pyb import Pin as Pin

class Encoder:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__(self, Apin, Bpin, timer):
        """! 
        Creates aencoder channels by initializing GPIO
        pins. 
        @param en_pin (There will be several pin parameters)
        """
        self.enc_chA = Pin(Apin, Pin.OUT_PP)
        self.enc_chB = Pin(Bpin, Pin.OUT_PP)
        self.tim = pyb.Timer(timer, prescaler=0, period=0xFFFF)
        self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.enc_chA)
        self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.enc_chB)
        self.position = 0
        self.prev_position = 1000
        self.old_delta = 0
        print ("Creating Encoder")

        
    def read(self):
        new_delta = self.tim.counter()
        delta_1 = new_delta - self.old_delta

        if delta_1 <= -32768:
            delta_1 += 65536
            if new_delta > self.old_delta: #big drop
                delta_1 = new_delta - 65536 - self.old_delta
        #Checking for Underflow in the encoder readings and then sub-checking if the direction changed to forwards
        if delta_1 >= 32768:
            delta_1 -= 65536
            if new_delta < self.old_delta: #jump
                delta_1 = new_delta + 65536 - self.old_delta
                
        self.old_delta = new_delta
        self.prev_position = self.position
        self.position -= delta_1
        print(self.position)


    def zero(self):
        self.position = 0