# Testing ottoMicroLogger Commands

import unittest
import serial
import time

# **** fubarino not connected yet for debugging purposes ****
# Opens serial port to the arduino:
ser=serial.Serial('/dev/ttyACM0')



class TestCommands(unittest.TestCase):
  def test_hello(self):
    result = "hello"
    self.assertEqual(result, "hello")

  def test_run_autonomously(self):
    while( 1 ):
      # spaces after the commas throw an error
#      dataline='{0}, {1}, {2}, {3}\n'.format( 5, 1300, 1500, 0)
      dataline='{0}, {1}, {2}, {3}\n'.format( 5,1300,1500,0 )
      ser.write(dataline.encode('ascii'))
      time.sleep( .2)
      serial_line_received = ser.readline()
      serial_line_received = serial_line_received.decode("utf-8")
      raw_serial_list = list( serial_line_received.split(','))
      self.assertEqual(raw_serial_list[0], '5')
      self.assertEqual(raw_serial_list[1], '1300')
      self.assertEqual(raw_serial_list[2], '1500')


if __name__ == '__main__':
  unittest.main()