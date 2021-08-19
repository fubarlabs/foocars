import time
import datetime
import logging
import RPi.GPIO as GPIO
import picamera
import serial
import numpy as np
import threading
import tensorflow as tf
import argparse
import concurrent.futures
from .defines import *

# configure logging
time_format = '%Y-%m-%d_%H-%M-%S'
logging.basicConfig(filename='carLogger.log', level=logging.DEBUG)
logging.debug('\n\n New Test Session {0}\n'.format(
    datetime.datetime.now().strftime(time_format)))
DEBUG = False
print(f"mode: {MODE}")


# set up argument parsing
# carRunner --mode auto
# carRunner --mode manual
# carRunner --mode remote
parser = argparse.ArgumentParser(description='carRuner command line overides.')
parser.add_argument('--mode', default="manual", choices=["manual", "auto", "remote"], type=str)
args = parser.parse_args()
MODE = args.mode

from .dropout_model import model as model
from .dropout_model_throttle import model as model2

def save_data(imgs, IMUdata, RCcommands, img_file, IMUdata_file, RCcommands_file):
    start = time.time()
    np.savez(img_file, imgs)
    np.savez(IMUdata_file, IMUdata)
    np.savez(RCcommands_file, RCcommands)
    end = time.time()
    print(f"time for save: {end-start}")

# Data Logging for Data Collection Mode
class DataCollector(object):
    """this object is passed to the camera.start_recording function, which will treat it as a
            writable object, like a stream or a file"""

    def __init__(self, serial_obj, save_dir):
        assert serial_obj.isOpen() == True
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.save_dir = save_dir
        self.ser = serial_obj
        # Number of frames to bundle together in a file.
        self.num_frames = BUNDLE_NUM_FRAMES
        camera_image_frame = [self.num_frames] + list(CAMERA_IMAGE_FRAME)
        print(camera_image_frame)
        # We put the images in here
        self.imgs = np.zeros((camera_image_frame), dtype=np.uint8)
        # we put the imu data in here
        self.IMUdata = np.zeros((self.num_frames, 7), dtype=np.float32)
        # we put the RC data in here
        self.RCcommands = np.zeros((self.num_frames, 2), dtype=np.float16)
        # this is the variable to keep track of number of frames per datafile
        self.idx = 0
        nowtime = datetime.datetime.now()
        self.currtime = time.time()
        self.img_file = self.save_dir + \
            '/imgs_{0}'.format(nowtime.strftime(time_format))
        self.IMUdata_file = self.save_dir + \
            '/IMU_{0}'.format(nowtime.strftime(time_format))
        self.RCcommands_file = self.save_dir + \
            '/commands_{0}'.format(nowtime.strftime(time_format))

    def write(self, s):
        '''this is the function that is called every time the PiCamera has a new frame'''
        imdata = np.reshape(np.fromstring(
            s, dtype=np.uint8), CAMERA_IMAGE_FRAME, 'C')
        # now we read from the serial port and format and save the data:

        self.ser.flushInput()
        n_read_items = 0
        while n_read_items != 10:
            try:
                datainput = self.ser.readline()
                data = list(map(float, str(datainput, 'ascii').split(',')))
                n_read_items = len(data)
            except ValueError:
                continue
            if DEBUG:
                print(data)
        # Note: the data from the IMU requires some processing which does not happen here:
        self.imgs[self.idx] = imdata
        # command=data[0]
        accelData = np.array([data[1], data[2], data[3]], dtype=np.float32)
        gyroData = np.array([data[4], data[5], data[6]], )
        datatime = np.array([int(data[7])], dtype=np.float32)
        steer_command = int(data[8])
        thr_command = int(data[9])
        self.IMUdata[self.idx] = np.concatenate(
            (accelData, gyroData, datatime))
        self.RCcommands[self.idx] = np.array([steer_command, thr_command])
        self.idx += 1
        if self.idx == self.num_frames:  # default value is 200, unless user specifies otherwise
            self.idx = 0
            self.flush()
        # print(time.time()-self.currtime)
        # self.currtime=time.time()

    def flush(self):
        '''this function is called every time the PiCamera has taken self.num_frames N number of images default 100'''
        self.executor.submit(save_data, np.copy(self.imgs), np.copy(self.IMUdata), np.copy(
            self.RCcommands), self.img_file, self.IMUdata_file, self.RCcommands_file)
        # this new image file name is for the next chunk of data, which starts recording now
        nowtime = datetime.datetime.now()
        self.img_file = self.save_dir + \
            '/imgs_{0}'.format(nowtime.strftime(time_format))
        self.IMUdata_file = self.save_dir + \
            '/IMU_{0}'.format(nowtime.strftime(time_format))
        self.RCcommands_file = self.save_dir + \
            '/commands_{0}'.format(nowtime.strftime(time_format))
        self.imgs[:] = 0
        self.IMUdata[:] = 0
        self.RCcommands[:] = 0
        self.idx = 0

