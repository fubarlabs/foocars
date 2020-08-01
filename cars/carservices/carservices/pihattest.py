import RPi.GPIO as GPIO
from defines import *
from time import sleep



def callback_switch_diagnostic(channel):
    print(f"diagnostic: {GPIO.input(switch_names['diagnostic'])}")
    for i in range(5):
        GPIO.output(LED_names["boot_RPi"], LED_ON)
        sleep(.2)
        GPIO.output(LED_names["boot_RPi"], LED_OFF)
        sleep(.2)
    GPIO.output(LED_names["boot_RPi"], LED_ON)


def callback_switch_autonomous(channel):
    print(f"autonomous: {GPIO.input(switch_names['autonomous'])}")
    if GPIO.input(switch_names["autonomous"])!=SWITCH_ON:
        return 
    GPIO.output(LED_names["autonomous"], LED_OFF)
    sleep(1)
    GPIO.output(LED_names["autonomous"], LED_ON)

                               

def callback_switch_collect_data(channel):
    print(f"collect_data: {GPIO.input(switch_names['collect_data'])}")
    if GPIO.input(switch_names["collect_data"])!=SWITCH_ON:
        return 
    GPIO.output(LED_names["collect_data"], LED_OFF)
    sleep(1)
    GPIO.output(LED_names["collect_data"], LED_ON)


def main():
    print("PI Hat Tests")

    print("LEDS")

    print(LED_names)

    print("switches and buttons")

    print(switch_names)


    GPIO.setmode(GPIO.BCM)

    for led in LED_names.values():
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, LED_OFF)


    print("Turn on Power Status LED")
    for i in range(5):
        GPIO.output(LED_names["boot_RPi"], LED_ON)
        sleep(.5)
        GPIO.output(LED_names["boot_RPi"], LED_OFF)
        sleep(.5)

    GPIO.output(LED_names["boot_RPi"], LED_ON)

    print("Collect LED")
    for i in range(5):
        GPIO.output(LED_names["collect_data"], LED_ON)
        sleep(.5)
        GPIO.output(LED_names["collect_data"], LED_OFF)
        sleep(.5)

    print("Auto Mode")
    for i in range(5):
        GPIO.output(LED_names["autonomous"], LED_ON)
        sleep(.5)
        GPIO.output(LED_names["autonomous"], LED_OFF)
        sleep(.5)

    # Switch Testing

    for switch in switch_names.values():
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    GPIO.add_event_detect(switch_names["diagnostic"], GPIO.FALLING, callback=callback_switch_diagnostic, bouncetime=50)
    GPIO.add_event_detect(switch_names["autonomous"], GPIO.BOTH, callback=callback_switch_autonomous, bouncetime=200)
    GPIO.add_event_detect(switch_names["collect_data"], GPIO.BOTH, callback=callback_switch_collect_data, bouncetime=50)


    while True:
        try:
            message = input("Press enter to quit\n\n") # Run until someone presses enter
            break
        finally:
            print("EXIT")
            GPIO.cleanup() # Clean up


if __name__ == "__main__":
    main()
