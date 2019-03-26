# referenced https://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python

import numpy as np
import wave
import sys
import math
import contextlib
import struct


def calc_cutoff_freq(data, data_size, frate):
    data = struct.unpack('{n}h'.format(n=data_size), data)
    data = np.array(data)
    w = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(w))
    # be careful, may need to sanity check the cutoff returned
    cutoff = np.percentile(freqs, 60)
    return cutoff*frate


# from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
def running_mean(x, windowSize):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


# from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved=True):

    if sample_width == 1:
        dtype = np.uint8  # unsigned char
    elif sample_width == 2:
        dtype = np.int16  # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels


def apply_low_pass_filter(fname, outname):
    with contextlib.closing(wave.open(fname, 'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()

        # Extract Raw Audio from multi-channel Wav File
        signal = spf.readframes(nFrames*nChannels)
        spf.close()
        channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

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
