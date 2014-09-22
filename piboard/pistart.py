# from time import sleep
# import serial
# ser = serial.Serial("/dev/ttyAMA0")
# # ser.write("UART the Font\n")
# while True:
  # ser.write("aaaaa\n")
  # sleep(1)
# read = ser.readline()
# print read
# ser.close()

#!/usr/bin/env python 

# Imports
from time import sleep
import RPi.GPIO as GPIO
import serial
import threading
import re


class LED:
  'Class for controling LEDs on H13467 board'
  
  def __init__(self, pin):
    self.pin = pin
    self.ledState = 0
    GPIO.setup(self.pin, GPIO.OUT)
    GPIO.output(self.pin, GPIO.LOW)

  def on(self):
    'turn LED on'
    self.ledState = 1
    GPIO.output(self.pin, GPIO.HIGH)
    print 'LED on'

  def off(self):
    'turn LED off'
    self.ledState = 0
    GPIO.output(self.pin, GPIO.LOW)
    print 'LED off'

  def toggle(self):
    'toggle the selected LED on and off'
    if self.ledState:
      self.off()
    else:
      self.on()


class BUTTON:
  'Class for sensing button on H13467 board'

  def __init__(self, pin):
    self.pin = pin
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    self.count = 0

  def isPressed(self):
    if GPIO.input(self.pin) == False:
      print 'Button Pressed!'
      self.count+=1

  def waitPress(self):
    while GPIO.input(self.pin):
      sleep(.05)
    print 'Button Pressed'

  def getCount(self):
    return self.count

  def isOdd(self):
    return self.count % 2 == 1


class BLUETOOTH:
  'Class to manage HC-06 BLUETOOTH board' 

  def __init__(self, piTxPin, piRxPin):
    self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
    # setup pins
    self.piTxPin = piTxPin
    self.piRxPin = piRxPin
    GPIO.setup(self.piTxPin, GPIO.OUT)
    GPIO.setup(self.piRxPin, GPIO.IN)

  def start(self):
    # start bt->serial thread
    self.receiver_thread = threading.Thread(target=self.reader)
    self.receiver_thread.setDaemon(1)
    self.receiver_thread.start()

  def stop(self):
    self.port.close()

  def send(self, btCmd):
    print "Sending: "+btCmd
    self.port.write("\r"+btCmd)
		
  def reader(self):
    'loop and read BT data'
    try:
      while True:
        btData = self.port.readline() #.rstrip("\n\lf")
        self.echoData(btData)
        # self.processData(btData)
    except:
      raise

  def echoData(self, data):
    print(data)


if __name__ == '__main__':
  # GPIO.setmode(GPIO.BCM)
  # LED1 = LED(18)
  # LED2 = LED(23)
  # LED3 = LED(24)
  # BTN  = BUTTON(25)
  # BT = BLUETOOTH(14, 15)
  # BT.start()

  print 'Use CTRL-C to end loop'
  try:
    print 'debug1'
    # port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
    # ser = serial.Serial("/dev/ttyAMA0")
    # # ser.write("UART the Font\n")
    # while True:
      # ser.write("aaaaa\n")
      # sleep(1)
    # read = ser.readline()
    # print read
    # ser.close()
    print 'debug2'
    while True:
      print 'TX: AT'
      port.write("AT\n")
      rcv = port.readline()
      print "RX: "+rcv
      # BTN.waitPress() # wait until key is pressed
      # LED1.toggle()
      # BT.send('AT')
      # print "Button has been pressed %s times" % BTN.getCount()
      # if BTN.isOdd():
        # LED2.on()
      # else:
        # LED2.off()
      # sleep(.5)
      # print chr(27) + "[2J"
  except KeyboardInterrupt:
    print '\nInterrupt caught'

  finally:
    print 'Tidy up before exit'
    GPIO.cleanup()
    BT.stop()
