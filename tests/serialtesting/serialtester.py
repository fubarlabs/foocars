import time
import RPi.GPIO as GPIO
import serial
import threading
from defines import *
from serial_monitor import SerialMonitor

serial_shutdown_req=False
toggle_shutdown_req=False

def shutdown_req():
  print("shutting down autonomous")
  global g_serial
  dataline='{0}, {1}, {2}, {3}\n'.format(commandEnum.STOP_AUTONOMOUS, 1500, 1500, 0)
  print("trying to shutdown autonomous")
  print(dataline)
  g_serial.write(dataline.encode('ascii')) 
  g_serial.flush()

  n_read_items=0
  while n_read_items!=10:
    try:
      datainput=g_serial.readline()
      print(datainput)
      data=list(map(float,str(datainput,'ascii').split(',')))
      n_read_items=len(data)
    except ValueError:
      continue
  print(data)
  '''
  while n_read_items!=10:
    datainput=g_serial.readline()
    data=list(map(float,str(datainput,'ascii').split(',')))
    n_read_items=len(data)
  print(data)
  '''
  while data[0]!=commandEnum.STOPPED_AUTO_COMMAND_RECIEVED: #continue sending stop commands until we get an ack
    print("sending stop signal")
    g_serial.write(dataline.encode('ascii'))
    g_serial.flush()
    #time.sleep(.01)
    g_serial.flushInput()

    n_read_items=0
    while n_read_items!=10:
      try:
        datainput=g_serial.readline()
        print(datainput)
        data=list(map(float,str(datainput,'ascii').split(',')))
        n_read_items=len(data)
      except ValueError:
        continue
    '''
    datainput=g_serial.readline()
    data=list(map(float,str(datainput,'ascii').split(',')))
    n_read_items=len(data)
    while n_read_items!=10:
      datainput=g_serial.readline()
      data=list(map(float,str(datainput,'ascii').split(',')))
      n_read_items=len(data)
    '''
    print(data)

