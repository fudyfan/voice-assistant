import RPi.GPIO as GPIO
import time

RED = 12
GRN = 33
BLU = 32
PINS = [RED,GRN,BLU]

class LED:
	def __init__(self):
		GPIO.setup(PINS, GPIO.OUT, initial=GPIO.LOW)

		# pins should be an iterable with pins of those you want turned on
		# all others will be turned off
		def turn_on(pins):
			for pin in pins:
				