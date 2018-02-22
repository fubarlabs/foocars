import sys, os

import time
import datetime
import serial

gErrorNum = 0

try:
    ser=serial.Serial('/dev/ttyACM0')
    print( 'opened serial port' )
    
except Exception as the_bad_news:                
    print( the_bad_news ) 


def getSerialCommandIfAvailable( dontWaitForCommand ):
    global gErrorNum
    
    numberOfCharsWaiting = ser.inWaiting()
    
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
    
numCommands = 0         
while( numCommands < 100 ):    
    theCommandList = getSerialCommandIfAvailable( 1 )
    if(theCommandList != [] ):
        print( 'the command = ' + str( theCommandList[ 0 ] ) +'  Str = ' + str( theCommandList[ 8 ] ) +'  Thr = ' + str( theCommandList[ 9 ] ))
        numCommands = numCommands + 1
        
print( 'number of errors = ' + str( gErrorNum ))