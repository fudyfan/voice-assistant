import RPi.GPIO as GPIO
class LED:
    RED = 0
    GRN = 0
    BLU = 0
    def __init__(self):
        self.RED = 12
        self.GRN = 33
        self.BLU = 32
        self.PINS = [RED,GRN,BLU]

    def turn_on_all():
        for pin in PINS:
            turn_on(pin)
    
    def turn_off_all():
        for pin in PINS:
            turn_off(pin)

    def turn_on(pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def turn_off(pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def change_color(off_c, on_c):
        turn_off(off_c)
        turn_on(on_c)

    def interupt():
        turn_off_all()
        GPIO.cleanup()