# Data Logging for Data Collection Mode
class AutoDataCollector(object):
    """this object is passed to the camera.start_recording function, which will treat it as a
            writable object, like a stream or a file"""

    def __init__(self, serial_obj, save_dir):
        assert serial_obj.isOpen() == True
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.save_dir = save_dir
        self.ser = serial_obj
        # Number of frames to bundle together in a file.
        self.num_frames = BUNDLE_NUM_FRAMES
        camera_image_frame = [self.num_frames] + list(CAMERA_IMAGE_FRAME)
        print(camera_image_frame)
        # We put the images in here
        self.imgs = np.zeros((camera_image_frame), dtype=np.uint8)
        # we put the imu data in here
        self.IMUdata = np.zeros((self.num_frames, 7), dtype=np.float32)
        # we put the RC data in here
        self.RCcommands = np.zeros((self.num_frames, 2), dtype=np.float16)
        # this is the variable to keep track of number of frames per datafile
        self.idx = 0
        nowtime = datetime.datetime.now()
        self.currtime = time.time()
        self.img_file = self.save_dir + \
            '/imgs_{0}'.format(nowtime.strftime(time_format))
        self.IMUdata_file = self.save_dir + \
            '/IMU_{0}'.format(nowtime.strftime(time_format))
        self.RCcommands_file = self.save_dir + \
            '/commands_{0}'.format(nowtime.strftime(time_format))

    def write(self, img):
        '''this is the function that is called every time the PiCamera has a new frame'''
        imdata = np.reshape(np.fromstring(
            img, dtype=np.uint8), CAMERA_IMAGE_FRAME, 'C')
        # now we read from the serial port and format and save the data:

        self.ser.flushInput()
        n_read_items = 0
        while n_read_items != 10:
            try:
                datainput = self.ser.readline()
                data = list(map(float, str(datainput, 'ascii').split(',')))
                n_read_items = len(data)
            except ValueError:
                continue
            if DEBUG:
                print(data)
        # Note: the data from the IMU requires some processing which does not happen here:
        self.imgs[self.idx] = imdata
        # command=data[0]
        accelData = np.array([data[1], data[2], data[3]], dtype=np.float32)
        gyroData = np.array([data[4], data[5], data[6]], )
        datatime = np.array([int(data[7])], dtype=np.float32)
        steer_command = int(data[8])
        thr_command = int(data[9])
        self.IMUdata[self.idx] = np.concatenate(
            (accelData, gyroData, datatime))
        self.RCcommands[self.idx] = np.array([steer_command, thr_command])
        self.idx += 1
        if self.idx == self.num_frames:  # default value is 200, unless user specifies otherwise
            self.idx = 0
            self.flush()
        # print(time.time()-self.currtime)
        # self.currtime=time.time()

    def flush(self):
        '''this function is called every time the PiCamera has taken self.num_frames N number of images default 100'''
        self.executor.submit(save_data, np.copy(self.imgs), np.copy(self.IMUdata), np.copy(
            self.RCcommands), self.img_file, self.IMUdata_file, self.RCcommands_file)
        # this new image file name is for the next chunk of data, which starts recording now
        nowtime = datetime.datetime.now()
        self.img_file = self.save_dir + \
            '/imgs_{0}'.format(nowtime.strftime(time_format))
        self.IMUdata_file = self.save_dir + \
            '/IMU_{0}'.format(nowtime.strftime(time_format))
        self.RCcommands_file = self.save_dir + \
            '/commands_{0}'.format(nowtime.strftime(time_format))
        self.imgs[:] = 0
        self.IMUdata[:] = 0
        self.RCcommands[:] = 0
        self.idx = 0


