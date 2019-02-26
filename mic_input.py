import pyaudio
import wave
import time
from gpiozero import Button
from functools import partial

def record_audio(button):
  CHUNK = 1024
  FORMAT = pyaudio.paInt16
  CHANNELS = 2
  RATE = 44100
  RECORD_SECONDS = 5
  WAVE_OUTPUT_FILENAME = "voice.wav"

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

  frames = []

  print("* recording")

  while True:
      data = stream.read(CHUNK)
      frames.append(data)
      if button.is_pressed:
        break

  print("* done recording")

  stream.stop_stream()
  stream.close()
  p.terminate()

  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()

  return


def get_input():
  # bind button to a pin (17)
  button = Button(17)
  button.when_pressed = partial(record_audio, button)


  
