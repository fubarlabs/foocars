import RPi.GPIO as GPIO
import socket
LED_names={ 
  "boot_RPi" : 4,
  "shutdown_RPi" : 3,
  "autonomous" : 27,
  "collect_data" : 2 
}


switch_names={ 
  "thr_step" : 9,
  "autonomous" : 6,
  "collect_data" : 11,
}
 
# Modes: manual, auto, remote
MODE = "manual"

# Camera settings
FRAME_RATE = 40
CAMERA_RESOLUTION = (128, 96)
AUTO_IMAGE_FRAME = (36, 128, 3)
CAMERA_IMAGE_FRAME = [96, 128, 3]

# Data settings
DATA_DIR = "/foocars/cars/chiaracer/data/"
COLLECT_DIR = DATA_DIR + "collected"
WEIGHTS_DIR = DATA_DIR + "weights/"
WEIGHTS_FILE = WEIGHTS_DIR + "weights.h5"

STEERSTATS_FILE = WEIGHTS_DIR + "steerstats.npz"
THROTTLE_WEIGHTS_FILE = WEIGHTS_DIR + "weights_throttle.h5"
THROTTLESTATS_FILE = WEIGHTS_DIR + "throttlestats.npz"


THR_MAX = 1580
THR_STEPS = [1500, 1540, 1560, 1580, 1600, 1620]
THR_CURRENT = THR_STEPS[0]
THR_POS = 0

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


