import time
import datetime
import logging
import RPi.GPIO as GPIO
import picamera
import serial
import numpy as np
import threading
import keras
import tensorflow as tf
from dropout_model import model


LED_names={ "boot_RPi" : 22,
  "shutdown_RPi" : 27,
  "autonomous" : 17,
  "collect_data" : 4,
  "save_to_USBdrive" : 3,
  "read_from_USBdrive" : 2,
}


switch_names={ "shutdown_RPi" : 6,
  "autonomous" : 5,
  "collect_data" : 11,
  "save_to_USBdrive" : 9,
  "read_from_USBdrive" : 10,
}

time_format='%Y-%m-%d_%H-%M-%S'

logging.basicConfig(filename='ottoLogger.log', level=logging.DEBUG)
logging.debug('\n\n New Test Session {0}\n'.format(datetime.datetime.now().strftime(time_format)))

SWITCH_ON=GPIO.LOW
SWITCH_OFF=GPIO.HIGH

LED_ON=GPIO.HIGH
LED_OFF=GPIO.LOW

class DataCollector(object):
  '''this object is passed to the camera.start_recording function, which will treat it as a 
      writable object, like a stream or a file'''
  def __init__(self, serial_obj, save_dir):
    assert serial_obj.isOpen()==True
    self.save_dir=save_dir
    self.ser=serial_obj
    self.num_frames=100
    self.imgs=np.zeros((self.num_frames, 96, 128, 3), dtype=np.uint8) #we put the images in here
    self.IMUdata=np.zeros((self.num_frames, 7), dtype=np.float32) #we put the imu data in here
    self.RCcommands=np.zeros((self.num_frames, 2), dtype=np.float16) #we put the RC data in here
    self.idx=0 # this is the variable to keep track of number of frames per datafile
    nowtime=datetime.datetime.now()
    self.currtime=time.time()
    self.img_file=self.save_dir+'/imgs_{0}'.format(nowtime.strftime(time_format))
    self.IMUdata_file=self.save_dir+'/IMU_{0}'.format(nowtime.strftime(time_format))
    self.RCcommands_file=self.save_dir+'/commands_{0}'.format(nowtime.strftime(time_format))
  
  def write(self, s):
    '''this is the function that is called every time the PiCamera has a new frame'''
    imdata=np.reshape(np.fromstring(s, dtype=np.uint8), (96, 128, 3), 'C')
    #now we read from the serial port and format and save the data:
    try:
      start=time.time()
      self.ser.flushInput()
      datainput=self.ser.readline()
      data=list(map(float,str(datainput,'ascii').split(','))) #formats line of data into array
      while len(data)!=9:
        datainput=self.ser.readline()
        data=list(map(float,str(datainput,'ascii').split(','))) #formats line of data into array
      end=time.time()
      #print(end-start)
      print(data)
      #print("got cereal\n")

    except ValueError as err:
      print(err)
      return 
    #Note: the data from the IMU requires some processing which does not happen here:
    self.imgs[self.idx]=imdata
    accelData=np.array([data[0], data[1], data[2]], dtype=np.float32)
    gyroData=np.array([data[3], data[4], data[5]], )
    datatime=np.array([int(data[6])], dtype=np.float32)
    steer_command=int(data[7])
    gas_command=int(data[8])
    self.IMUdata[self.idx]=np.concatenate((accelData, gyroData, datatime))
    self.RCcommands[self.idx]=np.array([steer_command, gas_command])
    self.idx+=1
    if self.idx == self.num_frames: #default value is 100, unless user specifies otherwise
      self.idx=0
      self.flush()  
    #print(time.time()-self.currtime)
    #self.currtime=time.time()
  
  def flush(self):
    '''this function is called every time the PiCamera stops recording'''
    start=time.time()
    np.savez(self.img_file, self.imgs)
    np.savez(self.IMUdata_file, self.IMUdata)
    np.savez(self.RCcommands_file, self.RCcommands)
    end=time.time()
    print("files saved\n")
    print(end-start)
    #this new image file name is for the next chunk of data, which starts recording now
    nowtime=datetime.datetime.now()
    self.img_file=self.save_dir+'/imgs_{0}'.format(nowtime.strftime(time_format))
    self.IMUdata_file=self.save_dir+'/IMU_{0}'.format(nowtime.strftime(time_format))
    self.RCcommands_file=self.save_dir+'/commands_{0}'.format(nowtime.strftime(time_format))
    self.imgs[:]=0
    self.IMUdata[:]=0
    self.RCcommands[:]=0
    self.idx=0


def imageprocessor(event, serial_obj):
  global g_imagedata
  global g_graph
  global g_lock
  global g_steerstats
  
  with g_graph.as_default():
    time.sleep(1)
    while not event.is_set():
      g_lock.acquire()
      tmpimg=np.copy(g_imageData)
      g_lock.release()
      immean=tmpimg.mean()
      imvar=tmpimg.std()
      start=time.time()

      pred=model.predict(np.expand_dims(tmpimg, axis=0))
      steer_command=pred[0][0]*g_steerstats[1]+g_steerstats[0]

      if steer_command>2000:
        steer_command=2000
      elif steer_command<1000:
        steer_command=1000

      end=time.time()
      if(end-start)<.2:
        time.sleep(.2-(end-start))
      dataline='{0}, {1}, {2}, {3}\n'.format(1, int(steer_command), 1567, 0)
      print(dataline)
      try:
        serial_obj.flushInput()
        serial_obj.write(dataline.encode('ascii'))
      except:
        print("some serial problem")


