import argparse
import sys
import os
import avs
from processing import Processing
from recording import Recording
from gpiozero import Button
from alexa_client.alexa_client import helpers
import RPi.GPIO as GPIO
import time
import led
import json
from functools import partial

IN_TUTORIAL = False
IN_MENU = False

def launch_menu(button, light, processor):
    global IN_MENU
    IN_MENU = True

    # launch
    print("starting menu")

    # flash white 2 times
    light.change_color((), off_c=led.ALL)
    time.sleep(1)
    for _ in range(2):
        light.flash(led.ALL)

    # make sure user lets go of button
    button.wait_for_release()

    # iterate through options until user makes a choice
    cont = True
    while cont:
        for color in led.ALL:
            light.change_color(color)
            time.sleep(1.5)
            if button.is_pressed:
                light.change_color((), off_c=led.ALL)
                button.wait_for_release()
                if color == led.RED:
                    print("selected speed 1")
                    speed = 1.0
                    cont = False
                    break
                elif color == led.GRN:
                    print("selected speed 2")
                    speed = 2.0
                    cont = False
                    break
                else:
                    print("selected speed 3")
                    speed = 3.0
                    cont = False
                    break

    with open('save_state.json', 'w') as saveFile:
        saveFile.write(json.dumps({"savedSpeed":speed}, indent=4))

    processor.set_speed(speed)

    IN_MENU = False

def play_tutorial():
    global IN_TUTORIAL
    IN_TUTORIAL = True
    os.system("omxplayer audio_instrs/tutorial.mp3")
    IN_TUTORIAL = False

def main(input_file, output_file, speed, debug=False):
    """
    Main control flow for Voice Assistant device.
    """
    GPIO.setmode(GPIO.BOARD)
    button = Button(17)
    button.hold_time = 2
    button.when_held = play_tutorial
    light = led.LED()
    # pull last saved speed from json
    with open('save_state.json', 'r') as saveFile:
        response = json.load(saveFile)
    speed = float(response['savedSpeed'])

    if speed == 1:
        light.change_color(light.RED)
    elif speed == 2:
        light.change_color(light.GREEN)
    else:
        light.change_color(light.BLUE)


    client = avs.connect_to_avs()
    dialog_req_id = [helpers.generate_unique_id()]
    audio_process = Processing(input_file, output_file, speed, 15)
    os.system("omxplayer audio_instrs/startup.mp3")
    
    # check if should play tutorial, requires holding for 2 sec
    # button.wait_for_press()
    time.sleep(5)

    # at this point know they've held for 2 sec
    # if button.is_pressed:
    #     os.system("omxplayer audio_instrs/tutorial.mp3")
    #     button.wait_for_release()

    if IN_TUTORIAL:
        print("hello in tutorial")
        time.sleep(78)

    # reset hold time/when_held func to go to menu
    button.hold_time = 5
    button.when_held = partial(launch_menu, button, light, audio_process)

    try:
        while True:
            print("ready for input")
            light.change_color(led.GRN)

            # record from mic
            if input_file == "in.wav":
                button.wait_for_press()

                # check if should launch menu, requires holding for 5 sec
                # for _ in range(100):
                #     if not button.is_pressed:
                #         break
                #     time.sleep(0.05)

                # at this point know they've held for 5 sec
                # if button.is_pressed:
                #     speed = launch_menu(button, light)
                    # with open('save_state.json', 'w') as saveFile:
                    #     saveFile.write(json.loads({"savedSpeed":speed}, indent=4))
                    # continue

                if button.is_pressed:
                    button.wait_for_release()

                if IN_MENU:
                    while IN_MENU:
                        pass
                    continue

                rec = Recording(input_file)
                light.change_color(led.BLU)
                rec.record(button)

            light.change_color(led.ALL)
            if debug:
                output_file = input_file
            else:
                audio_process.apply()

            # send to avs
            # outfiles = avs.send_rec_to_avs(output_file, client)
            outfiles = avs.send_rec_to_avs(output_file, client, dialog_req_id)

            # play back avs response
            light.change_color(led.PUR)
            if not outfiles:
                light.change_color(led.RED)
                os.system("omxplayer audio_instrs/alexa-noresponse.mp3")
                print("Error, no outfiles")
                time.sleep(1)

            for of in outfiles:
                print("playing: " + of)
                os.system("omxplayer " + of)

            if input_file == 'in.wav':
                print("Command completed! Waiting for new input!")
            else:
                light.interrupt()
                break

    except KeyboardInterrupt:
        light.interrupt()


def process_arguments(args):
    '''Argparse function to get the program parameters'''
    parser = argparse.ArgumentParser(description='Voice assistant')
    parser.add_argument('-i', '--input_file',
                        action='store',
                        default="in.wav",
                        required=False,
                        help='path to the input file (wav)')
    parser.add_argument('-o', '--output_file',
                        action='store',
                        default="out.wav",
                        required=False,
                        help='path to the processed output (wav)')
    parser.add_argument('-s', '--speed',
                        action='store',
                        type=float,
                        default=2.0,
                        required=False,
                        help='speed')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='debug mode (omit voice processing steps)')
    return vars(parser.parse_args(args))


if __name__ == '__main__':
    parameters = process_arguments(sys.argv[1:])
    main(**parameters)
