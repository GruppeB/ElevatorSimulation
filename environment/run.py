import argparse
import sys
import json
from unittest import defaultTestLoader, TestResult

from environment import elevator_environment
from environment.PersonStream import PersonStream
from agent.SimpleSingleElevator import SimpleSingleElevator
from agent.MovingAverageSingleElevator import MovingAverageSingleElevator
from agent.MovingModeSingleElevator import MovingModeSingleElevator
from agent.HistoryAverageSingleElevator import HistoryAverageSingleElevator
from agent.HistoryModeSingleElevator import HistoryModeSingleElevator
from environment.simulation_output import *

elevator_agents = {
    'SimpleSingleElevator': SimpleSingleElevator,
    'MovingAverageSingleElevator': MovingAverageSingleElevator,
    'MovingModeSingleElevator': MovingModeSingleElevator,
    'HistoryAverageSingleElevator': HistoryAverageSingleElevator,
    'HistoryModeSingleElevator': HistoryModeSingleElevator
}

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

def create_data_listeners(params):
    return [
        SimulationTimeSeries(
            column_names = ('# waiting persons',),
            data_file = open('data/waiting_persons.data', 'w'),
            state_changed = lambda c: (len(c.new_env_state.waiting_persons),)
        ),
        SimulationTimeSeries(
            column_names = tuple(
                '# persons in elevator {}'.format(i)
                for i in range(0, params.number_of_elevators)
            ),
            data_file = open('data/persons_in_elevators.data', 'w'),
            state_changed = lambda c: tuple(
                len(elevator_state.persons)
                for elevator_state in c.new_env_state.elevator_states.values()
            )
        ),
        SimulationTimeSeries(
            column_names = ('Waiting time',),
            data_file = open('data/waiting_times.data', 'w'),
            person_picked_up = lambda t, wp, e: (t - wp.person.arrival_time,)
        ),
        SimulationTimeSeries(
            column_names = ('Service time',),
            data_file = open('data/service_times.data', 'w'),
            person_finished = lambda t, p, e: (t - p.arrival_time,)
        )
    ]

def create_statistics(params):
    return [
        SimulationStatistic(
            name = 'Served persons',
            start_value = 0,
            person_finished = lambda v, *x: v + 1
        ),
        SimulationStatistic(
            name = 'Total waiting time',
            start_value = 0,
            person_picked_up = lambda v, t, wp, e: v + t - wp.person.arrival_time
        ),
        SimulationStatistic(
            name = 'Average waiting time',
            start_value = (0, 0),
            person_picked_up = lambda v, t, wp, e: (v[0] + t - wp.person.arrival_time, v[1]),
            person_finished = lambda v, *x: (v[0], v[1] + 1),
            result = lambda v: v[0] / v[1]
        ),
        SimulationStatistic(
            name = 'Total service time',
            start_value = 0,
            person_finished = lambda v, t, p, e: v + t - p.arrival_time
        ),
        SimulationStatistic(
            name = 'Average service time',
            start_value = (0, 0),
            person_finished = lambda v, t, p, e: (v[0] + t - p.arrival_time, v[1] + 1),
            result = lambda v: v[0] / v[1]
        ),
    ]

def run(args):
    print()

    if not args.ignore_tests:
        if not run_tests():
            return

    params = elevator_environment.EnvironmentParameters(
        **json.load(args.env_params_file)
    )

    if args.agent not in elevator_agents:
        raise Exception('Agent not recognized')
    agent = elevator_agents[args.agent](params)

    simulation_listeners = []

    statistics = create_statistics(params)
    simulation_listeners.extend(statistics)

    if args.save_data:
        simulation_listeners.extend(create_data_listeners(params))

    if args.state_dump_file:
        simulation_listeners.append(StateDump(args.state_dump_file, params))

    print('Running simulation with ' + TermColor.BOLD + args.agent + TermColor.ENDC)

    print()
    print('-' * 80)
    print()

    simulation_listeners.append(ProgressOutput(args.arrivals_file, sys.stdout))

    personstream = PersonStream(args.arrivals_file)
    duration = elevator_environment.run_simulation(
        params,
        personstream,
        agent,
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
        'agent',
        choices = list(elevator_agents.keys()),
        help = 'Which elevator agent to use'
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
