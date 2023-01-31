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
        self.motor_data = [(0,0)]
        self.time = utime.ticks_ms()
        print(f"Creating controller with KP {self.KP} and setpoint {self.setpoint}")

    def run(self):
        self.encoder.read()
        output = self.KP * (self.setpoint - self.encoder.position)
        self.motor.set_duty_cycle(output)
        
        delta_time = utime.ticks_ms() - self.time
        if delta_time >= 25:
            self.time = utime.ticks_ms()
            self.motor_data.append((delta_time + self.motor_data[-1][0], self.encoder.position))
        
        print(self.encoder.position)

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_KP(self, KP):
        self.KP = KP



if __name__ == "__main__":
    motor1 = MotorDriver(Pin.board.PC1, Pin.board.PA0, Pin.board.PA1, 5)
    encoder1 = Encoder(Pin.board.PB6, Pin.board.PB7, 4)
    controller1 = Controller(0.0001 , 3200000, motor1, encoder1)
    
    while 1:
        try:
            controller1.run()
        except KeyboardInterrupt:
            motor1.set_duty_cycle(0)
            print("motor shut off")
            print(controller1.motor_data)
            break
            
