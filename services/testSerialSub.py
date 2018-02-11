#!/usr/bin/env python3
#	changed from #!/usr/bin/python3 and enum worked

import sys, os
import serial

from enum import Enum   
  
import logging
logging.basicConfig(filename='/tmp/ottoMicroLogger.log',level=logging.DEBUG)
logging.debug( '\n\n new session \n' )
logging.debug( 'setting up model ')

# -------- Command enumeration same as ones on fubarino --------- 
#	use like this: commandEnum.NO_COMMAND_AVAILABLE
class commandEnum(Enum):
	NOT_ACTUAL_COMMAND = 0
	RC_SIGNAL_WAS_LOST = 1
	RC_SIGNALED_STOP_AUTONOMOUS = 2
	STEERING_VALUE_OUT_OF_RANGE = 3
	THROTTLE_VALUE_OUT_OF_RANGE= 4
	RUN_AUTONOMOUSLY = 5
	STOP_AUTONOMOUS = 6
	STOPPED_AUTO_COMMAND_RECEIVED = 7
	NO_COMMAND_AVAILABLE = 8
	GOOD_PI_COMMAND_RECEIVED = 9
	TOO_MANY_VALUES_IN_COMMAND = 10
	GOOD_RC_SIGNALS_RECEIVED = 11

# -------- Handler for clearing all switch errors --------- 
def handle_exception( the_bad_news ):
	logging.debug( '\n' )		
	logging.debug( '*** Exception occurred' )		
	if( len(the_bad_news.args) == 1 ):		# one argument exceptions are unforeseen 
		error_number = 15
		message = the_bad_news.args[0]
		logging.debug( str(the_bad_news.args[0]))
		
		exc_type, exc_obj, exc_tb = sys.exc_info()
		logging.debug(' line number = ' + str(exc_tb.tb_lineno))
	else:					# two argument exceptions are previously setup to be handled
		error_number = the_bad_news.args[0]
		message = the_bad_news.args[1]			
		logging.debug( 'error number = ' + str(the_bad_news.args[0]) + ': ' + str(the_bad_news.args[1]))

# -------- Wait or Not for a good command list from Fubarino --------
def getSerialCommandIfAvailable( theCommandList, dontWaitForCommand, theCommand ):
	numberOfCharsWaiting = 0
	
	if( numberOfCharsWaiting == 0 ):
		if( dontWaitForCommand ):
			theCommand = commandEnum.NO_COMMAND_AVAILABLE
			return
	
	serial_input_is_no_damn_good = True
	while( serial_input_is_no_damn_good ):		
		try:
			number_of_serial_items = 0
			required_number_of_data_items = 9
					
			while( serial_input_is_no_damn_good ):
#				ser.flushInput()	# dump partial command
#				serial_line_received = ser.readline()
				serial_line_received = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
				
#				raw_serial_list = list( str(serial_line_received,'ascii').split(','))
				raw_serial_list = list( serial_line_received.split(','))
				theCommand = raw_serial_list[ 0 ]
			 
				number_of_serial_items = len( raw_serial_list )
				line_not_checked = True
			
				while( line_not_checked ):
					if( number_of_serial_items == required_number_of_data_items + 1 ):
				
						no_conversion_errors = True
						for i in range( 1, required_number_of_data_items + 1 ):
							try:
								theCommandList.append( float( raw_serial_list[ i ]))
							except ValueError:
								no_conversion_errors = False
								logging.debug( 'error converting to float = ' + str( raw_serial_list[ i ]))
						
							if( no_conversion_errors ):
								serial_input_is_no_damn_good = False							
							line_not_checked = False
										
					else:		# first test of received line fails 
						line_not_checked = False
						logging.debug( 'serial input error: # data items = ' + str( number_of_serial_items  ))
							
			self.debugSerialInput = serial_line_received
		
		except Exception as the_bad_news:				
			handle_exception( the_bad_news )
			logging.debug( 'Error: receiving command from fubarino' )
			


theCommand = 0
dontWaitForCommand = False
theCommandList = []
getSerialCommandIfAvailable( theCommandList, dontWaitForCommand, theCommand )
print ( theCommandList )	
	
	
	
	
	
	
	
	
	
	
	
	
	