class DataGetter(object):
  def __init__(self):
    pass

  def write(self, s):
    global g_imageData
    global g_lock
    imagerawdata=np.reshape(np.fromstring(s, dtype=np.uint8), (96, 128, 3), 'C')
    imdata=imagerawdata[20:56, :]
    immean=imdata.mean()
    imvar=imdata.std()
    g_lock.acquire()
    g_imageData=np.copy((imdata-immean)/imvar)
    g_lock.release()

  def flush(self):
    pass


def callback_switch_shutdown_RPi(channel):
  if GPIO.input(switch_names["shutdown_RPi"])!=SWITCH_ON:
    return 
  GPIO.output(LED_names["shutdown_RPi"], LED_ON)
  time.sleep(1)
  GPIO.output(LED_names["shutdown_RPi"], LED_OFF)

def callback_switch_autonomous(channel):
  global g_getter
  global g_stop_event
  global g_ip_thread
  global g_camera
  global g_serial
  time.sleep(.1)
  if (GPIO.input(switch_names["autonomous"]))==SWITCH_ON:
    if callback_switch_autonomous.is_auto==True:
      logging.debug('read another high transition while in autonomous')
    else:
      logging.debug('\n user toggled autonomous on {0}\n'.format(datetime.datetime.now().strftime(time_format)))
      g_camera.start_recording(g_getter, format='rgb')
      g_ip_thread=threading.Thread(target=imageprocessor, args=[g_stop_event, g_serial])
      g_ip_thread.start()
      logging.debug('in autonomous mode')
      callback_switch_autonomous.is_auto=True
      GPIO.output(LED_names["autonomous"], GPIO.HIGH)
  else:		#switch off
    if callback_switch_autonomous.is_auto==True:
      logging.debug('\n user toggled autonomous off {0}\n'.format(datetime.datetime.now().strftime(time_format)))
      g_stop_event.set()
      g_ip_thread.join()
      g_camera.stop_recording()
      callback_switch_autonomous.is_auto=False
      g_stop_event.clear()
      for i in range(0, 5):
        dataline='{0}, {1}, {2}, {3}\n\n'.format(1, 1500, 1500, 0)
        print(dataline)
        g_serial.flushInput()
        g_serial.write(dataline.encode('ascii'))
        time.sleep(.05)
      GPIO.output(LED_names["autonomous"], GPIO.LOW)
    else:
      logging.debug('read another low transition while not autonomous')
callback_switch_autonomous.is_auto=False

def callback_switch_collect_data(channel):
  time.sleep(.1)
  global g_camera
  global g_collector
  if (GPIO.input(switch_names["collect_data"]))==SWITCH_ON:
    if callback_switch_collect_data.is_recording==True:
      logging.debug('read another high transition while already recording\n')
    else:
      logging.debug('\n user toggled collect data on {0}\n'.format(datetime.datetime.now().strftime(time_format)))
      callback_switch_collect_data.is_recording=True
      g_camera.start_recording(g_collector, format='rgb')
      GPIO.output(LED_names["collect_data"], LED_ON)
  else:
    if callback_switch_collect_data.is_recording==True:
      logging.debug('\n user toggled collect data off {0}\n'.format(datetime.datetime.now().strftime(time_format)))
      g_camera.stop_recording()
      callback_switch_collect_data.is_recording=False
      GPIO.output(LED_names["collect_data"], LED_OFF)
    else:
      logging.debug('read another low transition while not data collecting')
callback_switch_collect_data.is_recording=False


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

#code is an int in range 0-63, consisting of binary on-off values for the leds. boot_RPi is MSB
def displayBinLEDCode(code): 
  GPIO.output(LED_names["boot_RPi"], (code>>5)&1)
  GPIO.output(LED_names["shutdown_RPi"], (code>>4)&1)
  GPIO.output(LED_names["autonomous"], (code>>3)&1)
  GPIO.output(LED_names["collect_data"], (code>>2)&1)
  GPIO.output(LED_names["save_to_USBdrive"], (code>>1)&1)
  GPIO.output(LED_names["read_from_USBdrive"], code&1)


def initialize_service():
  #initialize the serial port: if the first port fails, we try the other one
  global g_serial
  g_serial=0
  try:
    g_serial=serial.Serial('/dev/ttyACM1')
  except serial.SerialException:
    try:
      g_serial=serial.Serial('/dev/ttyACM0')
    except serial.SerialException:
      print('Cannot connect to serial port')

  #initialize the camera
  global g_camera
  g_camera=picamera.PiCamera()
  g_camera.resolution=(128, 96)
  g_camera.framerate=10
  #initialize the data collector object
  global g_collector
  g_collector=DataCollector(g_serial, "/home/pi/autonomous/data")
  #initialize the image frame to be shared in autonomous mode
  global g_image_data
  g_image_data=np.zeros((36, 128, 3), dtype=np.uint8) 
  #initialize some stuff needed for network thread
  global g_stop_event
  g_stop_event=threading.Event()
  global g_lock
  g_lock=threading.Lock()
  #this is the object the camera writes to in autonomous mode
  global g_getter
  g_getter=DataGetter()
  #this stuff sets up the network
  global g_graph
  g_graph=tf.get_default_graph()
  #model.load_weights('weights_2018-02-24_14-00-35_epoch_40.h5')
  model.load_weights('weights_2018-04-05_02-43-30_epoch_66.h5')
  model._make_predict_function()
  global g_steerstats
  g_steerstats=np.load('steerstats.npz')['arr_0']
  global g_ip_thread
  g_ip_thread=0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for led in LED_names.values():
  GPIO.setup(led, GPIO.OUT)
  GPIO.output(led, LED_OFF)

initialize_service()

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


input("Press enter to stop")
GPIO.cleanup()
