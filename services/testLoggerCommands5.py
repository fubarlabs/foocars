import sys, os

import time
import datetime
import picamera
import picamera.array
import numpy as np
import serial
import argparse
import RPi.GPIO as GPIO
import subprocess  
from subprocess import call
import shutil
# import cv2
import threading
import tensorflow as tf
import keras
from enum import Enum     

from dropout_model import model


try:
    ser=serial.Serial('/dev/ttyACM0')
    logging.debug( 'opened serial port' )
    
except Exception as the_bad_news:                
    print( the_bad_news ) 


def getSerialCommandIfAvailable( dontWaitForCommand ):
    global ser
    
    numberOfCharsWaiting = ser.inWaiting()
    
    if( numberOfCharsWaiting == 0 ):
        if( dontWaitForCommand ):
            theResult = commandEnum.NO_COMMAND_AVAILABLE
            return
    
    serial_input_is_no_damn_good = True
    while( serial_input_is_no_damn_good ):        
        try:
            number_of_serial_items = 0
            required_number_of_serial_items = 10
                    
            while( serial_input_is_no_damn_good ):
                ser.flushInput()    # dump partial command
                serial_line_received = ser.readline()
                serial_line_received = serial_line_received.decode("utf-8")
#                logging.debug( 'serial line received = ' + serial_line_received )
#                raw_serial_list = list( str(serial_line_received,'ascii').split(','))    # this seems to throw an error
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
                                logging.debug( 'error converting to float = ' + str( raw_serial_list[ i ]))
                        
                            if( no_conversion_errors ):
                                serial_input_is_no_damn_good = False                            
                            line_not_checked = False
                                        
                    else:        # first test of received line fails 
                        line_not_checked = False
                        logging.debug( 'serial input error: # data items = ' + str( number_of_serial_items  ))
                            
            debugSerialInput = serial_line_received
        
        except Exception as the_bad_news:                
            print( 'Error: receiving command from fubarino' )
    
    return( theCommandList )   
    
         
while ( True ):    
    theCommandList = getSerialCommandIfAvailable( 1 )
    if(theCommandList != 0 ):
        print( theCommandList )