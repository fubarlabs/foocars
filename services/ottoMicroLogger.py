#!/usr/bin/python3

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

import logging
logging.basicConfig(filename='/tmp/ottoMicroLogger.log',level=logging.DEBUG)
logging.debug( '\n\n new session \n' )
logging.debug( 'setting up model ')

# -------- New Power On/Off functionality --------- 

# 1- User holds boot switch in ON position which energizes power relay coil ( power LED remains unlit )
# 2- Relay contacts close supplying 5 volts to Pi.
# 3- Pi boots, executes service program which also energizes relay coil
# 4- Pi turns on power LED to indicate to user that the Pi is under control
# 5- User releases toggle switch, but Pi has already latched relay contacts closed so it remains powered
# 6- Program continues to execute until user flips power off switch telling Pi to shut it down

#    CONSTANTS are in ALL CAPS

# -------- GPIO pin numbers for ottoMicro Car --------- 
LED_read_from_laptop = 2
LED_save_to_laptop = 3
LED_collect_data = 4
LED_autonomous = 17
LED_shutdown_RPi = 27
LED_boot_RPi = 22

SWITCH_collect_data = 10
SWITCH_save_to_laptop = 9
SWITCH_read_from_laptop = 11
SWITCH_autonomous = 5
SWITCH_shutdown_RPi = 6
# SWITCH_boot_RPi -> daughter board relay coil

OUTPUT_to_relay = 13

DEFAULT_AUTONOMOUS_THROTTLE = 1580

# -------- Switch constants --------- 
# switch position-UP connects GPIO pin to GROUND, 
#  thus internal pull up  resistors are used  
#  and LOW and HIGH signals are opposite to usual ON and OFF conventions
SWITCH_UP = GPIO.LOW        # LOW signal on GPIO pin means switch is in up position        
SWITCH_DOWN = GPIO.HIGH        # HIGH signal on GPIO pin means switch is in down position

# -------- LED state constants --------- 
LED_ON = GPIO.HIGH
LED_OFF = GPIO.LOW

# -------- Relay state constants --------- 
RELAY_ON = GPIO.HIGH
RELAY_OFF = GPIO.LOW

# -------- Command enumeration same as ones on fubarino --------- 
def enum(**enums):
    return type('Enum', (), enums)
       
commandEnum = enum(  
    NOT_ACTUAL_COMMAND = 0,
    RC_SIGNAL_WAS_LOST = 1,
    RC_SIGNALED_STOP_AUTONOMOUS = 2,
    STEERING_VALUE_OUT_OF_RANGE = 3,
    THROTTLE_VALUE_OUT_OF_RANGE= 4,
    RUN_AUTONOMOUSLY = 5,
    STOP_AUTONOMOUS = 6,
    STOPPED_AUTO_COMMAND_RECEIVED = 7,
    NO_COMMAND_AVAILABLE = 8,
    GOOD_PI_COMMAND_RECEIVED = 9,
    TOO_MANY_VALUES_IN_COMMAND = 10,
    GOOD_RC_SIGNALS_RECEIVED = 11 
    )

# --------Old Data Collection Command Line Startup Code--------- 
time_format='%Y-%m-%d_%H-%M-%S'

#    **** fubarino not connected yet for debugging purposes ****
#    Opens serial port to the arduino:
try:
    ser=serial.Serial('/dev/ttyACM0')
    logging.debug( 'opened serial port' )
    
except Exception as the_bad_news:                
    handle_exception( the_bad_news ) 
    
    
# -------------- Data Getter Object -------------------------------  
class DataGetter(object):
    def __init__(self):
        pass

    def write(self, s):
        global g_image_data
        imagerawdata=np.reshape(np.fromstring(s, dtype=np.uint8), (96, 128, 3), 'C')
        imdata=imagerawdata[0:78, :]
        immean=imdata.mean()
        imvar=imdata.std()
        g_lock.acquire()
        g_image_data=np.copy((imdata-immean)/imvar)
        g_lock.release()

    def flush(self):
        pass

