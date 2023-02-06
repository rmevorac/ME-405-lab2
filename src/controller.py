import pyb, utime
from pyb import Pin as Pin
from encoder_reader import Encoder
from motor_driver import MotorDriver

class Controller:
    def __init__(self, KP, setpoint, motor, encoder):
        self.KP = KP
        self.setpoint = setpoint
        self.motor = motor
        self.encoder = encoder
        self.motor_data = (0,0)
        self.time = utime.ticks_ms()
        print(f"Creating controller with KP {self.KP} and setpoint {self.setpoint}")

    def run(self):
        flag = 0
        
        delta_time = utime.ticks_ms() - self.time
        if delta_time >= 10:
            self.encoder.read()
            output = self.KP * (self.setpoint - self.encoder.position)
            self.motor.set_duty_cycle(output)
            
            self.time = utime.ticks_ms()
            self.motor_data = (delta_time + self.motor_data[0], self.encoder.position)
            flag = 1
        
        return flag

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_KP(self, KP):
        self.KP = KP

            
