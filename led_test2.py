import RPi.GPIO as GPIO
import threading
import time
import random

# define pins for each color
RED = 12
GRN = 33
BLU = 32

def turn_on(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turn_off(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
 
def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS, GPIO.OUT, initial=GPIO.LOW)

    turn_on(RED)
    time.sleep(1)
    
    turn_off(RED)
    turn_on(GRN)
    time.sleep(1)

    turn_off(GRN)
    turn_on(BLU)
    time.sleep(1)

    turn_on(GRN)
    time.sleep(1)
    turn_on(RED)
    time.sleep(1)
 
    GPIO.cleanup()
 
if __name__ == '__main__':
    main()