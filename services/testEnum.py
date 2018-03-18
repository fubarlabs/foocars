#!/usr/bin/python3

import sys, os

from enum import Enum     


# -------- Command enumeration same as ones on fubarino --------- 
# -------- This works --------- 

    
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
      
print( 'not actual command = ' + str( int( commandEnum.NOT_ACTUAL_COMMAND )))
print( 'throttle out of range = ' + str( int( commandEnum.THROTTLE_VALUE_OUT_OF_RANGE )))
print( 'no command available = ' + str( int( commandEnum.NO_COMMAND_AVAILABLE )))
print( 'good rc signals received = ' + str( int( commandEnum.GOOD_RC_SIGNALS_RECEIVED )))
