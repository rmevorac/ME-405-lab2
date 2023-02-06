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
            if(line == b''):
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

    datax = array.array('f', [len(databx)])
    datay = array.array('f', [len(databy)])
        
    for i in range(len(datax)):
        datax[i] = float(databx[i])
        datay[i] = float(databy[i])


    plt.plot(datax,datay)
    plt.axis([min(datax),max(datax),min(datay),max(datay)])
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.show()