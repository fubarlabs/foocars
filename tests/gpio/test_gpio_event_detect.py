import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)


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

 # Switch Testing

def callback_switch_thr_step(channel):
  print("thr_step")
def callback_switch_autonomous(channel):
  print("autonomous")
def callback_switch_collect_data(channel):
  print("collect")


for switch in switch_names.values():
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(switch_names["thr_step"], GPIO.FALLING, callback=callback_switch_thr_step, bouncetime=50)
GPIO.add_event_detect(switch_names["autonomous"], GPIO.BOTH, callback=callback_switch_autonomous, bouncetime=200)
GPIO.add_event_detect(switch_names["collect_data"], GPIO.BOTH, callback=callback_switch_collect_data, bouncetime=50)

while True:
  try:
      message = input("Press enter to quit\n\n") # Run until someone presses enter
      break
  finally:
      print("EXIT")
      GPIO.cleanup() # Clean up



