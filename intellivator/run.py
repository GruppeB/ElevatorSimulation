import argparse
import sys
import json
from unittest import defaultTestLoader, TestResult

from intellivator import elevator_environment
from intellivator.PersonStream import PersonStream
from intellivator.SimpleSingleElevator import SimpleSingleElevator
from intellivator.simulation_output import SimulationDump
from intellivator.simulation_output import ProgressOutput
from intellivator.simulation_output import write_summary

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

    state_change_listeners = []

    simulation_dump = None
    if args.dump_file:
        simulation_dump = SimulationDump(args.dump_file, params)
        state_change_listeners.append(simulation_dump.env_state_has_changed)

    print('Running simulation with ' + TermColor.BOLD + args.brain + TermColor.ENDC)

    print()
    print('-' * 80)
    print()

    progress_output = ProgressOutput(args.arrivals_file, sys.stdout)
    state_change_listeners.append(progress_output.env_state_has_changed)

    personstream = PersonStream(args.arrivals_file)
    duration, statistics = elevator_environment.run_simulation(
        params,
        personstream,
        brain,
        state_change_listeners
    )

    progress_output.done()

    if simulation_dump:
        simulation_dump.close()

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
        '--dump-file',
        type = argparse.FileType('w'),
        help = 'Dump simulation data to this file'
    )
    parser.add_argument(
        '--ignore-tests',
        action = 'store_true',
        help = "Don't run the tests"
    )

    run(parser.parse_args())
