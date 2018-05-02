import RPi.GPIO as GPIO

LED_names={ "boot_RPi" : 22,
  "shutdown_RPi" : 27,
  "autonomous" : 17,
  "collect_data" : 4,
  "save_to_USBdrive" : 3,
  "read_from_USBdrive" : 2,
}


switch_names={ "shutdown_RPi" : 6,
  "autonomous" : 5,
  "collect_data" : 11,
  "save_to_USBdrive" : 9,
  "read_from_USBdrive" : 10,
}

FRAME_RATE = 40
DATA_DIR = "/home/pi/foocars/cars/motto/data/"
COLLECT_DIR = DATA_DIR + "collected"
WEIGHTS_DIR = DATA_DIR + "weights/"
WEIGHTS_FILE = WEIGHTS_DIR + "weights.h5"
STEERSTATS_FILE = WEIGHTS_DIR + "steerstats.npz"
THR_MAX = 1590


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


