import RPi.GPIO as GPIO
import time

RED = (12)
GRN = (33)
BLU = (32)
PUR = (RED, BLU)
ALL = (RED, GRN, BLU)

class LED:
    def __init__(self):
        self.PINS = [RED,GRN,BLU]
        GPIO.setup(self.PINS, GPIO.OUT, initial=GPIO.LOW)

    def turn_on(self, pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def turn_off(self, pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    # off_c and on_c are iterables
    def change_color(self, on_c, off_c=ALL):
        for p in off_c:
            turn_off(off_c)
        for p in on_c:
            turn_on(on_c)

    # on_c is an iterable
    def flash(self, on_c, off_c=ALL):
        turn_on_all()
        time.sleep(1)
        turn_off_all()
        time.sleep(1)

    def interrupt(self):
        turn_off_all()
        GPIO.cleanup()

