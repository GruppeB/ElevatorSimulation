import unittest
from unittest.mock import Mock
from intellivator.elevator_environment import *
from intellivator.elevator_environment import _init_state

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
            number_of_floors=13,
            elevator_acceleration_duration=1,
            elevator_speed=1/3,
            door_duration=2,
            idle_time=float('inf')
        )

    def test_single_customer(self):
        class Brain():
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

        brain = Brain()
        brain.get_next_actions = Mock(side_effect=brain.get_next_actions)
        person_stream = PersonStreamStub([
            NewPersonEvent(
                time = 10,
                arrival_floor = 2,
                destination_floor = 5
            )
        ])

        time, statistics = run_simulation(self.params, person_stream, brain)
        self.assertEqual(time, 37)
        self.assertEqual(statistics.total_service_time, 25)
        self.assertEqual(statistics.total_waiting_time, 10)
        self.assertEqual(statistics.served_persons, 1)



if __name__ == '__main__':
    unittest.main()
