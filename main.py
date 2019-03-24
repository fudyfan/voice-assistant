from low_pass_filter import apply_low_pass_filter
from time_stretch import stretch
from wav_convert import convert_16bit, volume_adjust
import argparse
import sys
import pyaudio
import wave
import time
from recording import Recording
from gpiozero import Button
import real_avs
import os

def_input_string = '__def_input_string__'

def main(input_file, output_file, speed):
    print("ready for input")

    input_file_name = input_file
    if input_file == def_input_string:
        # record from mic?
        button = Button(17)
        button.wait_for_press()

        input_file_name = "out.wav"
        rec = Recording(input_file_name)
        rec.record(button)

    # low pass filter
    temp_fname = "temp.wav"
    print("Applying low-pass filter to {}".format(input_file_name))
    apply_low_pass_filter(input_file_name, temp_fname)

    # speed up
    print("Speeding up by factor of {}".format(speed))
    stretch(temp_fname, output_file, speed)

    volume_adjust(output_file, 15)

    # make sure formatted for avs
    print("Writing to {}".format(output_file))
    convert_16bit(output_file)
    print("Converting to Signed 16 bit Little Endian, Rate 16000 Hz, Mono")

    # send to avs
    client = real_avs.connect_to_avs()
    outfiles = real_avs.send_rec_to_avs(output_file, client)

    # play back avs response
    for of in outfiles:
        print("playing:" + of)
        os.system('omxplayer '+ of)



def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description='Voice assistant')

    parser.add_argument('-i', '--input_file', 
                        action='store',
                        default=def_input_string,
                        help='path to the input file (wav, mp3, etc)',
                        required=False)

    parser.add_argument('output_file',
                        action='store',
                        help='path to the processed output (wav)')

    parser.add_argument('-s', '--speed',
                        action='store',
                        type=float,
                        default=2.0,
                        required=False,
                        help='speed')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])
    main(**parameters)
