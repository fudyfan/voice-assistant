import argparse
import librosa
from pydub import AudioSegment
import soundfile
import numpy as np
import wave
import sys
import math
import contextlib
import struct
from low_pass_filter import *


class Processing:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def stretch(self, input_file, output_file, speed):
        '''Phase-vocoder time stretch demo function.

        :parameters:
        - input_file : str
            path to input audio
        - output_file : str
            path to save output (wav)
        - speed : float > 0
            speed up by this factor
        '''

        # 1. Load the wav file, resample
        y, sr = librosa.load(input_file, sr=16000, mono=True)

        # 2. Time-stretch through effects module
        y_stretch = librosa.effects.time_stretch(y, speed)

        librosa.output.write_wav(output_file, y_stretch, sr)

    def convert_16bit(self, file):
        data, samplerate = soundfile.read(file)
        soundfile.write(file, data, samplerate, subtype='PCM_16')

    def volume_adjust(self, file, decibels):
        voice = AudioSegment.from_wav(file)
        voice = voice + decibels
        voice.export(file, "wav")

    def apply_low_pass_filter(self, fname, outname):
        with contextlib.closing(wave.open(fname, 'rb')) as spf:
            sampleRate = spf.getframerate()
            ampWidth = spf.getsampwidth()
            nChannels = spf.getnchannels()
            nFrames = spf.getnframes()

            # Extract Raw Audio from multi-channel Wav File
            signal = spf.readframes(nFrames*nChannels)
            spf.close()
            channels = interpret_wav(
                signal, nFrames, nChannels, ampWidth, True)

            cutOffFrequency = calc_cutoff_freq(
                signal, nFrames*nChannels, sampleRate)

            # get window size
            # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
            freqRatio = (cutOffFrequency/sampleRate)
            N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)

            # Use moving average (only on first channel)
            filtered = running_mean(channels[0], N).astype(channels.dtype)

            wav_file = wave.open(outname, "w")
            wav_file.setparams((1, ampWidth, sampleRate, nFrames,
                                spf.getcomptype(), spf.getcompname()))
            wav_file.writeframes(filtered.tobytes('C'))
            wav_file.close()
