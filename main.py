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

RED = 12
GRN = 33
BLU = 32
PINS = [RED,GRN,BLU]

def turn_on(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turn_off(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

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
                turn_off(GRN)
                turn_on(BLU)
                rec = Recording(input_file)
                rec.record(button)
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
                break

            turn_off(BLU)
            turn_off(RED)
            turn_off(GRN)
    
    except KeyboardInterrupt:
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
