import time
import serial
import threading
from defines import *


class SerialMonitor:
  def  __init__(self):
    self.commandlist=[commandEnum.NO_COMMAND_AVAILABLE, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.timestamp=time.time()
    self.writebuffer=[]
    self.skip_read_event=threading.Event() #event used as boolean to request serial reading
    self.term_event=threading.Event() #event used to terminate serial thread
    self.list_lock=threading.Lock() #lock used for read/writing self.commandList
    self.time_lock=threading.Lock() #lock used for read/writing self.timestamp
    self.buffer_lock=threading.Lock() #lock used for read/writing self.writebuffer
    self.skip_read_event.clear()
    self.term_event.clear()
    self.serial_obj=0
    try:
      self.serial_obj=serial.Serial('/dev/ttyACM1') #read timeout
      self.portName='dev/ttyACM1'
    except serial.SerialException:
      try: 
        self.serial_obj=serial.Serial('/dev/ttyACM0') #read timeout 
        self.portName='dev/ttyACM0'
      except serial.SerialException:
        print('Error: cannot connect to serial port')

  def monitor(self):
    while not self.term_event.is_set():
      self.buffer_lock.acquire()
      wb=self.writebuffer[:]
      self.buffer_lock.release()
      if wb!=[]: #if there is content in the write buffer
        assert(len(wb)==4)
        dataline='{0}, {1}, {2}, {3}\n'.format(wb[0], wb[1], wb[2], wb[3])
        self.serial_obj.write(dataline.encode('ascii'))
      n_read_items=0
      raw_serial_data=[]
      while n_read_items!=10 and not self.skip_read_event.is_set():
        try:
          self.serial_obj.flushInput()
          start=time.time()
          line_read=self.serial_obj.readline()
          stop=time.time()
          line_read=line_read.decode("utf-8")
          raw_serial_data=[float(i) for i in line_read.strip().split(',')]
          n_read_items=len(raw_serial_data)
        except ValueError: #value error will be thrown if serial line contains non-numerals
          n_read_items=0 #read another line
      if not self.skip_read_event.is_set() and n_read_items==10:
        self.list_lock.acquire()
        self.commandlist[:]=raw_serial_data[:]
        self.list_lock.release()
        self.time_lock.acquire()
        self.timestamp=time.time()
        self.time_lock.release()

  def elapsed_readtime(self): #return the elapsed time since last successful serial read
    self.time_lock.acquire()
    readtime=self.timestamp
    self.time_lock.release()
    return time.time()-readtime

  def read(self): #returns most recent serial data
    #if this function is called, and skip_read_event is set, we clear it, then wait
    #for a recent read
    if self.skip_read_event.is_set():
      self.skip_read_event.clear()
    #while self.elapsed_readtime()>.01: #TODO this number is a guess
      #pass
    self.list_lock.acquire()
    readlist=self.commandlist[:]
    self.list_lock.release()
    return readlist
      
  def write(self, writelist):
    if len(writelist)!=4: #list must have four items: command, steer, throttle, -
      return False 
    self.buffer_lock.acquire()
    self.writebuffer=writelist[:]
    self.buffer_lock.release()
    return True #return value of true from this function does not mean the list is written

  def set_read(self, value):
    #toggle serial reading
    #this is necessary to skip the read loop in the thread during a time when values 
    #are not expected
    if value==True:
      self.skip_read_event.clear()
    elif value==False:
      self.skip_read_event.set()

  def start_serial(self):
    self.thread=threading.Thread(target=self.monitor)
    self.thread.start()

  def stop_serial(self):
    self.term_event.set()
    self.thread.join()
    self.serial_obj.close()

