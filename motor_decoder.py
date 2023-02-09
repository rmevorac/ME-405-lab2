## @file motor_decoder
# @brief This class handles the data coming in from the encoder and parses it for user readability and motor control
## @details
#
# This script contains code for plotting the position data received from a serial port. The data is collected in real-time and sent to the computer via the serial port.
#
# The main function of the script, `if __name__ == "__main__":`, initializes the serial port and receives position data from it. It prompts the user for two input values, the KP and setpoint values, which are sent to the controller via the serial port.
#
# The received position data is processed and plotted using the `matplotlib` library. The data is first read from the serial port and stored in two separate lists, `databx` and `databy`. These lists are then converted to arrays of type `float`, and the values are divided by 1000 to get the data in seconds and rotations.
#
# Finally, the data is plotted with `matplotlib`, with the time data on the x-axis and the position data on the y-axis. The plot is displayed to the user once all the data has been processed.               
# @author Ben Elkayam
# @author Roey Mevorach
# @author Ermias Yemane
# @date	January 1 30 2023
# This file contains code for plotting the position data received from a serial port.
#

import serial
import array
from matplotlib import pyplot as plt

## @brief This function prompts the user to input the KP and setpoint values.
#  The function will continue to prompt the user until a valid input is received.
#  @return A tuple of the KP and setpoint values
#
def get_params():
    while True:
        try:
            KP = float(input("Enter a KP: "))
            setpoint = int(input("Enter a setpoint: "))
            return (str(KP), str(setpoint))
        except ValueError:
            print("Please enter a valid input")

## @brief This function initializes the serial port and receives position data from it.
#  The received data is processed, converted and plotted using matplotlib.
#
if __name__ == "__main__":
    
    ## A list to store the x-axis position data
    databx = []
    ## A list to store the y-axis position data
    databy = []

    with serial.Serial('COM4', 115200) as serSend:
        serSend.flush()
        ## Prompting user for KP and setpoint
        params = get_params()

        ## Sending user input to controller
        serSend.write(f"{params[0]}\r\n".encode())
        serSend.write(f"{params[1]}\r\n".encode())
#<<<<<<< HEAD
        
        serSend.close()
#=======
#>>>>>>> e0903c1f04926ae3f85e405623f2b6211c26c488


    ## Opening the serial port 'COM4' with a baud rate of 115200 and a timeout of 7 seconds
    with serial.Serial('COM4',115200,timeout = 1) as ser:
        ## Flushing the input buffer of the serial port
        ser.flush()
#<<<<<<< HEAD
        
        
#=======
#>>>>>>> e0903c1f04926ae3f85e405623f2b6211c26c488

        ## A loop to continuously read the data from the serial port
        while 1:
            
            ## Reading a line of data from the serial port
            line = ser.readline()

            ## Checking if the line read is equal to 'end'
            if(line == b''):
                print('ended')
                ## Breaking the loop if 'end' is received
                break
            try:
                ## Splitting the received line on ',' to get the x and y position data
                tempx,tempy = (line.strip().split(b','))
                ## Appending the received x and y position data to their respective lists
                databx.append(tempx)
                databy.append(tempy)
                print(tempx)
                print(tempy)
            except:
                ## Printing an error message in case of any error while reading the line

                ## Continuing to the next iteration of the loop
                continue

        print('Stop Reading')


    ## Converting the lists of bytes to arrays of float type
    datax = array.array('f', [0] * len(databx))
    datay = array.array('f', [0] * len(databy))
       
    ## Converting the position data from bytes to float and dividing by 1000 to get the data in seconds and rotations
    ##Fix plotting to zero before submission and last value comes in with paraenthesis 
    for i in range(len(datax)):
        
        datax[i] = float(databx[i])/1000
        datay[i] = float(databy[i])/1000


    ## Plotting the received position data
    plt.plot(datax,datay)
    ## Setting the axis limits of the plot
    plt.axis([min(datax),max(datax),min(datay),max(datay) + 0.5])
    ## Adding a label to the x-axis of the plot
    plt.xlabel("Time (S)")
    ## Adding a label to the y-axis of the plot
    plt.ylabel("Position (Rotations)")
    ## Displaying the plot
    plt.show()