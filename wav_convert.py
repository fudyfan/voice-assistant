from pydub import AudioSegment
import soundfile

def convert_16bit(file):
    data, samplerate = soundfile.read(file)
    soundfile.write(file, data, samplerate, subtype='PCM_16')

def volume_adjust(file, decibels):
    voice = AudioSegment.from_wav(file)
    voice = voice + decibels
    voice.export(file, "wav")

