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
            echoed_number_of_serial_items = 4
                    
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
                                        
                    elif( number_of_serial_items == echoed_number_of_serial_items ):
                        serial_input_is_no_damn_good = False                            
                        
                    else:        # first test of received line fails 
                        line_not_checked = False
                        print( 'serial input error: # data items = ' + str( number_of_serial_items  ))
                        print( 'serial line received = ' + serial_line_received )
                            
            debugSerialInput = serial_line_received
        
        except Exception as the_bad_news:                
            print( the_bad_news )
    
    return( theCommandList ) 
 
leftValue = 1300   
rightValue = 1700   
currValue = leftValue 
echoTestValue = 999 
  
cnt = 1

while( cnt < 101 ):    
    theCommandList = getSerialCommandIfAvailable( 1 )
    if(theCommandList != [] ):
    
        if( theCommandList[ 0 ] == 6 ):
            if( theCommandList[ 1 ] == echoTestValue ):
                print( 'Echoed 6' )
            else: 
                break
    
        print ('cnt = ' + str( cnt ))
       
        if(( cnt % 10 ) == 0 ):
            if( currValue == leftValue ):
                currValue = rightValue
            else:
                currValue = leftValue
            
            #   the following will turn on autonomous if not followed by another write
            #   an RC reversal will cause break from loop
            dataline='{0},{1},{2},{3}\n'.format( int(5),int(currValue),int(1500),int(0) )
            ser.write(dataline.encode('ascii'))
#            ser.write('5,1300,1500,0'.encode('ascii'))         #  this causes the same behaviour
            
            print( 'start auto' )
            time.sleep(10)
            
#            theCommandList = getSerialCommandIfAvailable( 1 )
            
#            ser.write('6,1300,1500,0'.encode('ascii'))
#            time.sleep(.25)
#            dataline='{0},{1},{2},{3}\n'.format( int(6),int(echoTestValue),int(echoTestValue),int(echoTestValue) )
#            ser.write(dataline.encode('ascii'))
#            print( 'stop auto' )
        cnt = cnt + 1
        
                       
#	send stop autonomous
dataline='{0}, {1}, {2}, {3}\n'.format( 6,1500,1500,0 )
ser.write(dataline.encode('ascii'))
        
print( 'number of errors = ' + str( gErrorNum ))

time.sleep( 1)
ser.close()



