# Voice Assistant

This project manipulates a voice recording in order to be comprehensible to Amazon's Alexa.

### Prerequisites

This program uses Python modules that will need to be manually installed, including pyaudio, gpiozero, and librosa. To install, use the following commands:

```
pip3 install pyaudio
pip3 install gpiozero
pip3 install librosa
```

### Usage

The program runs with three command line arguments, input_file, output_file, and speed. The input file is a .wav audio file of a recorded Alexa command, and the output file should specify where to save the .wav output. Speed is an optional parameter that will specify how much the input file audio should be speed up.

```
python3 main.py [input_file] [output_file] -s [speed]
```

After running this command, an output file will be created, which can be played to Alexa to elict a response. 

### User Tutorial

To use the product, the user should press the button on the Raspberry Pi and speak their Alexa query into the microphone. When they are finished, they should press the button again. The system will process the command and play back a response. 

The light attached to the Raspberry Pi will inidicate the state of the program. When it is green, it is idle and ready to take in input. When it is blue, it is listening for audio input. When it is red, it is processing the input and getting a repsonse from Alexa. When it is purple, it is playing ALexa's response to the user. 

The user may also change the amount their audio will be sped up. To do so, press and hold the button for 5 seconds when the device is in an idle state (the light is green). The button can be released once the button flashes white. The light will then begin cycling through three colors (red, green, blue), each of which corresponds to a speed at which the audio will be processed--red is 2x, green 3x, and blue 4x. To select a speed, press and hold the button when the light is the desired color/corresponding speed and release when the light turns off. The device can now be used as normal but will use the newly selected speed in its audio processing!