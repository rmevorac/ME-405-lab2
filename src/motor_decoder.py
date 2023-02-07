"""!@file		encoder_reader.py
    @brief		This class handles the data coming in from the encoder and parses it for user readability and motor control
                
    
    @author		Ben Elkayam
    @author		Roey Mevorach
    @author		Ermias Yemane
    @date		January 2 6 2023


"""
"""
@package
"""

import serial
import array
from matplotlib import pyplot as plt


if __name__ == "__main__":
    
    databx = []
    databy = []

    with serial.Serial('COM4',115200,timeout = 7) as ser:
        ser.flush()
        
        while 1:
            
            line = ser.readline()
            print(line)
            if(line == b'end'):
                print('ended')
                break
            try:
                tempx,tempy = (line.strip().split(b','))
                databx.append(tempx)
                databy.append(tempy)
            except:
                print('error in reading line')
                continue

        print('Stop Reading')


    
    datax = array.array('f', [0] * len(databx))
    datay = array.array('f', [0] * len(databy))
       
    for i in range(len(datax)):
        datax[i] = float(databx[i])/1000
        datay[i] = float(databy[i])/1000


    plt.plot(datax,datay)
    plt.axis([min(datax),max(datax),min(datay),max(datay)])
    plt.xlabel("Time (S)")
    plt.ylabel("Position (Rotations)")
    plt.show()