import RPi.GPIO as GPIO
import socket
LED_names={ 
  "boot_RPi" : 2,
  "shutdown_RPi" : 3,
  "autonomous" : 4,
  "collect_data" : 27,
  "save_to_USBdrive" : 22,
  "read_from_USBdrive" : 17,
}


switch_names={ 
  "shutdown_RPi" : 9,
  "autonomous" : 11,
  "collect_data" : 6,
  "save_to_USBdrive" : 13,
  "read_from_USBdrive" : 5,
}

FRAME_RATE = 40
DATA_DIR = "/home/pi/foocars/cars/"+ socket.gethostname()+ "/data/"
COLLECT_DIR = DATA_DIR + "collected"
WEIGHTS_DIR = DATA_DIR + "weights/"
WEIGHTS_FILE = WEIGHTS_DIR + "weights.h5"
STEERSTATS_FILE = WEIGHTS_DIR + "steerstats.npz"
THR_MAX = 1580

SWITCH_ON=GPIO.LOW
SWITCH_OFF=GPIO.HIGH

LED_ON=GPIO.HIGH
LED_OFF=GPIO.LOW

#function returns dynamically created object of type 'Enum' with fields enums:
def enum(**enums):
  return type('Enum', (), enums) 

commandEnum=enum(
  NOT_ACTUAL_COMMAND=0,
  RC_SIGNAL_WAS_LOST=1, 
  RC_SIGNALED_STOP_AUTONOMOUS=2, 
  STEERING_VALUE_OUT_OF_RANGE=3, 
  THROTTLE_VALUE_OUT_OF_RANGE=4, 
  RUN_AUTONOMOUSLY=5, 
  STOP_AUTONOMOUS=6, 
  STOPPED_AUTO_COMMAND_RECIEVED=7, 
  NO_COMMAND_AVAILABLE=8, 
  GOOD_PI_COMMAND_RECEIVED=9, 
  TOO_MANY_VALUES_IN_COMMAND=10, 
  GOOD_RC_SIGNALS_RECIEVED=11)


