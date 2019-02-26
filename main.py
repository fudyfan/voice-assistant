from low_pass_filter import apply_low_pass_filter
from time_stretch import stretch
import argparse
import sys
# import click

# @click.command()
# @click.argument('infile')
# @click.argument('outfile')
# @click.option('--speed', default=2, help='speed up by this factor')


def main(input_file, output_file, speed):
    temp_fname = "temp.wav"
    print("Applying low-pass filter to {}".format(input_file))
    apply_low_pass_filter(input_file, temp_fname)
    print("Speeding up by factor of {}".format(speed))
    stretch(temp_fname, output_file, speed)
    print("Writing to {}".format(output_file))


def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description='Voice assistant')

    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')

    parser.add_argument('output_file',
                        action='store',
                        help='path to the processed output (wav)')

    parser.add_argument('-s', '--speed',
                        action='store',
                        type=float,
                        default=2.0,
                        required=False,
                        help='speed')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments(sys.argv[1:])
    main(**parameters)
