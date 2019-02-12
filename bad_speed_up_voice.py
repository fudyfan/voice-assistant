import wave

CHANNELS = 1
swidth = 2
Change_RATE = 10

spf = wave.open('flip_a_coin.wav', 'rb')
RATE=spf.getframerate()
signal = spf.readframes(-1)

wf = wave.open('changed.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(swidth)
wf.setframerate(RATE*Change_RATE)
wf.writeframes(signal)
wf.close()
