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