def imageprocessor(event, serial_obj):
    global g_imagedata
    global g_graph
    global g_lock
    global g_steerstats
    global g_throttlestats

    # __init__ the data storage

    time.sleep(1)
    while not event.is_set():
        g_lock.acquire()
        tmpimg = np.copy(g_imageData)
        g_lock.release()
        immean = tmpimg.mean()
        imvar = tmpimg.std()
        start = time.time()
        import pdb; pdb.set_trace()

        pred = model.predict(np.expand_dims(tmpimg, axis=0))
        steer_command = pred[0][0]*g_steerstats[1]+g_steerstats[0]

        throttle_pred = model2.predict(np.expand_dims(tmpimg, axis=0))
        throttle_command = throttle_pred[0][0] * \
            g_throttlestats[1]+g_throttlestats[0]

        if steer_command > 2000:
            steer_command = 2000
        elif steer_command < 1000:
            steer_command = 1000

        if throttle_command > 2000:
            throttle_command = 2000
        elif throttle_command < 1000:
            throttle_command = 1000

        end = time.time()
        print(f"time for preds: {end-start}")

        dataline = '{0}, {1}, {2}, {3}\n'.format(
            commandEnum.RUN_AUTONOMOUSLY, int(steer_command), int(throttle_command), 0)
        if DEBUG:
            print(dataline)
        try:
            serial_obj.write(dataline.encode('ascii'))
            serial_obj.flush()
            print("serial write done")
            import pdb; pdb.set_trace()

            # TODO: output buffer...future
            # write stores the info info a bundle of n number frames
            # flush writes those frames to the output files
            # save tmpimg
            #  write_log(tmpimg, g_serial.readline())
            #g_auto_collector.write(tmpimg)
        except Exception as e:
            print(f"serial issue error: {e}")

# In automous mode read the g_serial response and save in appropriate files.
def write_log(img, serial_text):
    datainput=serial_text
    data=list(map(float, str(datainput, 'ascii').split(',')))
    n_read_items=len(data)
    print(f"serial: {data}")

class DataGetter(object):
    def __init__(self):
        pass

    def write(self, s):
        global g_imageData
        global g_lock
        imagerawdata = np.reshape(np.fromstring(
            s, dtype=np.uint8), (96, 128, 3), 'C')
        imdata = imagerawdata[20:56, :]
        immean = imdata.mean()
        imvar = imdata.std()
        g_lock.acquire()
        g_imageData = np.copy((imdata-immean)/imvar)
        g_lock.release()

    def flush(self):
        pass


def callback_thr_steps(channel):
    global THR_POS
    global THR_CURRENT

    if GPIO.input(switch_names["thr_step"]) != SWITCH_ON:
        return
    GPIO.output(LED_names["boot_RPi"], LED_OFF)
    if THR_POS < len(THR_STEPS):
        THR_CURRENT = THR_STEPS[THR_POS]
        print(f'THR_CURRENT: {THR_STEPS[THR_POS]}')
        THR_POS = THR_POS + 1
    else:
        THR_POS = 0
    time.sleep(.5)
    GPIO.output(LED_names["boot_RPi"], LED_ON)


def callback_switch_autonomous(channel):
    
    time.sleep(.1)
    if (GPIO.input(switch_names["autonomous"])) == SWITCH_ON:
        if callback_switch_autonomous.is_auto == True:
            logging.debug('read another high transition while in autonomous')
        else:
            print("Switch Autonomous: On")
            autonomous(True)
    else:  # switch off, second edge detect
        if callback_switch_autonomous.is_auto == True:
            print("Switch Autonomous: Off")
            autonomous(False)
        else:
            logging.debug('read another low transition while not autonomous')


callback_switch_autonomous.is_auto = False


