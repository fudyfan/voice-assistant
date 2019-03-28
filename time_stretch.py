import argparse
import librosa


def stretch(input_file, output_file, speed):
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
