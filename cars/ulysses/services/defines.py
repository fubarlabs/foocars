import RPi.GPIO as GPIO

LED_names={ 
  "shutdown_RPi" : 4,
  "autonomous" : 27,
  "collect_data" : 2,
}


switch_names={ 
  "shutdown_RPi" : 9,
  "autonomous" : 11,
  "collect_data" : 6,
}

FRAME_RATE = 40
DATA_DIR = "/home/pi/foocars/cars/ulysses/data/"
COLLECT_DIR = DATA_DIR + "collected"
WEIGHTS_DIR = DATA_DIR + "weights/"
#WEIGHTS_FILE = WEIGHTS_DIR + "weights_2018-04-15_21-43-33_epoch_20.h5"
#WEIGHTS_FILE = WEIGHTS_DIR + "weights_2018-04-15_21-43-33_epoch_40.h5"
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


#code is an int in range 0-63, consisting of binary on-off values for the leds. boot_RPi is MSB
def displayBinLEDCode(code): 
  GPIO.output(LED_names["autonomous"], (code>>2)&1)
  GPIO.output(LED_names["shutdown_RPi"], (code>>1)&1)
  GPIO.output(LED_names["collect_data"], (code)&1)
  
