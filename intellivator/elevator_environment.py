from collections import namedtuple
from recordclass import recordclass
from enum import IntEnum

EnvironmentParameters = namedtuple(
    'EnvironmentParameters',
    [
        'number_of_elevators',
        'number_of_floors',
        'elevator_acceleration_duration',
        'elevator_speed',
        'door_duration'
    ]
)

NoEvent = namedtuple('NoEvent', ['time'])(float('inf'))
NewPersonEvent = namedtuple('Event', ['time', 'arrival_floor', 'destination_floor'])
ElevatorArrivalEvent = namedtuple(
    'ElevatorArrivalEvent',
    [
        'elevator',
        'time',
        'arrival_floor',
        'start_position',
        'start_time'
    ]
)
OpenDoorEvent = namedtuple('OpenDoorEvent', ['elevator', 'time'])
CloseDoorEvent = namedtuple('CloseDoorEvent', ['elevator', 'time'])

class Direction(IntEnum):
    UP = 1
    NONE = 0
    DOWN = -1

Person = namedtuple('Person', ['arrival_time', 'destination_floor'])
WaitingPerson = namedtuple('WaitingPerson', ['person', 'arrival_floor'])
ElevatorState = recordclass(
    'ElevatorState',
    [
        'position',
        'direction',
        'persons',
        'door_open'
    ]
)
Statistics = recordclass(
    'Statistics',
    [
        'total_service_time',
        'total_waiting_time',
        'served_persons'
    ]
)
EnvironmentState = recordclass(
    'EnvironmentState',
    ['elevator_states', 'time', 'waiting_persons', 'statistics']
)

Elevator = namedtuple('Elevator', ['id'])

def _init_state(environment_parameters):

    elevators = [Elevator(i) for i in range(environment_parameters.number_of_elevators)]
    elevator_states = {
        elevator: ElevatorState(0, Direction.NONE, [], False)
        for elevator in elevators
    }

    stats = Statistics(
        total_service_time=0,
        total_waiting_time=0,
        served_persons=0
    )

    return EnvironmentState(elevator_states, 0, [], stats), elevators

def run_simulation(environment_parameters, person_stream, brain):

   environment_state, elevators = _init_state(environment_parameters)
   environment_stream = EnvironmentStream(person_stream, elevators)

   print(environment_state)
   print(elevators)



   # while environment_stream.has_next_event():
   #     next_event = environment_stream.get_next_event()
   #     environment_state = next_state(environment_state, next_event)
   #     next_action = brain.get_next_action(environment_state, next_event)
   #     environment_state = next_state(environment_state, next_action)

class EnvironmentStream():
    def __init__(self, person_stream, elevators):
        self.person_stream = person_stream
        self.elevator_streams = { e: ElevatorStream for e in elevators }

    def _get_earliest_stream(self):
        earliest_stream = self.person_stream
        for elevator_stream in self.elevator_streams.values():
            if elevator_stream.peek().time < earliest_stream.peek().time:
                earliest_stream = elevator_stream
        return earliest_stream

    def get_next_event(self):
        return self._get_earliest_stream().get_next()

    def has_next_event(self):
        return self._get_earliest_stream().peek() != NoEvent

    def add_elevator_event(self, elevator, event):
        self.elevator_streams[elevator].add_event(event)

    def flush_elevator_stream(self, elevator):
        self.elevator_stream.flush()


class ElevatorStream():
    def __init__():
        self.events = []

    def get_next(self):
        if not self.events:
            return NoEvent
        else:
            return self.events.pop(0)

    def peek(self):
        if not self.events:
            return NoEvent
        else:
            return self.events[0]

    def add_event(self, event):
        assert self.events or event.time > events[-1].time
        self.events.append(event)

    def flush(self):
        self.event = []

def next_state_new_person(env_state, event):
    new_person = Person(
        arrival_time=event.time,
        destination_floor=event.destination_floor
    )
    new_waiting_person = WaitingPerson(
        person=new_person,
        arrival_floor=event.arrival_floor
    )
    env_state.waiting_persons.append(new_waiting_person)

def next_state_open_door(env_state, event):
    elevator_state = env_state.elevator[event.elevator]
    current_floor = elevator_state.position
    finished_persons = [
        p for p in elevator_state.persons
        if p.destination_floor == current_floor
    ]

    assert elevator_state.open_door == False
    elevator_state.open_door = True
    for p in finished_persons:
        elevator_state.persons.remove(p)
        env_state.statistics.total_service_time += event.time - p.arrival_time
        served_persons += 1



def next_state(env_state, event):
    if type(event) == NewPersonEvent:
        next_state_new_person(env_state, event)
    elif type(event) == OpenDoorEvent:
        next_state_open_door(env_state, event)
