import wave

CHANNELS = 1
swidth = 2
Change_RATE = 10

with wave.open('sample_audio/flip_a_coin.wav', 'rb') as spf:
    RATE = spf.getframerate()
    signal = spf.readframes(-1)

with wave.open('changed.wav', 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*Change_RATE)
    wf.writeframes(signal)
