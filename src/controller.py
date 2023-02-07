## @file
#  This file contains the Controller class definition
#

import pyb, utime
from pyb import Pin as Pin
from encoder_reader import Encoder
from motor_driver import MotorDriver

## @brief Class for controlling the position of a motor using an encoder and a motor driver
#
class Controller:
    ## @brief Constructor method for the Controller class
    #  @param kp Proportional gain
    #  @param setpoint Target position for the motor
    #  @param motor MotorDriver object
    #  @param encoder Encoder object
    #
    def __init__(self, kp, setpoint, motor, encoder):
        self.kp = kp
        self.setpoint = setpoint
        self.motor = motor
        self.encoder = encoder
        self.motor_data = (0,0)
        self.time = utime.ticks_ms()
        print(f"Creating controller with KP {self.kp} and setpoint {self.setpoint}")

    ## @brief Method for running the controller
    #  @return flag indicating whether the motor data has been updated
    #
    def run(self):
        flag = 0
        
        delta_time = utime.ticks_ms() - self.time
        if delta_time >= 10:
            self.encoder.read()
            output = self.kp * (self.setpoint - self.encoder.position)
            self.motor.set_duty_cycle(output)
            
            self.time = utime.ticks_ms()
            self.motor_data = (delta_time + self.motor_data[0], self.encoder.position)
            flag = 1
        
        return flag

    ## @brief Method for setting the target position for the motor
    #  @param setpoint Target position for the motor
    #
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    ## @brief Method for setting the proportional gain
    #  @param kp Proportional gain
    #
    def set_kp(self, kp):
        self.kp = kp
