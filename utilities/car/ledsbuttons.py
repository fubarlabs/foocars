import RPi.GPIO as GPIO
import time


#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

leds =  [2,3,4,17,27,22]
swts = [11,9,10,5,6]

def swt_callback:
    print("led gpio: %s, swt gpio: %s", led[0],swt[0])
    GPIO.output(led, GPIO.HIGH)


for led in leds:
    GPIO.setup(led, GPIO.OUT)
    print ("led gpio:%s", led)
    GPIO.output(led, GPIO.HIGH)

for swt in swts:
    GPIO.setup(swt, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    print ("swt gpio:%s", swt)



GPIO.add_event_detect(swt[0], GPIO.FALLING, callback=swt_callback, bouncetime=30)

for ii in range(5):
    for led in leds:
        print ("led gpio:%s", led)
        GPIO.output(led, GPIO.LOW)
        time.sleep(.25)
        GPIO.output(led, GPIO.HIGH)
        time.sleep(.25)


while True:
	time.sleep(1)

GPIO.cleanup()