# -------------- Image Processor Function -------------------------------  
def imageprocessor(event):
    global g_image_data
    global g_graph
    global g_steerstats
    
    with g_graph.as_default():
        time.sleep(1)
        while not event.is_set():
            g_lock.acquire()
            tmpimg=np.copy(g_image_data)
            g_lock.release()
            immean=tmpimg.mean()
            imvar=tmpimg.std()
            print('{0}, {1}'.format(immean, imvar))
            start=time.time()
            pred=model.predict(np.expand_dims(tmpimg, axis=0))
            end=time.time()
            if(end-start)<.2:
                time.sleep(.2-(end-start))
            end2=time.time()                
            steer_command=pred[0][0]*g_steerstats[1]+g_steerstats[0]
            #    !!! must have one space after comma !!!
            dataline='{0}, {1}, {2}, {3}\n'.format( int(commandEnum.RUN_AUTONOMOUSLY ),int( steer_command ),int( DEFAULT_AUTONOMOUS_THROTTLE ),int(0) )
            print(dataline)
            
            commandEnum.NO_COMMAND_AVAILABLE 
            theCommandList = getSerialCommandIfAvailable( 1 )
            
            try:
                ser.write(dataline.encode('ascii'))
                logging.debug( 'autonomous command: ' + str( dataline ))

            except Exception as the_bad_news:                
                 handle_exception( the_bad_news )
                 
            print( theCommandList )
            
            if( theCommandList[ 0 ] == 6 ):
                if( theCommandList[ 1 ] == echoTestValue ):
                    print( 'Echoed 6' )
                else: 
                    stop_autonomous()

# ------------------------------------------------- 
def stop_autonomous():  
    global g_Recorded_Data_Not_Saved
    global g_Wants_To_See_Video
    global g_Is_Autonomous
    global g_Camera_Is_Recording
    global g_camera
    global g_getter
    global g_stop_event
    global g_ip_thread
    
    try:
        if ( g_Wants_To_See_Video ):
            g_camera.stop_preview()
        g_camera.stop_recording()            
        g_stop_event.set()
        logging.debug( 'OK: autonomous complete' )

    except Exception as the_bad_news:                
        handle_exception( the_bad_news )
        logging.debug( 'NG: autonomous problem' )
        
    finally:
        g_Camera_Is_Recording = False
        g_Recorded_Data_Not_Saved = True
        turn_OFF_LED( LED_autonomous )
        logging.debug( 'exiting autonomous\n' )
        
        # blink LEDs as an alarm if autonmous switch has been left up
        LED_state = LED_ON

        while( GPIO.input( SWITCH_autonomous ) == SWITCH_UP ): 
            GPIO.output( LED_autonomous, LED_state )
            time.sleep( .25 )
            LED_state = LED_state ^ 1        # XOR bit to turn LEDs off or on

        # turn off all LEDs for initialization
        turn_OFF_all_LEDs()
        
# ------------------------------------------------- 
def callback_switch_autonomous( channel ):  
    global g_Recorded_Data_Not_Saved
    global g_Wants_To_See_Video
    global g_Is_Autonomous
    global g_Camera_Is_Recording
    global g_camera
    global g_getter
    global g_stop_event
    global g_ip_thread

    if( GPIO.input( SWITCH_autonomous ) == SWITCH_UP ):
        if( g_Is_Autonomous == False ):
            try:
                turn_ON_LED( LED_autonomous )
                g_camera.start_recording( g_getter, format='rgb' )
                g_ip_thread=threading.Thread(target=imageprocessor, args=[g_stop_event])
                g_ip_thread.start()
                g_Camera_Is_Recording = True
                g_Is_Autonomous = True
                logging.debug( '* in autonomous mode, camera is recording' )
                if ( g_Wants_To_See_Video ):
                    g_camera.start_preview() #displays video while it's being recorded

            except Exception as the_bad_news:                
                handle_exception( the_bad_news )
        else:
            logging.debug( '* warning: while recording, ANOTHER RISING transition on the autonomous switch' )
        
    else:    # a autonomous data switch down position has occurred        
        if( g_Is_Autonomous == True ):
            logging.debug( '* autonomous switch is now down' )
            stop_autonomous()
            g_ip_thread.join()
        else:
            logging.debug( '* warning: while recording, ANOTHER FALLING transition on the autonomous switch' )
            
# -------------- Data Collector Object -------------------------------  
NUM_FRAMES = 100

