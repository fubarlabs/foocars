
# Testing ottoMicroLogger Commands

import serial
import time
import sys, os
#import ipdb; ipdb.set_trace()

#ser=serial.Serial('/dev/ttyACM0')          #pi
ser=serial.Serial('/dev/cu.usbmodem1441')   #home mac
#ser=serial.Serial('/dev/cu.usbmodem196')        # work mac
  
time.sleep( .5 )

ser.flushInput()
leftValue = 1700
rightValue = 1300
currValue = leftValue

gNumErrors = 0

def getCommandFromSerial():
    global gNumErrors
    
    command = 0
    try:
        numBytes = ser.in_waiting
        if( numBytes != 0 ):
#                serBytes = ser.read(bytesToRead)
#                print ( 'bytes:' + str( serBytes ))
#                serial_line_received = serBytes.decode('ascii')
#               serial_line_received = serial_line_received.decode("utf-8")
                bytes_received = ser.readline()
                print ( 'bytes received = ' + str( bytes_received ))
                print ( 'number received = ' + str( len( bytes_received )))
                serial_line_received = bytes_received.decode('ascii')    # convert to ascii
                print ( 'ascii received = ' + serial_line_received )
                raw_serial_list = list( serial_line_received.split(','))
                print ( 'command received = ' + str( raw_serial_list[ 0 ]))
                if( len( raw_serial_list ) != 10 ):
                    gNumErrors = gNumErrors + 1
                
                else:
                    command = int( raw_serial_list[ 0 ])
                        
    except Exception as the_bad_news:
        print ( 'exception = ' + str(the_bad_news.args[0]))  
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print ( 'line no. = ' + str(exc_tb.tb_lineno))
    
    return( command )
    
for x in range(1, 102):
    
    command = getCommandFromSerial()
    if( command  == 6 ):
        break
    
    print ('cnt = ' + str( x ))
       
    if( (x % 10 ) == 0 ):
        if( currValue == leftValue ):
            currValue = rightValue
        else:
            currValue = leftValue
            
        dataline='{0}, {1}, {2}, {3}\n'.format( int(5),int(currValue),int(1500),int(0) )
#    ser.flushOutput()
        ser.write(dataline.encode('ascii'))
        print( dataline )
    
    time.sleep(.25)
        
for x in range(1, 10):
    command = getCommandFromSerial()
                       
#	send stop autonomous
dataline='{0}, {1}, {2}, {3}\n'.format( 6,1500,1500,0 )
ser.write(dataline.encode('ascii'))
print( 'number of errors = ' + str( gNumErrors ))
time.sleep( 1)
#ser.close()


