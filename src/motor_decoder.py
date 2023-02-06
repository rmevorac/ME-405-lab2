import serial
from matplotlib import pyplot as plt



if __name__ == "__main__":
    
    databx = []
    databy = []
    datax = []
    datay = []
    with serial.Serial('COM4',115200,timeout = 7) as ser:
        ser.flush()
        
        while 1:
            
            line = ser.readline()
            print(line)
            if(line == b''):
                print('ended')
                break
            try:
                databx,databy =  (line.strip().split(b','))
            except:
                print('error in reading line')
                continue
            
        print('Stop Reading')
        
    for i in range(len(datax)):
        datax[i] = float(databx[i])
    
    for j in range(len(datay)):
        datay[j] = float(databy[j])
    
    


    plt.plot(datax,datay)
    plt.axis([min(datax),max(datax),min(datay),max(datay)])
    plt.xlabel(titles[plotindex])
    plt.ylabel(titles[plotindex+1])
    plt.show()
