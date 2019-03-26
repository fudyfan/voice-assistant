import argparse
import sys
import os
import avs
from recording import Recording
from gpiozero import Button
from alexa_client.alexa_client import helpers
from low_pass_filter import apply_low_pass_filter
from time_stretch import stretch
from wav_convert import convert_16bit, volume_adjust
import RPi.GPIO as GPIO
import time

RED = 12
GRN = 33
BLU = 32
PINS = [RED,GRN,BLU]

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

def launch_menu(button):
    print("starting menu")
    
    # flash white 2 times
    turn_off_all()
    time.sleep(1)
    for i in range(0, 2):
        turn_on_all()
        time.sleep(1)
        turn_off_all()
        time.sleep(1)

    # make sure user lets go of button
    button.wait_for_release()

    # iterate through options until user makes a choice
    while True:
        for pin in PINS:
            turn_on(pin)
            time.sleep(1.5)
            if button.is_pressed:
                turn_off(pin)
                button.wait_for_release()
                turn_off(pin)
                if pin == RED:
                    print("selected speed 2")
                    return 2.0
                elif pin == GRN:
                    print("selected speed 3")
                    return 3.0
                else:
                    print("selected speed 4")
                    return 4.0
            turn_off(pin)

def main(input_file, output_file, speed, debug=False):
    """
    Main control flow for Voice Assistant device.
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS, GPIO.OUT, initial=GPIO.LOW)
    button = Button(17)
    client = avs.connect_to_avs()
    dialog_req_id = helpers.generate_unique_id()

    try:
        while True:
            print("ready for input")
            turn_on(GRN)

            # record from mic
            if input_file == "in.wav":
                button.wait_for_press()

                # check if should launch menu, requires holding for 5 sec
                for i in range(100):
                    if not button.is_pressed:
                        break
                    time.sleep(0.05)

                # at this point know they've held for 5 sec
                if button.is_pressed:
                    speed = launch_menu(button)
                    continue

                rec = Recording(input_file)
                turn_off(GRN)
                turn_on(BLU)
                rec.record(button)
            
            turn_off(GRN)
            turn_off(BLU)

            turn_on(RED)
            if debug:
                output_file = input_file
            else:
                # low pass filter
                temp_fname = "temp.wav"
                print("Applying low-pass filter to {}".format(input_file))
                apply_low_pass_filter(input_file, temp_fname)

                # speed up
                print("Speeding up by factor of {}".format(speed))
                stretch(temp_fname, output_file, speed)

                # may not be necessary, or can try to do this dynamically
                volume_adjust(output_file, 15)

                # make sure formatted for avs
                print("Converting to Signed 16 bit Little Endian, Rate 16000 Hz, Mono")
                convert_16bit(output_file)

            # send to avs
            outfiles = avs.send_rec_to_avs(output_file, client)
            # outfiles = avs.send_rec_to_avs(output_file, client, dialog_req_id)

            # play back avs response
            turn_on(BLU)
            for of in outfiles:
                print("playing: " + of)
                os.system("omxplayer " + of)

            if input_file == 'in.wav':
                print("Command completed! Waiting for new input!")
            else:
                turn_off_all()
                break

            turn_off_all()
    
    except KeyboardInterrupt:
        turn_off_all()
        GPIO.cleanup()


def process_arguments(args):
    '''Argparse function to get the program parameters'''
    parser = argparse.ArgumentParser(description='Voice assistant')
    parser.add_argument('-i', '--input_file',
                        action='store',
                        default="in.wav",
                        required=False,
                        help='path to the input file (wav)')
    parser.add_argument('-o', '--output_file',
                        action='store',
                        default="out.wav",
                        required=False,
                        help='path to the processed output (wav)')
    parser.add_argument('-s', '--speed',
                        action='store',
                        type=float,
                        default=2.0,
                        required=False,
                        help='speed')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='debug mode (omit voice processing steps)')
    return vars(parser.parse_args(args))


if __name__ == '__main__':
    parameters = process_arguments(sys.argv[1:])
    main(**parameters)
