import RPi.GPIO as GPIO
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Reshape
from keras.optimizers import Adam, SGD
#from dropout_model import model
from history_model import model
model.add(Dense(6+1, activation='linear', kernel_initializer='lecun_uniform'))
model.compile(loss=['mse'], optimizer=SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True), metrics=['mse'])
print(model.summary())


LED_names={
  "save_to_USBdrive" : 2,
  "collect_data" : 3,
  "read_from_USBdrive" : 4,
  "autonomous" : 17,
  "shutdown_RPi" : 22,
  "boot_RPi" : 27,
}


switch_names={ 
  "save_to_USBdrive": 5, 
  "collect_data" : 6,
  "read_from_USBdrive" : 13,
  "autonomous" : 19,
  "shutdown_RPi" : 21,
  "boot_RPi" : 26,
}

FRAME_RATE = 40 #optimism
DATA_DIR = "/home/pi/foocars/cars/otto/data/"
COLLECT_DIR = DATA_DIR + "collected"
WEIGHTS_DIR = DATA_DIR + "models/w1/"
WEIGHTS_FILE = WEIGHTS_DIR + "weights.h5"
STEERSTATS_FILE = WEIGHTS_DIR + "steerstats.npz"
THR_MAX =1445
THR_HIGH=1310
THR_MID=1375
THR_LOW=1435


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


