import pyb, utime
from encoder_reader import Encoder
from motor_driver import MotorDriver

class Controller:
    def __init__(self, KP, setpoint, motor, encoder):
        self.KP = KP
        self.setpoint = setpoint
        self.motor = motor
        self.encoder = encoder

    def run(self):
        self.motor.set_duty_cycle(self.KP() * (self.setpoint - self.encoder.position))

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_KP(self, KP):
        self.KP = KP



if __name__ == "__main__":
    motor1 = ()
    encoder1 = ()
    controller1 = (1.5, 100, motor1, encoder1)
    pass