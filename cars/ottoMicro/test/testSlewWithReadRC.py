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

gErrorNum=0
echoTestValue = 999

def getSerialCommandIfAvailable( dontWaitForCommand ):
    global gErrorNum
    
    numberOfCharsWaiting = ser.inWaiting()
    print ( numberOfCharsWaiting )
    
    if( numberOfCharsWaiting == 0 ):
        if( dontWaitForCommand ):
            theCommandList = []
            return( theCommandList )
    
    serial_input_is_no_damn_good = True
    while( serial_input_is_no_damn_good ):        
        try:
            number_of_serial_items = 0
            required_number_of_serial_items = 10
                    
            while( serial_input_is_no_damn_good ):
                ser.flushInput()    # dump partial command
                serial_line_received = ser.readline()
                serial_line_received = serial_line_received.decode("ascii")
                raw_serial_list = list( serial_line_received.split(','))
                
                theCommandList = []             
                number_of_serial_items = len( raw_serial_list )
                line_not_checked = True
            
                while( line_not_checked ):
                    if( number_of_serial_items == required_number_of_serial_items ):
                
                        no_conversion_errors = True
                        for i in range( 0, required_number_of_serial_items ):
                            try:
                                theCommandList.append( float( raw_serial_list[ i ]))
                            except ValueError:
                                no_conversion_errors = False
                                gErrorNum = gErrorNum + 1
                        
                            if( no_conversion_errors ):
                                serial_input_is_no_damn_good = False                            
                            line_not_checked = False
                                        
                    else:        # first test of received line fails 
                        line_not_checked = False
                        print( 'serial input error: # data items = ' + str( number_of_serial_items  ))
                            
            debugSerialInput = serial_line_received
        
        except Exception as the_bad_news:                
            print( the_bad_news )
    
    return( theCommandList )   

for x in range(0, 5):
    dataline='{0}, {1}, {2}, {3}\n'.format( 5,1300,1500,0 )
    ser.write(dataline.encode('ascii'))
    time.sleep(.5)
    dataline='{0}, {1}, {2}, {3}\n'.format( 5,1700,1500,0 )
    ser.write(dataline.encode('ascii'))
    time.sleep(.5)
    
    theCommandList = getSerialCommandIfAvailable( 1 )
    if(theCommandList != [] ):
        print( theCommandList )
        print( theCommandList[ 0 ] )
        
    if( theCommandList[ 0 ] == 6 ):
        if( theCommandList[ 1 ] == echoTestValue ):
            print( 'Echoed 6' )
        else: 
            break 
    print( x )
       
#	send stop autonomous
dataline='{0}, {1}, {2}, {3}\n'.format( 6,1500,1500,0 )
ser.write(dataline.encode('ascii'))
time.sleep( 1)
ser.close()