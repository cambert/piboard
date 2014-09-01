__author__ = 'Robert'

print "-----------"
print "  3-blink  "
print "-----------"

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

# for i in range(1,5):
while 1:
	print "Lights on"
	GPIO.output(18,GPIO.HIGH)
	GPIO.output(23,GPIO.HIGH)
	GPIO.output(24,GPIO.HIGH)
	time.sleep(1)
	print "Lights off"
	GPIO.output(18,GPIO.LOW)
	GPIO.output(23,GPIO.LOW)
	GPIO.output(24,GPIO.LOW)
	time.sleep(1)

GPIO.cleanup()