class DataCollector(object):
    '''this object is passed to the camera.start_recording function, which will treat it as a 
            writable object, like a stream or a file'''
    def __init__(self):
        self.imgs=np.zeros((NUM_FRAMES, 96, 128, 3), dtype=np.uint8) #we put the images in here
        self.IMUdata=np.zeros((NUM_FRAMES, 7), dtype=np.float32) #we put the imu data in here
        self.RCcommands=np.zeros((NUM_FRAMES, 2), dtype=np.float16) #we put the RC data in here
        self.idx=0 # this is the variable to keep track of number of frames per datafile
        
        self.debugSerialInput = ""    # save last serial input so we can print it out 
        
        nowtime=datetime.datetime.now()
        
        try:        #   reorganize the data collection folder
            not_done_renumbering_collected_folders = True
            maximum_folder_index = 9
            path = '/home/pi/autonomous/data/collected_data'
            path_with_index = path + str( maximum_folder_index )     # does a folder exist with the maximum index?
            if( os.path.exists( path_with_index )):
                shutil.rmtree( path_with_index, ignore_errors=True)    # get rid of the last folder (even if the files inside are not read only)
            
            folder_index = maximum_folder_index - 1         # start looking for a folder with one less than the maximum index                
            while( not_done_renumbering_collected_folders ):
                old_folder_path = path + str( folder_index )
                new_folder_path = path + str( folder_index + 1 )
            
                if( os.path.exists( old_folder_path )):
                    os.rename( old_folder_path, new_folder_path )
                    logging.debug( 'old folder = ' + old_folder_path + '  new folder = ' + new_folder_path )
                
                folder_index = folder_index - 1
                if( folder_index < 0 ):
                    not_done_renumbering_collected_folders = False
                
            self.path_with_index = path + '0'
            if( os.path.exists( path_with_index == False )):
                os.makedirs( self.path_with_index )
                                
            logging.debug( 'collected data path = ' + self.path_with_index )
        
        except Exception as the_bad_news:                
            handle_exception( the_bad_news )
            logging.debug( 'self.idx = ' + str( self.idx ))
            logging.debug( 'Error: exception in data collection folder reorg' )
       
        self.img_file = self.path_with_index + '/imgs_{0}'.format(nowtime.strftime(time_format))
        self.IMUdata_file = self.path_with_index + '/IMU_{0}'.format(nowtime.strftime(time_format))
        self.RCcommands_file = self.path_with_index + '/commands_{0}'.format(nowtime.strftime(time_format))

    def write(self, s):
        '''this is the function that is called every time the PiCamera has a new frame'''
        imdata=np.reshape(np.fromstring(s, dtype=np.uint8), (96, 128, 3), 'C')
                        
        try:
            # !!!!!!!!!   This will be an INFINITE LOOP if either the RC or ESC is off    !!!!!!!!
            dontWaitForCommand = False    #  Keep waiting for a good command
            theCommandList = getSerialCommandIfAvailable( dontWaitForCommand )
            logging.debug( 'serial command: ' + str( theCommandList ))
            
            #Note: the data from the IMU requires some processing which does not happen here:
            self.imgs[self.idx]=imdata
            accelData=np.array([theCommandList[1], theCommandList[2], theCommandList[3]], dtype=np.float32)
            gyroData=np.array([theCommandList[4], theCommandList[5], theCommandList[6]], )
            datatime=np.array([int(theCommandList[7])], dtype=np.float32)
            steering_value=int(theCommandList[8])
            throttle_value=int(theCommandList[9])
            self.IMUdata[self.idx]=np.concatenate((accelData, gyroData, datatime))
            self.RCcommands[self.idx]=np.array([steering_value, throttle_value])
            self.idx+=1
            
            if ((self.idx % 20 ) == 0 ):     # blink the LED everytime 20 frames are recorded
                turn_OFF_LED( LED_collect_data )
                time.sleep( .2)
                turn_ON_LED( LED_collect_data )

            if self.idx == NUM_FRAMES: #default value is 100, unless user specifies otherwise
                self.flush()  
            
        except Exception as the_bad_news:                
            handle_exception( the_bad_news )
            logging.debug( 'self.idx = ' + str( self.idx ))
            logging.debug( 'Error: exception in data collection write' )

    def flush(self):
        '''this function is called every time the PiCamera stops recording'''
        np.savez(self.img_file, self.imgs)
        np.savez(self.IMUdata_file, self.IMUdata)
        np.savez(self.RCcommands_file, self.RCcommands)
        #this new image file name is for the next chunk of data, which starts recording now
        nowtime=datetime.datetime.now()
        self.img_file = self.path_with_index + '/imgs_{0}'.format(nowtime.strftime(time_format))
        self.IMUdata_file = self.path_with_index + '/IMU_{0}'.format(nowtime.strftime(time_format))
        self.RCcommands_file = self.path_with_index + '/commands_{0}'.format(nowtime.strftime(time_format))
        self.imgs[:]=0
        self.IMUdata[:]=0
        self.RCcommands[:]=0
        logging.debug( 'OK: camera flush, frame index = ' + str( self.idx ))
        self.idx=0
        
