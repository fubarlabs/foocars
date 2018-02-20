
# Testing ottoMicroLogger Commands

import serial
import time

#ser=serial.Serial('/dev/ttyACM0')          #pi
ser=serial.Serial('/dev/cu.usbmodem1411')   #home mac
	
    
time.sleep( .5 )

for x in range(0, 10):
    dataline='{0}, {1}, {2}, {3}\n'.format( int(5),int(1300),int(1500),int(0) )
    ser.write(dataline.encode('ascii'))
    time.sleep(.25)
    dataline='{0}, {1}, {2}, {3}\n'.format( 5,1700,1500,0 )
    ser.write(dataline.encode('ascii'))
    time.sleep( .25)
    bytesToRead = ser.inWaiting()
    if( bytesToRead > 0 ):
        serBytes = ser.read(bytesToRead)
        print ( bytesToRead )
        serial_line_received = serBytes.decode('ascii')
#       serial_line_received = serial_line_received.decode("utf-8")
        raw_serial_list = list( serial_line_received.split(','))
        command = raw_serial_list[ 0 ]
        print ( command )
        if( command == 6 ):
            break
#	send stop autonomous
dataline='{0}, {1}, {2}, {3}\n'.format( 6,1500,1500,0 )
ser.write(dataline.encode('ascii'))
time.sleep( 1)
ser.close()


