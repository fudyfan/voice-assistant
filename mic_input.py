import pyaudio
import wave
import time
from gpiozero import Button
from functools import partial

def callback(in_data, frame_count, time_info, status):
    buffer.write(in_data)
    return (in_data, pyaudio.paContinue)

def record_audio():
  button = Button(17)
  button.wait_for_press()

  CHUNK = 1024
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 16000
  RECORD_SECONDS = 5
  WAVE_OUTPUT_FILENAME = "voice.wav"

  p = pyaudio.PyAudio()

  stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    stream_callback=callback,
)

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


  