# ------------------------------------------------- 
def callback_switch_collect_data( channel ):  
    global g_Recorded_Data_Not_Saved
    global g_Wants_To_See_Video
    global g_Camera_Is_Recording
    global g_camera
    global g_collector
        
    if( GPIO.input( SWITCH_collect_data ) == SWITCH_UP ):
        if( g_Camera_Is_Recording == False ):
            try:
                turn_ON_LED( LED_collect_data )
                
                g_collector=DataCollector()
                
                g_collector.idx = 0        # just in case it wasn't zeroed by flush routine                
                g_camera.start_recording( g_collector, format='rgb' )
                g_Camera_Is_Recording = True
                logging.debug( '* in collect mode, camera is recording' )
                if ( g_Wants_To_See_Video ):
                    g_camera.start_preview() #displays video while it's being recorded

            except Exception as the_bad_news:                
                handle_exception( the_bad_news )
            
        else:
            logging.debug( '* warning: while recording, ANOTHER RISING transition on the collect switch' )
        
    else:    # a collect data switch down position has occurred        
        if( g_Camera_Is_Recording == True ):
            logging.debug( '* collect switch is now down' )
            try:
                if ( g_Wants_To_See_Video ):
                    g_camera.stop_preview()
                g_camera.stop_recording()            
                logging.debug( 'OK: Camera recorded' )

            except Exception as the_bad_news:                
                handle_exception( the_bad_news )
                logging.debug( 'NG: Camera NOT recorded' )
                
            finally:
                g_Camera_Is_Recording = False
                g_Recorded_Data_Not_Saved = True
                turn_OFF_LED( LED_collect_data )
                logging.debug( 'exiting collect data\n' )

        else:
            logging.debug( '* warning: while recording, ANOTHER FALLING transition on the collect switch' )
            


# -------- Switch / Button use cheatsheet --------- 
#
# Switch / Button        STATE        MEANING
# --------------------------------------------------------------
# SWITCH_boot_RPi        up        Energize power relay to Pi -> Boot Pi        
#                down        normal RPi operation
#
# SWITCH_shutdown_RPi        momentary up    Tried to shutdown Pi, if Data folder unsaved, blink all LEDs as warning
#                        otherwise go through normal shutdown
#    after warning LEDs blinking:                    
#                up, but not held    go back to normal RPi operation
#                up, and held    go through shutdown without saving Data folder
#
# SWITCH_autonomous        up        Put car in autonomous mode
#                down        normal RPi operation
#
# SWITCH_collect_data        up        Start collecting data
#                down        Stop collection data if doing that        
#
# SWITCH_save_to_laptop    momentary up    Copy collected data to USB drive
#                down        normal RPi operation
#
# SWITCH_read_from_laptop    momentary up    Read training data to from USB drive
#                down        normal RPi operation
#

# -------- LED status cheatsheet --------- 
#    on startup:
# autonomous LED blinking on startup            autonomous switch was left in the up position
# collect data LED blinking on startup            collect data switch was left in the up position

#    in normal operation:
# all LEDs blinking                    Tried to shutdown without first saving Data folder
# read and save LEDs blinking together            USB drive not mounted - insert or remove and insert USB drive

# -------- Wait or Not for a good command list from Fubarino --------
#    read from the serial port and format and save the data:
#      There are a few problems that can arise if the serial buffer happens to be flushed in the midst of receiving a line:
#       1- the serial line received can be only partially received
#       2- the number of data items in that partial line is less than the required number
#       3- the number of items is correct, but one of data items is not whole and cannot be converted into a float
#      So, if any of those errors are detected, the line is discarded and the next line received is tested

#----------- Wait or Not for a serial command from the fubarino -------------
#    return with a list of 10 FLOATS: the command and then 9 data values
def getSerialCommandIfAvailable( dontWaitForCommand ):
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
            handle_exception( the_bad_news )
            logging.debug( 'Error: receiving command from fubarino' )
    
    return( theCommandList )        

# -------- LED functions to make code clearer --------- 
def turn_ON_LED( which_LED ):
    GPIO.output( which_LED, LED_ON )

