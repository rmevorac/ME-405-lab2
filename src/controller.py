"""!
@file controller.py
    This file contains a Controller class which is used for controlling the
    position of a motor using an encoder and a motor driver.

@author Ben Elkayam
@author Roey Mevorach
@author Ermias Yemane

@date   2023-Feb-10
"""
import pyb, utime
from pyb import Pin as Pin
from encoder_reader import Encoder
from motor_driver import MotorDriver


class Controller:
    '''!
    @class      Controller
    @brief      A control system for positioning a motor using feedback from an encoder and a motor driver.
    @details    The Controller class implements a control loop that uses an Encoder object to get feedback
                on the position of a motor and a MotorDriver object to control the motor. It has methods
                for setting the target position and the proportional gain of the control loop, as well as a
                method for running the control loop and updating the motor's position.
    '''

    def __init__(self, kp, setpoint, motor, encoder):
        '''!
        @brief      Create a controller object.
        @details    The constructor method initializes the Controller object with the given proportional gain kp,
                    target position setpoint, MotorDriver object motor, and Encoder object encoder. It also initializes
                    the motor_data attribute as a tuple of (0,0), the time attribute as the current time in milliseconds,
                    and prints a message indicating that the Controller object has been created with the given kp and setpoint.
        @param      self The object itself
        @param      kp Proportional gain
        @param      setpoint Target position for the motor
        @param      motor MotorDriver object
        @param      encoder Encoder object
        @return     None
        '''
        self.kp = kp
        self.setpoint = setpoint
        self.motor = motor
        self.encoder = encoder
        self.motor_data = (0,0)
        self.time = utime.ticks_ms()
        print(f"Creating controller with KP {self.kp} and setpoint {self.setpoint}")

    def run(self):
        '''!
        @brief      Runs the controller.
        @details    Reads the encoder position, calculates the control output using a proportional control law,
                    and sets the duty cycle of the motor. The method also updates the motor data and returns
                    a flag indicating if the motor data has been updated.
        @param      self The object itself
        @return     A flag indicating if the motor data has been updated (0 or 1).
        '''
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

    def set_setpoint(self, setpoint):
        """!
        @brief      Method to set the target position for the motor.
        @details    This method takes in a setpoint parameter and updates the target position of the motor.
        @param      self The object itself
        @param      setpoint Target position for the motor
        @return     None
        """
        self.setpoint = setpoint

    def set_kp(self, kp):
        '''!
        @brief      Set the proportional gain.
        @details    This method updates the proportional gain of the controller.
        @param      self The object itself
        @param      kp Proportional gain
        @return     None
        '''
        self.kp = kp