import serial

with serial.Serial('COM4',115200) as ser:
    ser.flush()
    while True:
        try:
          print (ser.readline().split(b','))
        except:
            print('error')
