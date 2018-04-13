import RPi.GPIO as GPIO
import time


LED_names={ "save_to" : 22,
  "collect_data" : 27,
  "read_from" : 17,
  "autonomous" : 4,
  "shutdown_RPi" : 3,
  "boot_RPi" : 2,
}


switch_names={ "collect_data" : 6,
  "read_from" : 5,
  "autonomous" : 11,
  "shutdown_RPi" : 9,
  "boot_RPi" : 10,
  "save_to": 13 
}

time_format='%Y-%m-%d_%H-%M-%S'

def displayBinLEDCode(code): 
  GPIO.output(LED_names["boot_RPi"], (code>>5)&1)
  GPIO.output(LED_names["shutdown_RPi"], (code>>4)&1)
  GPIO.output(LED_names["autonomous"], (code>>3)&1)
  GPIO.output(LED_names["read_from"], (code>>2)&1)
  GPIO.output(LED_names["collect_data"], (code>>1)&1)
  GPIO.output(LED_names["save_to"], code&1)


def callback_switch_shutdown_RPi(channel):
  if GPIO.input(switch_names["shutdown_RPi"])!=SWITCH_ON:
    return 
  print("shutdown RPi Button")
  GPIO.output(LED_names["shutdown_RPi"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["shutdown_RPi"], LED_OFF)

def callback_switch_boot_RPi(channel):
  if GPIO.input(switch_names["boot_RPi"])!=SWITCH_ON:
    return 
  print("boot RPi Button")
  GPIO.output(LED_names["boot_RPi"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["boot_RPi"], LED_OFF)


def callback_switch_save_to(channel):
  if GPIO.input(switch_names["save_to"])!=SWITCH_ON:
    return
  print("Save to USB Drive Button")
  GPIO.output(LED_names["save_to"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["save_to"], LED_OFF)

def callback_switch_read_from(channel):
  if GPIO.input(switch_names["read_from"])!=SWITCH_ON:
    return
  print("Read from USB Drive Button")
  GPIO.output(LED_names["read_from"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["read_from"], LED_OFF)

def callback_switch_collect_data(channel):
  time.sleep(.1)
  if (GPIO.input(switch_names["collect_data"]))==SWITCH_ON:
    if callback_switch_collect_data.is_recording==True:
      print('read another high transition while already recording\n')
    else:
      print('toggled collect data on')
      callback_switch_collect_data.is_recording=True
      GPIO.output(LED_names["collect_data"], LED_ON)
  else:
    if callback_switch_collect_data.is_recording==True:
      print('toggled collect data off')
      callback_switch_collect_data.is_recording=False
      GPIO.output(LED_names["collect_data"], LED_OFF)
    else:
      print('read another low transition while not data collecting')
callback_switch_collect_data.is_recording=False

def callback_switch_autonomous(channel):
  time.sleep(.1)
  if (GPIO.input(switch_names["autonomous"]))==SWITCH_ON:
    if callback_switch_collect_data.is_recording==True:
      print('read another high transition while autonomizing\n')
    else:
      print('toggled autonomous on')
      callback_switch_autonomous.is_recording=True
      GPIO.output(LED_names["autonomous"], LED_ON)
  else:
    if callback_switch_autonomous.is_recording==True:
      print('toggled autonomous off')
      callback_switch_autonomous.is_recording=False
      GPIO.output(LED_names["autonomous"], LED_OFF)
    else:
      print('read another low transition while not autonomizing')
callback_switch_autonomous.is_recording=False

SWITCH_ON=GPIO.LOW
SWITCH_OFF=GPIO.HIGH

LED_ON=GPIO.HIGH
LED_OFF=GPIO.LOW

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for led in LED_names.values():
  GPIO.setup(led, GPIO.OUT)
  GPIO.output(led, LED_OFF)

for j in range(0, 3):
  for i in range(0, 6):
    displayBinLEDCode(2**i)
    time.sleep(.05)
  for i in range(0, 6):
    displayBinLEDCode(2**(5-i))
    time.sleep(.05)
displayBinLEDCode(0)

for switch in switch_names.values():
  GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(switch_names["shutdown_RPi"], GPIO.FALLING, callback=callback_switch_shutdown_RPi, bouncetime=50);
GPIO.add_event_detect(switch_names["boot_RPi"], GPIO.FALLING, callback=callback_switch_boot_RPi, bouncetime=50);
GPIO.add_event_detect(switch_names["autonomous"], GPIO.BOTH, callback=callback_switch_autonomous, bouncetime=200);
GPIO.add_event_detect(switch_names["collect_data"], GPIO.BOTH, callback=callback_switch_collect_data, bouncetime=50);
GPIO.add_event_detect(switch_names["save_to"], GPIO.FALLING, callback=callback_switch_save_to, bouncetime=50);
GPIO.add_event_detect(switch_names["read_from"], GPIO.FALLING, callback=callback_switch_read_from, bouncetime=50);


input("Press enter to stop")
GPIO.cleanup()
