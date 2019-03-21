import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

class Recording:
	def __init__(self, filename_):
		self.filename = filename_
		self.audio_instance = pyaudio.PyAudio()
		self.frames = []
		self.stream = self.audio_instance.open(
			format=pyaudio.paInt16,
			channels=CHANNELS,
			rate=RATE,
			input=True,
			frames_per_buffer=CHUNK
		)

		print("* recording")

	def __del__(self):
		print("* done recording")

		self.stream.stop_stream()
		self.stream.close()
		self.audio_instance.terminate()

		# write file
		wf = wave.open(self.filename, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(self.audio_instance.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(self.frames))
		wf.close()

	def record(self, button):
		while True:
			data = self.stream.read(CHUNK)
			self.frames.append(data)
			
			if button.is_pressed:
				return
