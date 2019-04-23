''' Test Cases. '''

import avs
import os
from low_pass_filter import apply_low_pass_filter
from time_stretch import stretch
from wav_convert import convert_16bit, volume_adjust
import argparse
import sys
import pyaudio
import wave
import time
from alexa_client.alexa_client import helpers

def test_avs:
    '''Tests that a prerecorded sample produces a result.'''
    input_file = "sample_audio/alexa_what_time_is_it.wav"
    dialog_req_id = helpers.generate_unique_id()
    client = avs.connect_to_avs()

    outfiles = avs.send_rec_to_avs(input_file, client, dialog_req_id)

    for of in outfiles:
        print("playing:" + of)
        os.system('mpg321 '+ of)
    

def test_brad:
    '''Tests that a recording from Brad produces a result.'''
    input_file = "sample_audio/flip_a_coin.wav"
    dialog_req_id = helpers.generate_unique_id()
    client = avs.connect_to_avs()   
    
    temp_fname = "temp.wav"
    apply_low_pass_filter(input_file, temp_fname)
    stretch(temp_fname, f, speed)
    volume_adjust(temp_fname, 15)
    convert_16bit(temp_fname)

    outfiles = avs.send_rec_to_avs(temp_fname, client, dialog_req_id)

    for of in outfiles:
        print("playing:" + of)
        os.system('mpg321 '+ of)


def test_incorrect:
    '''Tests that "bad input" produces an error message.'''
    input_file = "sample_audio/bad_recording.wav"
    dialog_req_id = helpers.generate_unique_id()
    client = avs.connect_to_avs()  

    convert_16bit(input_file)

    outfiles = avs.send_rec_to_avs(input_file, client, dialog_req_id)

    for of in outfiles:
        print("playing:" + of)
        os.system('mpg321 '+ of)


def main():
    print("Testing AVS...")
    test_avs()
    print("Testing Brad's recording...")
    test_brad()
    print("Testing bad input...")
    test_incorrect()


if __name__ == '__main__':
    main()