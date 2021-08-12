# Test the button polling

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

btn_pin = 9
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(btn_pin):
            print("ON")
        else:
            print("OFF")

        sleep(.25)

except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()