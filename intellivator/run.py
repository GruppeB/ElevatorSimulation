import argparse
import sys
import json

from intellivator import elevator_environment
from intellivator.PersonStream import PersonStream
from intellivator.SimpleSingleElevator import SimpleSingleElevator
from intellivator.simulation_output import SimulationDump
from intellivator.simulation_output import write_summary

def run(args):
    params = elevator_environment.EnvironmentParameters(
        **json.load(args.env_params_file)
    )

    personstream =  PersonStream(args.arrivals_file)

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


    duration, statistics = elevator_environment.run_simulation(
        params,
        personstream,
        brain,
        state_change_listeners
    )

    if simulation_dump:
        simulation_dump.close()

    print()
    print('-' * 80)
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

    run(parser.parse_args())