def turn_OFF_LED( which_LED ):
    GPIO.output( which_LED, LED_OFF )    
    
def at_least_one_momentary_switch_is_up():
    if(( GPIO.input( SWITCH_save_to_laptop ) == SWITCH_UP ) or ( GPIO.input( SWITCH_read_from_laptop ) == SWITCH_UP ) 
            or ( GPIO.input( SWITCH_shutdown_RPi ) == SWITCH_UP )):    
        return True
    else:
        return False
        
def all_switches_are_down():
    if(( GPIO.input( SWITCH_save_to_laptop ) == SWITCH_UP ) or ( GPIO.input( SWITCH_autonomous ) == SWITCH_UP )
            or ( GPIO.input( SWITCH_read_from_laptop ) == SWITCH_UP ) or ( GPIO.input( SWITCH_shutdown_RPi ) == SWITCH_UP )
            or ( GPIO.input( SWITCH_collect_data ) == SWITCH_UP )):
        return False
    else:
        return True
                
# -------- Handler for clearing all switch errors --------- 
def handle_exception( the_bad_news ):
    global g_Current_Exception_Not_Finished

    if( g_Current_Exception_Not_Finished ):
        logging.debug( '*** another exception occurred, last exception not finished' )        
    else: 
        logging.debug( '\n' )        
        logging.debug( '*** Exception occurred' )        
        g_Current_Exception_Not_Finished = True
        if( len(the_bad_news.args) == 1 ):        # one argument exceptions are unforeseen 
            error_number = 15
            message = the_bad_news.args[0]
            logging.debug( str(the_bad_news.args[0]))
            
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.debug(' line number = ' + str(exc_tb.tb_lineno))
        else:                    # two argument exceptions are previously setup to be handled
            error_number = the_bad_news.args[0]
            message = the_bad_news.args[1]            
            logging.debug( 'error number = ' + str(the_bad_news.args[0]) + ': ' + str(the_bad_news.args[1]))
            
        blinkSpeed = .2
        switch_on_count = 3
        
        # blink the error number in the LEDs until the user holds down the button for 3 seconds
        LED_state = LED_ON
        error_not_cleared = True
        if( error_number > 31 ):    # bigger than this, we've run out of LEDs
            error_number = 31
            
        while( error_not_cleared ):    
            if( at_least_one_momentary_switch_is_up()):    # holding any momentary switch up for long enough will clear error
                switch_on_count = switch_on_count - 1
                if( switch_on_count <= 0 ):
                    error_not_cleared = False            
            if( LED_state == LED_ON ):        # put error_number in binary on the LEDs    
                LED_state = error_number & 0b00001
                GPIO.output( LED_read_from_laptop, LED_state )
                LED_state = ( error_number & 0b00010 ) >> 1
                GPIO.output( LED_save_to_laptop, LED_state )
                LED_state = ( error_number & 0b00100 ) >> 2
                GPIO.output( LED_collect_data, LED_state )
                LED_state = ( error_number & 0b01000 ) >> 3
                GPIO.output( LED_autonomous, LED_state )
                LED_state = ( error_number & 0b10000 ) >> 4
                GPIO.output( LED_shutdown_RPi, LED_state )
                LED_state = LED_OFF    
            else:
                turn_OFF_all_LEDs_except_BOOT()    
                LED_state = LED_ON    
            
            time.sleep( blinkSpeed )

        turn_OFF_all_LEDs_except_BOOT()        # show the user the error has been cleared
    
        # don't leave until we're sure user released button    
        while True:
            time.sleep( blinkSpeed )        # executes delay at least once
            if ( all_switches_are_down()): break
    
        logging.debug( "*** exception cleared by user\n" )
        g_Current_Exception_Not_Finished = False
             
     