def autonomous(mode):
    global g_getter
    global g_stop_event
    global g_ip_thread
    global g_camera
    global g_serial

    if mode == True:
        print("Autonomous: On")
        logging.debug('\n user toggled autonomous on {0}\n'.format(
            datetime.datetime.now().strftime(time_format)))
        g_camera.start_recording(g_getter, format='rgb')
        g_ip_thread = threading.Thread(target=imageprocessor, args=[
                                       g_stop_event, g_serial])
        g_ip_thread.start()
        logging.debug('in autonomous mode')
        callback_switch_autonomous.is_auto = True
        GPIO.output(LED_names["autonomous"], GPIO.HIGH)
    else:  # autonomous off
        print("Autonomous: Off")
        logging.debug('\n user toggled autonomous off {0}\n'.format(datetime.datetime.now().strftime(time_format)))
        if not g_stop_event.isSet(): #if the event isn't already set, then stop autonomous is triggered by the switch
            g_stop_event.set() #stop autonomous thread
        g_ip_thread.join() #join the autonomous thread
        g_camera.stop_recording()
        callback_switch_autonomous.is_auto=False
        GPIO.output(LED_names["autonomous"], GPIO.LOW)
        g_stop_event.clear() #clear stop event so we can reenter autonomous


def callback_switch_collect_data(channel):
    time.sleep(.1)
    global g_camera
    global g_collector
    if (GPIO.input(switch_names["collect_data"]))==SWITCH_ON:
        if callback_switch_collect_data.is_recording==True:
            logging.debug('read another high transition while already recording\n')
        else:
            print("Data Collection: On")
            logging.debug('\n user toggled collect data on {0}\n'.format(datetime.datetime.now().strftime(time_format)))
            callback_switch_collect_data.is_recording=True
            g_camera.start_recording(g_collector, format='rgb')
            GPIO.output(LED_names["collect_data"], LED_ON)
    else:
        if callback_switch_collect_data.is_recording==True:
            print("Data Collection: Off")
            logging.debug('\n user toggled collect data off {0}\n'.format(datetime.datetime.now().strftime(time_format)))
            g_camera.stop_recording()
            callback_switch_collect_data.is_recording=False
            GPIO.output(LED_names["collect_data"], LED_OFF)
        else:
            logging.debug('read another low transition while not data collecting')
callback_switch_collect_data.is_recording=False

# code is an int in range 0-63, consisting of binary on-off values for the leds. boot_RPi is MSB
def displayBinLEDCode(code): 
    GPIO.output(LED_names["boot_RPi"], (code>>1)&1)
    GPIO.output(LED_names["autonomous"], (code>>2)&1)
    GPIO.output(LED_names["collect_data"], (code)&1)

def initialize_service():
    # initialize the serial port: if the first port fails, we try the other one
    global g_serial
    try:
        g_serial=serial.Serial('/dev/ttyAMA0')
    except serial.SerialException:
        try:
            g_serial=serial.Serial('/dev/ttyACM1')
        except serial.SerialException:
            try:
                g_serial=serial.Serial('/dev/ttyACM0')
            except serial.SerialException:
                logging.debug("error: cannot connect to serial port")
    # initialize the camera
    global g_camera
    g_camera=picamera.PiCamera()
    g_camera.resolution=CAMERA_RESOLUTION
    g_camera.framerate=FRAME_RATE
    # initialize the data collector object
    global g_collector
    g_collector=DataCollector(g_serial, COLLECT_DIR)
    #init the autonomous data collector object
    #global g_auto_collector
    #g_auto_collector=AutoDataCollector(g_serial, COLLECT_DIR)
    # initialize the image frame to be shared in autonomous mode
    global g_image_data
    g_image_data=np.zeros(AUTO_IMAGE_FRAME, dtype=np.uint8) 
    # initialize some stuff needed for network thread
    global g_stop_event
    g_stop_event=threading.Event()
    global g_lock
    g_lock=threading.Lock()
    # this is the object the camera writes to in autonomous mode
    global g_getter
    g_getter=DataGetter()

    # this stuff sets up the network
    model.load_weights(WEIGHTS_FILE)
    global g_steerstats
    g_steerstats=np.load(STEERSTATS_FILE)['arr_0']

    model2.load_weights(THROTTLE_WEIGHTS_FILE)
    global g_throttlestats
    g_throttlestats=np.load(THROTTLESTATS_FILE)['arr_0']

    global g_ip_thread
    g_ip_thread=0
    print("Car Ready!")

