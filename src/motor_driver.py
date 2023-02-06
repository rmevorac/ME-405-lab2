"""! @file lab1.py Motor Driver  """
import pyb
from pyb import Pin as Pin


# yellow (channel A) leads for clockwise
# Blue (channel B) leads for clockwise

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer_num):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several pin parameters)
        """
        pin1 = Pin(in1pin, Pin.OUT_PP)
        pin2 = Pin(in2pin, Pin.OUT_PP)
        timer = pyb.Timer(timer_num, freq=0xFFFF)
        self.pin_en = Pin(en_pin, Pin.OUT_OD, Pin.PULL_UP)
        self.ch1 = timer.channel(1, pyb.Timer.PWM, pin=pin1)
        self.ch2 = timer.channel(2, pyb.Timer.PWM, pin=pin2)
        print("Creating a motor driver")
        
    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        self.pin_en.value(1)

        if level < 0:
            self.ch1.pulse_width_percent(-1 * level)
            self.ch2.pulse_width_percent(0)
        elif level > 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(level)
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
            
#         print (f"Setting duty cycle to {level}")