def callback_switch_save_to_laptop( channel ): 
    global g_No_Callback_Function_Running
    global g_laptop_data_path
    global g_pi_data_path
   
    # don't reenter an already running callback and don't respond to a high to low switch transition
    if(( g_No_Callback_Function_Running ) and ( GPIO.input( SWITCH_save_to_laptop ) == SWITCH_UP )): 
        g_No_Callback_Function_Running = False
            
        try:
            turn_ON_LED( LED_save_to_laptop )

            switch_state = SWITCH_UP
            while ( switch_state == SWITCH_UP ):
                switch_state = GPIO.input( SWITCH_save_to_laptop )
    
            # do the copying ....
            logging.debug( 'attempting to save Data folder to laptop' )            
            command = 'scp -i ~/.ssh/id_rsa -r ' + g_pi_data_path + ' ' + g_laptop_data_path
            logging.debug( command )
            call ( command, shell=True )
                        
            g_Recorded_Data_Not_Saved = False
                                                                    
        except Exception as the_bad_news:                
            handle_exception( the_bad_news )
            logging.debug( 'NG: data NOT saved to laptop' )
            
        finally:
            g_No_Callback_Function_Running = True
            turn_OFF_LED( LED_save_to_laptop )
            logging.debug( 'OK: folder saved, exiting save to laptop' )

    else: 
        logging.debug( 'callback skipped: falling edge of save_to_laptop' )
    
# ------------------------------------------------- 
def callback_switch_read_from_laptop( channel ):
    global g_No_Callback_Function_Running
    global g_laptop_training_steerstats_file
    global g_laptop_training_weights_file
    global g_pi_training_steerstats_file
    global g_pi_training_weights_file
    
    # don't reenter an already running callback and don't respond to a high to low switch transition
    if(( g_No_Callback_Function_Running ) and ( GPIO.input( SWITCH_read_from_laptop ) == SWITCH_UP )): 
        g_No_Callback_Function_Running = False
                        
        try:
            turn_ON_LED( LED_read_from_laptop )
            switch_state = SWITCH_UP
            while ( switch_state == SWITCH_UP ):
                switch_state = GPIO.input( SWITCH_read_from_laptop )
    
            # do the reading ....
            logging.debug( 'attempting to read from laptop' )

            command = 'scp -i ~/.ssh/id_rsa -r ' + g_laptop_training_weights_file + ' ' + g_pi_training_weights_file
            call ( command, shell=True )
            command = 'scp -i ~/.ssh/id_rsa -r ' + g_laptop_training_steerstats_file + ' ' + g_pi_training_steerstats_file
            call ( command, shell=True )
                            
        except Exception as the_bad_news:                
            handle_exception( the_bad_news )
            logging.debug( 'NG: data NOT read from laptop' )
            
        finally:
            g_No_Callback_Function_Running = True
            turn_OFF_LED( LED_read_from_laptop )
            logging.debug( 'OK: data read, exiting read from laptop' )
    else: 
        logging.debug( 'callback skipped: falling edge of read_from_laptop' )
     
# ------------------------------------------------- 
#    regular exception handling not used with shutdown function
def callback_switch_shutdown_RPi( channel ):
    global g_Recorded_Data_Not_Saved
    global g_No_Callback_Function_Running

    # don't reenter an already running callback and don't respond to a high to low switch transition
    if(( g_No_Callback_Function_Running ) and ( GPIO.input( SWITCH_shutdown_RPi ) == SWITCH_UP )): 
        g_No_Callback_Function_Running = False
        logging.debug( 'starting shutdown' )        
        
        while( GPIO.input( SWITCH_shutdown_RPi ) == SWITCH_UP ):    # wait for user to release switch
            pass
            
        time.sleep( .1 )    # debounce switch                
            
        if( g_Recorded_Data_Not_Saved ):
            blinkSpeed = .2
            pushed_up_count = 15
            LEDs_state = LED_ON
            shutdown_is_wanted = False
        else:
            shutdown_is_wanted = True
        
        #----------------------------------------------
        #    Recorded data is not saved, check to see if user really wants to shutdown without saving
        if( shutdown_is_wanted == False ):
            user_has_not_reacted = True                                                
            
            while( True ):        # loop until break
                if( LEDs_state == LED_ON ):    # blink all lights to signify data is unsaved
                    turn_ON_all_LEDs()
                    LEDs_state = LED_OFF        
                else:
                    turn_OFF_all_LEDs()
                    LEDs_state = LED_ON
                    
                time.sleep( blinkSpeed )                    

                if( user_has_not_reacted ):
                    if( GPIO.input( SWITCH_shutdown_RPi ) == SWITCH_UP ):    # pushed up yet?
                        user_has_not_reacted = False            # user has finally pushed switch up        
            
                # switch has been pushed up again
                else:    
                    if( GPIO.input( SWITCH_shutdown_RPi ) == SWITCH_UP ):    # still pushed up?
                        pushed_up_count = pushed_up_count - 1
                    
                        if( pushed_up_count <= 0 ):                                
                            shutdown_is_wanted = True
                            break            # switch was pushed up long enough                 
                    else:                            
                        shutdown_is_wanted = False
                        break                # switch was pushed up but not for long enough                                                                            
        #----------------------------------------------
                            
        if( shutdown_is_wanted ):
            # shut down pi, data saved or not
            turn_OFF_all_LEDs()        # show the user the error has been cleared
            GPIO.output( OUTPUT_to_relay, RELAY_OFF )
            logging.debug( 'calling pi shutdown' )
            os.system( 'shutdown now -h' )
        
        #    user changed his mind, exit function without shut down
        turn_OFF_all_LEDs()        # show the user the shutdown has been stopped
        turn_ON_LED( LED_boot_RPi )    # turn this one back on to show power is still on
        logging.debug( 'user changed mind about shutdown' )
        g_No_Callback_Function_Running = True
        
    else: 
        logging.debug( 'skipped: another callback from shutdown_RPi' )
                     
