"""!
@file main.py
    This file implements the main function for a motor control system. The system consists of a motor, encoder,
    and a controller. The motor is driven by a `MotorDriver` object and the encoder is read by an `Encoder` object.
    The system reads the KP and setpoint values from the decoder (other computer) and updates the motor
    accordingly using the Controller object. The motor data is written to the second USB-serial port.

@author Ben Elkayam
@author Roey Mevorach
@author Ermias Yemane

@date   2023-Feb-10
"""

"""!
@package Python inferface for micro-controller board utilities and tools. Necessary for pin and timer access
"""
import pyb, utime
from pyb import Pin as Pin
from encoder_reader import Encoder
from motor_driver import MotorDriver
from controller import Controller

def get_inputs():
    """!
    @brief      This function reads the user's input for the KP and setpoint values from the decoder.
    @details    The function creates a UART object on port 2 with a baudrate of 115200 and a timeout of 5 seconds.
                It then waits for input from the serial communication and reads the KP and setpoint values.
                Finally, it closes the serial communication and returns a tuple of the KP and setpoint values.
    @param      None
    @return     A tuple of the KP and setpoint values.
    """
    # Set up the USB-serial port
    ser = pyb.UART(2, baudrate=115200, timeout=5)

    while 1:
        if ser.any():
            kp = ser.readlines()
            setpoint = ser.readlines()
            break

    # Close the USB-serial port
    ser.deinit()

    return (kp, setpoint)



if __name__ == "__main__":
    ## Set up the USB-serial port
    u2 = pyb.UART(2, baudrate=115200)
    
    motor1 = MotorDriver(Pin.board.PC1, Pin.board.PA0, Pin.board.PA1, 5)
    encoder1 = Encoder(Pin.board.PB6, Pin.board.PB7, 4)
    updated_params = get_inputs()
    controller1 = Controller(updated_params[0] , updated_params[1], motor1, encoder1)
    
    while 1:        
        try:
            if controller1.run():
                u2.write(f"{controller1.motor_data[0]}, {controller1.motor_data[1]}\r\n")

            ## This code is used for debugging and testing
            # if abs(encoder1.position - encoder1.prev_position) <= 2\
            #     and encoder1.position in range(controller1.setpoint - 50, controller1.setpoint + 50):
            #     u2.write("end")
            #     updated_params = get_inputs()
            #     controller1.encoder.zero()
            #     controller1.time = utime.ticks_ms()
            #     controller1.motor_data = (0, 0)
            #     controller1.set_KP(updated_params[0])
            #     controller1.set_setpoint(updated_params[1])
                
        except KeyboardInterrupt:
            motor1.set_duty_cycle(0)
            print("motor shut off")
            break

    # close the USB-serial port
    u2.deinit()