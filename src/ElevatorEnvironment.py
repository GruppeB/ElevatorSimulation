from collections import namedtuple
from enum import IntEnum

Event = namedtuple('Event', ['time', 'arrival_floor', 'destination_floor'])

class Direction(IntEnum):
    self.UP = 1
    self.NONE = 0
    self.DOWN = -1

Person = namedtuple('Person', ['arrival_time', 'destination_floor'])
WaitingPerson = namedtuple('WaitingPerson', ['person', 'arrival_floor'])
ElevatorState = namedtuple('ElevatorState', ['position', 'direction', 'persons'])
EnvironmentState = namedtuple(
    'EnvironmentState',
    ['elevator_state', 'time', 'persons_waiting']
)

def run_simulation(eventstream, elevator):
    next_elevator_event = slkdsggdf
    while True:
        # hva er neste ting som skjer?
        # gjor tilstandstransformasjon
        # spytt ut info
        # finn ut hva heisen vil gjore na
