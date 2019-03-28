import librosa
from pydub import AudioSegment
import soundfile
import wave
import math
import contextlib
from lowpass_helpers import *


class Processing:
    temp_file = 'temp.wav'

    def __init__(self, input_file, output_file, speed, decibels):
        self.input_file = input_file
        self.output_file = output_file
        self.speed = speed
        self.decibels = decibels

    def low_pass_filter(self):
        print("Applying low-pass filter to " + self.input_file)
        with contextlib.closing(wave.open(self.input_file, 'rb')) as spf:
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

            wav_file = wave.open(self.temp_file, "w")
            wav_file.setparams((1, ampWidth, sampleRate, nFrames,
                                spf.getcomptype(), spf.getcompname()))
            wav_file.writeframes(filtered.tobytes('C'))
            wav_file.close()

    def time_stretch(self):
        """Phase-vocoder time stretch function."""
        print("Speeding up by factor of " + str(self.speed))

        # 1. Load the wav file, resample
        y, sr = librosa.load(self.temp_file, sr=16000, mono=True)

        # 2. Time-stretch through effects module
        y_stretch = librosa.effects.time_stretch(y, self.speed)

        librosa.output.write_wav(self.temp_file, y_stretch, sr)

    def volume_adjust(self):
        voice = AudioSegment.from_wav(self.temp_file)
        voice = voice + self.decibels
        voice.export(self.temp_file, "wav")

    def convert_16bit(self):
        print("Converting to Signed 16 bit Little Endian, Rate 16000 Hz, Mono")
        data, samplerate = soundfile.read(self.temp_file)
        soundfile.write(self.output_file, data, samplerate, subtype='PCM_16')
