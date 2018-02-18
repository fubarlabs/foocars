# Testing ottoMicroLogger Commands

import serial
import time

# Opens serial port to the arduino:
ser=serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS        #number of bits per bytes
ser.parity = serial.PARITY_NONE        #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE     #number of stop bits
time.sleep( .1)

for x in range(0, 3):
      # spaces after the commas throw an error
#      dataline='{0}, {1}, {2}, {3}\n'.format( 5, 1300, 1500, 0)
      dataline='{0}, {1}, {2}, {3}\n'.format( 5,1300,1500,0 )
      ser.write(dataline.encode('ascii'))
      time.sleep( 1)
      dataline='{0}, {1}, {2}, {3}\n'.format( 5,1700,1500,0 )
      ser.write(dataline.encode('ascii'))
      time.sleep( 1)

#	send stop autonomous
dataline='{0}, {1}, {2}, {3}\n'.format( 6,1500,1500,0 )
ser.write(dataline.encode('ascii'))
time.sleep( 1)
ser.close()