# -------- Put binary (6 bit) number on LEDs ---------
def displayBinaryOnLEDs( theNumber ):
    GPIO.output( LED_read_from_laptop, theNumber & 0b000001 )
    GPIO.output( LED_save_to_laptop, ( theNumber & 0b000010 ) >> 1 )
    GPIO.output( LED_collect_data, ( theNumber & 0b000100 ) >> 2 )
    GPIO.output( LED_autonomous, ( theNumber & 0b001000 ) >> 3 )
    GPIO.output( LED_shutdown_RPi, ( theNumber & 0b010000 ) >> 4 )
    GPIO.output( LED_boot_RPi, ( theNumber & 0b100000 ) >> 5 )

# ------------------------------------------------- 
def turn_OFF_all_LEDs():
    turn_OFF_LED( LED_save_to_laptop )
    turn_OFF_LED( LED_read_from_laptop )
    turn_OFF_LED( LED_collect_data )
    turn_OFF_LED( LED_shutdown_RPi )
    turn_OFF_LED( LED_autonomous )
    turn_OFF_LED( LED_boot_RPi )

# ------------------------------------------------- 
def turn_OFF_all_LEDs_except_BOOT():
    turn_OFF_LED( LED_save_to_laptop )
    turn_OFF_LED( LED_read_from_laptop )
    turn_OFF_LED( LED_collect_data )
    turn_OFF_LED( LED_shutdown_RPi )
    turn_OFF_LED( LED_autonomous )
         
# ------------------------------------------------- 
def turn_ON_all_LEDs():
    turn_ON_LED( LED_save_to_laptop )
    turn_ON_LED( LED_read_from_laptop )
    turn_ON_LED( LED_collect_data )
    turn_ON_LED( LED_shutdown_RPi )
    turn_ON_LED( LED_autonomous )
    turn_ON_LED( LED_boot_RPi )
         
# ------------------------------------------------- 
def initialize_RPi_Stuff():
#    note: global variables start with a little "g"
    global g_camera
    global g_Camera_Is_Recording
    global g_Is_Autonomous
    global g_Wants_To_See_Video
    global g_Recorded_Data_Not_Saved
    global g_No_Callback_Function_Running
    global g_Current_Exception_Not_Finished
    global g_collector
    global g_getter
    global g_graph
    global g_image_data
    global g_stop_event
    global g_lock
    global g_ip_thread
    global g_steerstats
    global g_pi_data_path
    global g_laptop_data_path
    global g_laptop_training_steerstats_file
    global g_laptop_training_weights_file
    global g_pi_training_steerstats_file
    global g_pi_training_weights_file
    
    g_ip_thread = 0
    g_Wants_To_See_Video = True
    g_Camera_Is_Recording = False
    g_Is_Autonomous = False
    g_Recorded_Data_Not_Saved = False
    g_No_Callback_Function_Running = True
    g_Current_Exception_Not_Finished = False
#    g_collector=DataCollector()
    g_getter=DataGetter()
    g_camera = picamera.PiCamera()
    g_camera.resolution=(128, 96) #final image size

    # g_camera.zoom=(.125, 0, .875, 1) #crop so aspect ratio is 1:1
    g_camera.framerate=10 #<---- framerate (fps) determines speed of data recording
    
#--------- saving collected data paths ----------    
    g_pi_data_path = '/home/pi/autonomous/data/'
    g_laptop_data_path = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/'

