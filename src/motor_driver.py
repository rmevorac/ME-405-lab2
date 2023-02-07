## @file

import pyb
from pyb import Pin as Pin

# yellow (channel A) leads for clockwise
# Blue (channel B) leads for clockwise

class MotorDriver:
    ## @brief This class is used to control a motor using the Pyboard and its pins.
    #
    def __init__ (self, en_pin, in1pin, in2pin, timer_num):
        ## Initialize the pin objects for the enable, input 1 and input 2 pins of the motor.
        pin1 = Pin(in1pin, Pin.OUT_PP)
        pin2 = Pin(in2pin, Pin.OUT_PP)
        timer = pyb.Timer(timer_num, freq=0xFFFF)
        self.pin_en = Pin(en_pin, Pin.OUT_OD, Pin.PULL_UP)
        self.ch1 = timer.channel(1, pyb.Timer.PWM, pin=pin1)
        self.ch2 = timer.channel(2, pyb.Timer.PWM, pin=pin2)
        print("Creating a motor driver")

    ## @brief This function sets the duty cycle of the PWM signal applied to the motor to control its speed.
    #  @param level The duty cycle of the PWM signal as a percentage (-100 to 100).
    #
    def set_duty_cycle (self, level):
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
