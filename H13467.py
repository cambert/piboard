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


class BUT:
  'Class for sensing button on H13467 board'

  def __init__(self, pin):
    self.pin = pin
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    self.count = 0

  def isPressed(self):
    if GPIO.input(self.pin) == False:
      print 'Button Pressed!'
      self.count+=1

  def getCount(self):
    return self.count

  def isOdd(self):
    return self.count % 2 == 1


class GPS:
  'Class for getting information for GPS module on H13467 board'

  def __init__(self, awakePin, onOffPin):
    self.port = serial.Serial("/dev/ttyAMA0", baudrate=4800, timeout=3.0)
    # Store GPS information
    self.SIV = 0
    # setup pins
    self.awakePin = awakePin
    self.onOffPin = onOffPin
    GPIO.setup(self.awakePin, GPIO.IN)
    GPIO.setup(self.onOffPin, GPIO.OUT)
    # send pulse to switch module on __|--|__
    GPIO.output(self.onOffPin, GPIO.LOW)
    sleep(0.2)
    GPIO.output(self.onOffPin, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(self.onOffPin, GPIO.LOW)

  def start(self):
    # start gps->serial thread
    self.receiver_thread = threading.Thread(target=self.reader)
    self.receiver_thread.setDaemon(1)
    self.receiver_thread.start()

  def stop(self):
    self.port.close()

  def isAwake(self):
    return GPIO.input(self.awakePin)

  def reader(self):
    'loop and read GPS data'
    try:
      while self.isAwake():
        gpsData = self.port.readline().rstrip("\n\lf")
        # self.echoData(gpsData)
        self.processData(gpsData)

    except:
      raise

  def echoData(self, data):
    print(data)

  def processData(self, data):
    if 'GPGSV' in data:
      gsvData = re.split(',|\*', data)
      self.SIV = gsvData[3]

  def getSIV(self):
    return self.SIV


if __name__ == '__main__':
  GPIO.setmode(GPIO.BCM)
  LD1 = LED(25)
  BTN  = BUT(23)
  LD2 = LED(24)
  GPS1 = GPS(18, 22)
  GPS1.start()

  print 'Use CTRL-C to end loop'
  try:
    while 1:
      LD1.toggle()
      BTN.isPressed()
      print "Button has been pressed %s times" % BTN.getCount()
      if BTN.isOdd():
        LD2.on()
      else:
        LD2.off()
      print "GPS module is awake %s" % GPS1.isAwake()
      print "Satalites in view is: %s" % GPS1.getSIV()
      sleep(1)
      print chr(27) + "[2J"

  except KeyboardInterrupt:
    print '\nInterrupt caught'

  finally:
    print 'Tidy up before exit'
    GPIO.cleanup()
    GPS1.stop()
