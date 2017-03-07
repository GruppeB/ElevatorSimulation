#!/usr/bin/python3

import argparse
import os
from glob import glob
from subprocess import call


def run(args):
    call('gnuplot gnuplots/{}.gp'.format(args.plot), shell=True)


def main():
    parser = argparse.ArgumentParser(
        description = 'Script to aid plotting of simulation plots'
    )

    plots = sorted([
        os.path.splitext(os.path.basename(path))[0]
        for path in glob('gnuplots/*.gp')
    ])

    parser.add_argument(
        'plot',
        help = 'What to plot',
        choices = plots
    )

    run(parser.parse_args())


if __name__ == "__main__":
    main()
