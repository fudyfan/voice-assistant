import pyaudio
import wave
import time
from recording import Recording
from gpiozero import Button

button = Button(17)
button.wait_for_press()

rec = Recording("out.wav")
rec.record(button)