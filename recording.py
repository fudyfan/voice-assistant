import pyaudio
import wave
import time

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

    def record(self, button):
        # for timeout
        time_start = time.time()
        while True:
            data = self.stream.read(CHUNK)
            self.frames.append(data)
            time2 = time.time()

            if button.is_pressed or ( (time2 - time_start) >= 30 ):
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

                return
