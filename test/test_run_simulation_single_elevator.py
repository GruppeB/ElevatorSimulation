import unittest
from unittest.mock import Mock
from environment.elevator_environment import *
from environment.elevator_environment import _init_state

class PersonStreamStub():
    def __init__(self, person_events):
        self.person_events = person_events

    def peek(self):
        if self.person_events:
            return self.person_events[0]
        else:
            return NoEvent

    def get_next(self):
        if self.person_events:
            return self.person_events.pop(0)
        else:
            return NoEvent

class RunSimulationSingleElevator(unittest.TestCase):

    def setUp(self):
        self.params = EnvironmentParameters(
            number_of_elevators=1,
            elevator_capacity=10,
            number_of_floors=13,
            elevator_acceleration_duration=1,
            elevator_speed=1/3,
            door_duration=2,
            idle_time=60
        )

    def test_single_customer(self):
        '''
        0: Intialize
        60: TimePassedEvent
        100: NewPersonEvent - floor 2
        101: ElevatorDepartureEvent - from floor 0
        107: ElevatorArrivalEvent - to floor 0
        110: OpenDoorEvent
        110: LoadElevatorEvent
        112: CloseDoorEvent
        113: ElevatorDepartureEvent - from floor 2
        122: ElevatorArrivalEvent - to floor 5
        125: OpenDoorEvent
        127: CloseDoorEvent
        '''
        class Agent():
            def init(self, env_state):
                self.elevator = list(env_state.elevator_states.keys())[0]

            def get_next_actions(self, env_state, event):
                if type(event) is NewPersonEvent:
                    return [
                        Action(
                            elevator=self.elevator,
                            persons_to_load=tuple(),
                            destination=2
                        )
                    ]
                elif type(event) is OpenDoorEvent and env_state.waiting_persons:
                    return [
                        Action(
                            elevator=self.elevator,
                            persons_to_load=tuple(env_state.waiting_persons),
                            destination=5
                        )
                    ]
                else:
                    return []

        agent = Agent()
        agent.get_next_actions = Mock(side_effect=agent.get_next_actions)
        person_stream = PersonStreamStub([
            NewPersonEvent(
                time = 100,
                arrival_floor = 2,
                destination_floor = 5
            )
        ])

        simulation_listener = Mock()
        simulation_listener.env_state_has_changed = Mock()

        time = run_simulation(
            self.params,
            person_stream,
            agent,
            [simulation_listener]
        )
        self.assertEqual(time, 127)

        self.assertEqual(agent.get_next_actions.call_count, 3)
        self.assertEqual(simulation_listener.env_state_has_changed.call_count, 12)



if __name__ == '__main__':
    unittest.main()
