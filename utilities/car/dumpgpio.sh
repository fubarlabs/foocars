 #!/bin/sh

echo "LED_read_from_laptop = 2"
cat /sys/class/gpio/gpio2/value 
echo "LED_save_to_laptop = 3"
cat /sys/class/gpio/gpio3/value 
echo "LED_collect_data = 4"
cat /sys/class/gpio/gpio4/value 
echo "LED_autonomous = 17"
cat /sys/class/gpio/gpio17/value 
echo "LED_shutdown_RPi = 27"
cat /sys/class/gpio/gpio27/value 
echo "LED_boot_RPi = 22"
cat /sys/class/gpio/gpio22/value 
echo "SWITCH_collect_data = 11"
cat /sys/class/gpio/gpio11/value 
echo "SWITCH_save_to_laptop = 9"
cat /sys/class/gpio/gpio9/value 
echo "SWITCH_read_from_laptop = 10"
cat /sys/class/gpio/gpio10/value 
echo "SWITCH_autonomous = 5"
cat /sys/class/gpio/gpio5/value 
echo "SWITCH_shutdown_RPi = 6"
cat /sys/class/gpio/gpio6/value 
echo "------------------"
echo "ls /sys/class/gpio"
ls /sys/class/gpio/