def callback_switch_shutdown_RPi(channel):
  if GPIO.input(switch_names["shutdown_RPi"])!=SWITCH_ON:
    return
  GPIO.output(LED_names["shutdown_RPi"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["shutdown_RPi"], LED_OFF)

def callback_switch_autonomous(channel):
  time.sleep(.1)
  if GPIO.input(switch_names['autonomous'])==SWITCH_ON:
    if callback_switch_autonomous.is_auto==True:
      print("read another autonomous toggle on while in autonomous mode")
    else:
      print("user toggled autonomous on")
      callback_switch_autonomous.is_auto=True
      GPIO.output(LED_names['autonomous'], GPIO.HIGH)
  else:
    if callback_switch_autonomous.is_auto==True:
      print("user toggled autonomous off")
      if serial_shutdown_req==False:
        print("toggling shutdown req")
      callback_switch_autonomous.is_auto=False
      GPIO.output(LED_names['autonomous'], GPIO.LOW)
    else:
      print("read another autonomous toggle off while not in autonomous mode")
callback_switch_autonomous.is_auto=False

def callback_switch_collect_data(channel):
  time.sleep(.1)
  if GPIO.input(switch_names['collect_data'])==SWITCH_ON:
    if callback_switch_collect_data.is_collecting==True:
      print("read another collect data toggle on while in collect mode")
    else:
      print("user toggled collect data on")
      callback_switch_collect_data.is_collecting=True
      GPIO.output(LED_names['collect_data'], GPIO.HIGH)
  else:
    if callback_switch_collect_data.is_collecting==True:
      print("user toggled collect data off")
      callback_switch_collect_data.is_collecting=False
      GPIO.output(LED_names['collect_data'], GPIO.LOW)
    else:
      print("read another collect data toggle off while in not in collect mode")
callback_switch_collect_data.is_collecting=False


def callback_switch_save_to_USBdrive(channel):
  if GPIO.input(switch_names["save_to_USBdrive"])!=SWITCH_ON:
    return
  GPIO.output(LED_names["save_to_USBdrive"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["save_to_USBdrive"], LED_OFF)

def callback_switch_read_from_USBdrive(channel):
  if GPIO.input(switch_names["read_from_USBdrive"])!=SWITCH_ON:
    return
  GPIO.output(LED_names["read_from_USBdrive"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["read_from_USBdrive"], LED_OFF)

def displayBinLEDCode(code): 
  GPIO.output(LED_names["boot_RPi"], (code>>5)&1)
  GPIO.output(LED_names["shutdown_RPi"], (code>>4)&1)
  GPIO.output(LED_names["autonomous"], (code>>3)&1)
  GPIO.output(LED_names["collect_data"], (code>>2)&1)
  GPIO.output(LED_names["save_to_USBdrive"], (code>>1)&1)
  GPIO.output(LED_names["read_from_USBdrive"], code&1)

global g_serial
try:
  g_serial=serial.Serial('/dev/ttyACM1')
except serial.SerialException:
  try:
    g_serial=serial.Serial('/dev/ttyACM0')
  except serial.SerialException:
    print("Error, could not connect to a serial port")

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
GPIO.add_event_detect(switch_names["autonomous"], GPIO.BOTH, callback=callback_switch_autonomous, bouncetime=200);
GPIO.add_event_detect(switch_names["collect_data"], GPIO.BOTH, callback=callback_switch_collect_data, bouncetime=50);
GPIO.add_event_detect(switch_names["save_to_USBdrive"], GPIO.FALLING, callback=callback_switch_save_to_USBdrive, bouncetime=50);
GPIO.add_event_detect(switch_names["read_from_USBdrive"], GPIO.FALLING, callback=callback_switch_read_from_USBdrive, bouncetime=50);

auto_dataline='{0}, {1}, {2}, {3}\n'.format(commandEnum.RUN_AUTONOMOUSLY, 1500, 1500, 0)
was_in_auto=False

while(True):
  g_serial.flushInput()
  datainput=g_serial.readline()
  data=list(map(float,str(datainput,'ascii').split(',')))
  n_read_items=len(data)
  while n_read_items!=10:
    datainput=g_serial.readline()
    data=list(map(float,str(datainput,'ascii').split(',')))
    n_read_items=len(data)
  if callback_switch_collect_data.is_collecting==True:
    print("Data collection:")
    print(data)
 
  elif callback_switch_autonomous.is_auto==True:
    #while we are in autonomous mode, we have to poll fubarino for stop signal
    was_in_auto=True
    print("autonomous mode")
    print(data)
    if data[0]==commandEnum.RC_SIGNALED_STOP_AUTONOMOUS: #if we get a stop signal
      print("got RC shutdown")
      serial_shutdown_req=True
      for i in range(0, 5): #send ack 5 times
        time.sleep(.01)
        dataline='{0}, {1}, {2}, {3}\n'.format(commandEnum.STOPPED_AUTO_COMMAND_RECIEVED, 1500, 1500, 0)
        g_serial.write(dataline.encode('ascii')) 
      while callback_switch_autonomous.is_auto==True: 
        time.sleep(.5)
        GPIO.output(LED_names["autonomous"], GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(LED_names["autonomous"], GPIO.LOW)
      was_in_auto=False
    else:    
      print(auto_dataline.encode('ascii'))
      g_serial.write(auto_dataline.encode('ascii'))
      g_serial.flush()

  if was_in_auto==True and callback_switch_autonomous.is_auto==False:
    print("shutting down autonomous on fubarino")
    shutdown_req()
    was_in_auto=False
"""
  print(toggle_shutdown_req)
  if toggle_shutdown_req==True:
    dataline='{0}, {1}, {2}, {3}\n'.format(commandEnum.STOP_AUTONOMOUS, 1500, 1500, 0)
    print("trying to shutdown autonomous")
    print(dataline)
    g_serial.write(dataline.encode('ascii')) 
    g_serial.flush()

    datainput=g_serial.readline()
    data=list(map(float,str(datainput,'ascii').split(',')))
    n_read_items=len(data)
    while n_read_items!=10:
      datainput=g_serial.readline()
      data=list(map(float,str(datainput,'ascii').split(',')))
      n_read_items=len(data)
    print(data)
    while data[0]!=commandEnum.STOPPED_AUTO_COMMAND_RECIEVED: #continue sending stop commands until we get an ack
      print("sending stop signal")
      g_serial.write(dataline.encode('ascii'))
      g_serial.flush()
      #time.sleep(.01)
      g_serial.flushInput()
      datainput=g_serial.readline()
      data=list(map(float,str(datainput,'ascii').split(',')))
      n_read_items=len(data)
      while n_read_items!=10:
        datainput=g_serial.readline()
        data=list(map(float,str(datainput,'ascii').split(',')))
        n_read_items=len(data)

      print(data)
    toggle_shutdown_req=False
"""
 
GPIO.cleanup()
g_serial.close()