#--------- loading training data paths ----------    
    g_laptop_training_steerstats_file = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/nnfixed/steerstats.npz'
    g_laptop_training_weights_file = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/nnfixed/weights.h5'
    g_pi_training_steerstats_file = '/home/pi/autonomous/services/steerstats.npz'
    g_pi_training_weights_file = '/home/pi/autonomous/services/weights.h5'

    model.load_weights('/home/pi/autonomous/services/weightsBell2.h5')
    g_steerstats=np.load('/home/pi/autonomous/services/steerstats.npz')['arr_0']

    model._make_predict_function()
    g_graph=tf.get_default_graph()

    g_image_data=np.zeros((78, 128, 3), dtype=np.uint8)
    g_stop_event=threading.Event()
    g_lock=threading.Lock()
    
    # dazzle them with Night Rider LED show...
    for x in range(0, 3):
        for i in range(0, 6):
            displayBinaryOnLEDs( 2 ** i )
            time.sleep( .125 )
            
        for i in range(5, -1, -1):
            displayBinaryOnLEDs( 2 ** i )
            time.sleep( .125 )    # dazzle them with Night Rider LED show...
    
    # blink LEDs as an alarm if autonmous or collect switches have been left up
    LED_state = LED_ON

    while( GPIO.input( SWITCH_collect_data ) == SWITCH_UP ):
        GPIO.output( LED_collect_data, LED_state )
        time.sleep( .25 )
        LED_state = LED_state ^ 1        # XOR bit to turn LEDs off or on
        
    while( GPIO.input( SWITCH_autonomous ) == SWITCH_UP ): 
        GPIO.output( LED_autonomous, LED_state )
        time.sleep( .25 )
        LED_state = LED_state ^ 1        # XOR bit to turn LEDs off or on
    
    # turn off all LEDs for initialization
    turn_OFF_all_LEDs()
# ---------------- MAIN PROGRAM ------------------------------------- 

GPIO.setmode( GPIO.BCM )  
GPIO.setwarnings( False )

#  falling edge detection setup for all switchs 
GPIO.setup( SWITCH_save_to_laptop, GPIO.IN, pull_up_down = GPIO.PUD_UP ) 
GPIO.setup( SWITCH_autonomous, GPIO.IN, pull_up_down = GPIO.PUD_UP ) 
GPIO.setup( SWITCH_read_from_laptop, GPIO.IN, pull_up_down = GPIO.PUD_UP ) 
GPIO.setup( SWITCH_shutdown_RPi, GPIO.IN, pull_up_down = GPIO.PUD_UP ) 
GPIO.setup( SWITCH_collect_data, GPIO.IN, pull_up_down = GPIO.PUD_UP ) 

GPIO.setup( LED_read_from_laptop, GPIO.OUT )
GPIO.setup( LED_save_to_laptop, GPIO.OUT )
GPIO.setup( LED_collect_data, GPIO.OUT )
GPIO.setup( LED_shutdown_RPi, GPIO.OUT )
GPIO.setup( LED_autonomous, GPIO.OUT )
GPIO.setup( LED_boot_RPi, GPIO.OUT )

GPIO.setup( OUTPUT_to_relay, GPIO.OUT )

# setup callback routines for switch falling edge detection  
#    NOTE: because of a RPi bug, sometimes a rising edge will also trigger these routines!
GPIO.add_event_detect( SWITCH_save_to_laptop, GPIO.FALLING, callback=callback_switch_save_to_laptop, bouncetime=50 )  
GPIO.add_event_detect( SWITCH_autonomous, GPIO.BOTH, callback=callback_switch_autonomous, bouncetime=100 )  
GPIO.add_event_detect( SWITCH_read_from_laptop, GPIO.FALLING, callback=callback_switch_read_from_laptop, bouncetime=50 )  
GPIO.add_event_detect( SWITCH_shutdown_RPi, GPIO.FALLING, callback=callback_switch_shutdown_RPi, bouncetime=50 )  
GPIO.add_event_detect( SWITCH_collect_data, GPIO.BOTH, callback=callback_switch_collect_data, bouncetime=200 ) 

initialize_RPi_Stuff()
    
GPIO.output( OUTPUT_to_relay, RELAY_ON )

LED_state = LED_ON
LED_count = 0

while ( True ):    
    if(( LED_count % 100 ) == 0 ):       # every 100 times through flip the led state to show we're alive
        GPIO.output( LED_boot_RPi, LED_state )
        LED_state = LED_state ^ 1
    LED_count = LED_count + 1 
    
    
