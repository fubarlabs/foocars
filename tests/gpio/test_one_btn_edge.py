# Test the button edge detection

import RPi.GPIO as GPIO
from time import sleep


def button_handler(pin):
    print(f"pin:{pin}, value: {GPIO.input(pin)}")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    btn_pin = 9
    GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(
        btn_pin, GPIO.BOTH,
        callback=button_handler,
        bouncetime=200
    )
    try:
        sleep(1000)
    except KeyboardInterrupt:
        GPIO.cleanup()
        
