import RPi.GPIO as GPIO
from time import sleep

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

for switch in switch_names.values():
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    try:
        GPIO.wait_for_edge(switch["thr_step"], GPIO.FALLING)
        print(f"thr_step: falling")
        GPIO.wait_for_edge(switch["autonomous"], GPIO.FALLING)
        print(f"autonomous: falling")
        GPIO.wait_for_edge(switch["collect_data"], GPIO.FALLING)
        print(f"colelct_data: falling")

    finally:
        print("EXIT")
        GPIO.cleanup() # Clean up

