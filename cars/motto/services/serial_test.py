import time
from serial_monitor import SerialMonitor

ser=SerialMonitor()

print("starting serial")

ser.start_serial()

for i in range(1, 100):
  time.sleep(.2)
  print(ser.read())

ser.stop_serial()