def main():
    try:
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

        # Leave an indicator that the PI is booted
        GPIO.output(LED_names["boot_RPi"], LED_ON)

        for switch in switch_names.values():
            GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # default for g_auto_mode
        global g_auto_mode
        g_auto_mode=False
        # Check what mode the car is in, manual, auto, remote
        if MODE == "manual":
            GPIO.add_event_detect(switch_names["thr_step"], GPIO.FALLING, callback=callback_thr_steps, bouncetime=50)
            GPIO.add_event_detect(switch_names["autonomous"], GPIO.BOTH, callback=callback_switch_autonomous, bouncetime=200)
            GPIO.add_event_detect(switch_names["collect_data"], GPIO.BOTH, callback=callback_switch_collect_data, bouncetime=50)

        if MODE == "auto":
                print("Autonomous: On")
                g_auto_mode = True
                autonomous(g_auto_mode)
                
        printcount=0
        while(True):
            time.sleep(.001)
            # Check if vehicle is in autonomous mode
            if callback_switch_autonomous.is_auto==True: 
                g_auto_mode=True
                printcount=printcount+1
                # while we are in autonomous mode, we have to poll Arduino for stop signal
                g_serial.flushInput()
                n_read_items=0
                while n_read_items!=10:
                    try:
                        datainput=g_serial.readline()
                        data=list(map(float, str(datainput, 'ascii').split(',')))
                        n_read_items=len(data)
                    except ValueError:
                        continue

                if printcount==10:
                    print(data)
                    printcount=0
                if data[0]==commandEnum.RC_SIGNALED_STOP_AUTONOMOUS: #if we get a stop signal
                    autonomous(False)
                    g_stop_event.set() #stop the autonomous thread
                    g_auto_mode=False
                    callback_switch_autonomous.is_auto=False
                    print(f"callback_switch_autonomous.is_auto = {callback_switch_autonomous.is_auto}")
                    for i in range(0, 5): #send ack 5 times
                        time.sleep(.01)
                        dataout='{0}, {1}, {2}, {3}\n'.format(commandEnum.STOPPED_AUTO_COMMAND_RECIEVED, 1500, 1500, 0)
                        g_serial.write(dataout.encode('ascii'))
                    while callback_switch_autonomous.is_auto==True: #blink the led until user turns off the switch
                        time.sleep(.5)
                        GPIO.output(LED_names["autonomous"], GPIO.HIGH)
                        time.sleep(.5)
                        GPIO.output(LED_names["autonomous"], GPIO.LOW)
            
            # Check if the vehicle is autonomous mode and has switched off autonomous mode
            if g_auto_mode==True and callback_switch_autonomous.is_auto==False:
                dataout='{0}, {1}, {2}, {3}\n'.format(commandEnum.STOP_AUTONOMOUS, 1500, 1500, 0)
                g_serial.write(dataout.encode('ascii'))
                g_serial.flush()
                g_serial.flushInput()
                n_read_items=0
                while n_read_items!=10:
                    try:
                        datainput=g_serial.readline()
                        data=list(map(float, str(datainput, 'ascii').split(',')))
                        n_read_items=len(data)
                    except ValueError:
                        continue
                while data[0]!=commandEnum.STOPPED_AUTO_COMMAND_RECIEVED:
                    g_serial.write(dataout.encode('ascii'))
                    g_serial.flush()
                    g_serial.flushInput()
                    n_read_items=0
                    while n_read_items!=10:
                        try:
                            datainput=g_serial.readline()
                            data=list(map(float, str(datainput, 'ascii').split(',')))
                            n_read_items=len(data)
                        except ValueError:
                            continue
                g_auto_mode=False
    finally:            
        GPIO.output(LED_names["boot_RPi"], GPIO.LOW)
        GPIO.cleanup()
        g_camera.close()
        g_serial.close()
        print("EXIT")

if __name__ == "__main__":
    main()
