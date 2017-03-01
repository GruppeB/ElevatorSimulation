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
LoadElevatorEvent = namedtuple('LoadElevatorEvent', ['elevator', 'time', 'persons_to_load'])
ElevatorDepartureEvent = namedtuple('ElevatorDepartureEvent', ['elevator', 'time', 'direction'])

Action = namedtuple('Action', ['elevator', 'time', 'persons_to_load', 'destination'])
ElevatorStreamUpdate = namedtuple('ElevatorStreamUpdate', ['elevator', 'events'])


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
    #    next_action = brain.get_next_action(environment_state, next_event)
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

    def peek_elevator_stream(self, elevator):
        return self.elevator_streams[elevator].peek()

    def update_elevator_stream(self, elevator_stream_update):
        elevator = elevator_stream_update.elevator
        events = elevator_stream_update.events
        self.flush_elevator_stream(elevator)
        for event in events:
            self.add_elevator_event(elevator, event)


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
    elevator_state = env_state.elevator_states[event.elevator]
    current_floor = elevator_state.position
    finished_persons = [
        p for p in elevator_state.persons
        if p.destination_floor == current_floor
    ]

    assert elevator_state.door_open == False
    assert elevator_state.direction == Direction.NONE
    elevator_state.door_open = True
    for p in finished_persons:
        elevator_state.persons.remove(p)
        env_state.statistics.total_service_time += event.time - p.arrival_time
        env_state.statistics.served_persons += 1

def next_state_close_door(env_state, event):
    elevator_state = env_state.elevator_states[event.elevator]
    current_floor = elevator_state.position
    assert elevator_state.door_open == True
    assert elevator_state.direction == Direction.NONE
    elevator_state.door_open = False

def next_state_elevator_arrival(env_state, event):
    elevator_state = env_state.elevator_states[event.elevator]
    assert elevator_state.position != event.arrival_floor
    elevator_state.position = event.arrival_floor
    elevator_state.direction = Direction.NONE


def next_state_load_elevator(env_state, event):
    elevator_state = env_state.elevator_states[event.elevator]
    assert elevator_state.direction == Direction.NONE
    for p in event.persons_to_load:
        assert p.arrival_floor == elevator_state.position
        elevator_state.persons.append(p.person)
        env_state.waiting_persons.remove(p)

def next_state_elevator_departure(env_state, event):
    elevator_state = env_state.elevator[event.elevator]
    elevator_state.direction = event.direction

def next_state(env_state, event):
    if type(event) == NewPersonEvent:
        next_state_new_person(env_state, event)
    elif type(event) == OpenDoorEvent:
        next_state_open_door(env_state, event)
    elif type(event) == CloseDoorEvent:
        next_state_close_door(env_state, event)
    elif type(event) == ElevatorArrivalEvent:
        next_state_elevator_arrival(env_state, event)
    elif type(event) == LoadElevatorEvent:
        next_state_load_elevator(env_state, event)
    else:
        raise Exception("No such event!")

def update_elevator_position(env_state, elevator_speed, next_elevator_events):
    for elevator, elevator_state in env_state.elevator_states.items():
        next_event = next_elevator_events[elevator]
        if type(next_event) is ElevatorArrivalEvent:
            travel_time = env_state.time - next_event.start_time
            travel_distance = travel_time * elevator_speed
            direction = elevator_state.direction
            assert direction*(next_event.arrival_floor - next_event.start_position) > 0
            elevator_state.position = next_event.start_position + travel_distance * direction

def get_direction(from_pos, to_pos):
    if to_pos - from_pos > 0:
        return Direction.UP
    elif to_pos - from_pos < 0:
        return Direction.DOWN
    else:
        return Direction.NONE


def action_to_events(action, env_state, parameters):
    elevator = action.elevator
    elevator_state = env_state.elevators[elevator]
    current_time = env_state.time
    eventlist = []
    if elevator_state.direction == Direction.NONE:
        eventlist.append(
            LoadElevatorEvent(
                elevator = elevator,
                time = current_time,
                persons_to_load = action.persons_to_load
            )
        )
        if not env_state.elevator_states[elevator].door_open:
            current_time += parameters.door_duration
            eventlist.append(
                OpenDoorEvent(
                    elevator = elevator,
                    time = current_time
                )
            )
        current_time += parameters.door_duration
        eventlist.append(
            CloseDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )
    else:
        assert not action.persons_to_load

    start_time = current_time
    new_direction = get_direction(elevator_state.position, action.destination)
    if elevator_state.direction == Direction.NONE:
        start_time += parameters.elevator_acceleration_duration
    elif elevator_state.direnction != new_direction:
        start_time += parameters.elevator_acceleration_duration * 2

    current_time = start_time + abs(elevator_state.position - action.destination) / parameters.elevator_speed
    eventlist.append(
        ElevatorArrivalEvent(
            elevator = elevator,
            time = current_time,
            arrival_floor = action.destination,
            start_position = elevator_state.position,
            start_time = start_time
        )
    )
    current_time += parameters.elevator_acceleration_duration + parameters.door_duration
    eventlist.append(
        OpenDoorEvent(
            elevator = elevator,
            time = current_time
        )
    )
    current_time += parameters.door_duration
    eventlist.append(
        CloseDoorEvent(
            elevator = elevator,
            time = current_time
        )
    )
    return ElevatorStreamUpdate(
        elevator = elevator,
        events = eventlist
    )
