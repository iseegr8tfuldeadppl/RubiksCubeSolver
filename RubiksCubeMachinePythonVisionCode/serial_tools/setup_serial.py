from serial import Serial
from serial import EIGHTBITS
from serial import PARITY_NONE
from serial import STOPBITS_ONE

def Setup_serial(port='COM4'):

    done = False
    while done==False:
        try:
            ser = Serial(
            port = port,
            baudrate = 9600,
            bytesize = EIGHTBITS,
            parity = PARITY_NONE,
            stopbits = STOPBITS_ONE,
            timeout = 1,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False,
            writeTimeout = 2
            )
            if(ser.isOpen() == False):
                ser.open()
            else:
                done = True
                print('Connected')
                return ser
        except IOError:
          pass
