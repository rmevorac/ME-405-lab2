import pyb, utime
from pyb import Pin as Pin
from encoder_reader import Encoder
from motor_driver import MotorDriver
from controller import Controller

def get_params():
    while True:
        try:
            KP = float(input("Enter a KP: "))
            setpoint = int(input("Enter a setpoint: "))
            return (KP, setpoint)
        except ValueError:
            print("Please enter a valid input")
            
    
if __name__ == "__main__":
    pyb.repl_uart(None)                    # Turn off the REPL on UART2
    u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port
    
    motor1 = MotorDriver(Pin.board.PC1, Pin.board.PA0, Pin.board.PA1, 5)
    encoder1 = Encoder(Pin.board.PB6, Pin.board.PB7, 4)
    updated_params = get_params()
    controller1 = Controller(updated_params[0] , updated_params[1], motor1, encoder1)
    
    while 1:        
        try:
            if controller1.run():
                u2.write(f"{controller1.motor_data[0]}, {controller1.motor_data[1]}\r\n")
            
            if abs(encoder1.position - encoder1.prev_position) <= 2\
                and encoder1.position in range(controller1.setpoint - 50, controller1.setpoint + 50):
                u2.write("end")
                updated_params = get_params()
                controller1.encoder.zero()
                controller1.time = utime.ticks_ms()
                controller1.motor_data = (0, 0)
                controller1.set_KP(updated_params[0])
                controller1.set_setpoint(updated_params[1])
                
        except KeyboardInterrupt:
            motor1.set_duty_cycle(0)
            print("motor shut off")
            print(controller1.motor_data)
            break