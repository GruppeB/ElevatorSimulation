import argparse
import sys
import json
from unittest import defaultTestLoader, TestResult

from intellivator import elevator_environment
from intellivator.PersonStream import PersonStream
from intellivator.SimpleSingleElevator import SimpleSingleElevator
from intellivator.simulation_output import *

class TermColor:
    PURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_tests():
    result = TestResult()
    print(TermColor.BOLD + 'Running tests ... ' + TermColor.ENDC, end='')
    defaultTestLoader.discover('.').run(result)
    if result.wasSuccessful():
        print(TermColor.OKGREEN + 'Passed' + TermColor.ENDC)
    else:
        print(TermColor.FAIL + 'Failed' + TermColor.ENDC)
    print()

    return result.wasSuccessful()

def create_data_listeners():
    listeners = []

    listeners.append(StateChangeTimeSeries(
        ('\# waiting persons',),
        number_of_persons_waiting,
        open('data/waiting_persons.data', 'w')
    ))

    return listeners

def run(args):
    print()

    if not args.ignore_tests:
        if not run_tests():
            return

    params = elevator_environment.EnvironmentParameters(
        **json.load(args.env_params_file)
    )

    brain = None
    if args.brain == 'SimpleSingleElevator':
        brain = SimpleSingleElevator(params)
    else:
        raise Exception('Brain not recognized')

    simulation_listeners = []

    if args.save_data:
        simulation_listeners.extend(create_plot_data_listeners())

    if args.state_dump_file:
        simulation_listeners.append(StateDump(args.state_dump_file, params))

    print('Running simulation with ' + TermColor.BOLD + args.brain + TermColor.ENDC)

    print()
    print('-' * 80)
    print()

    simulation_listeners.append(ProgressOutput(args.arrivals_file, sys.stdout))

    personstream = PersonStream(args.arrivals_file)
    duration, statistics = elevator_environment.run_simulation(
        params,
        personstream,
        brain,
        simulation_listeners
    )

    print()
    print('-' * 80)
    print()
    print(TermColor.BOLD + 'Summary' + TermColor.ENDC)
    print()
    write_summary(duration, statistics, sys.stdout)
    print()
    print('-' * 80)
    print()



def main():
    parser = argparse.ArgumentParser(
        description = 'Script to run elevator simulations'
    )
    parser.add_argument(
        'arrivals_file',
        type = argparse.FileType('r'),
        help = 'File with arrivals'
    )
    parser.add_argument(
        'env_params_file',
        type = argparse.FileType('r'),
        help = 'JSON file with environment paramaters'
    )
    parser.add_argument(
        'brain',
        choices = ['SimpleSingleElevator'],
        help = 'Which elevator brain to use'
    )
    parser.add_argument(
        '-s', '--state-dump-file',
        type = argparse.FileType('w'),
        help = 'Dump simulation data to this file'
    )
    parser.add_argument(
        '--ignore-tests',
        action = 'store_true',
        help = "Don't run the tests"
    )
    parser.add_argument(
        '-d', '--save-data',
        action = 'store_true',
        help = 'Save simulation data in the data folder'
    )

    run(parser.parse_args())
