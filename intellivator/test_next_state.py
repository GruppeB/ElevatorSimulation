import unittest
from intellivator.elevator_environment import *
from intellivator.elevator_environment import _init_state

class NextState(unittest.TestCase):

    def setUp(self):
        params = EnvironmentParameters(
            number_of_elevators=2,
            number_of_floors=13,
            elevator_acceleration_duration=2,
            elevator_speed=3,
            door_duration=2
        )
        env_state, elevators = _init_state(params)
        self.env_state = env_state
        self.elevators = elevators

    def test_new_person(self):
        state = self.env_state
        next_state(state, NewPersonEvent(
            time=32,
            arrival_floor=2,
            destination_floor=10
        ))
        self.assertEqual(len(state.waiting_persons), 1)
        self.assertEqual(state.waiting_persons[0], WaitingPerson(
            Person(arrival_time=32, destination_floor=10), arrival_floor=2
        ))

    # def test_elevator_arrival(self):
    #     state = self.env_state
    #     state = next_state(state, ElevatorArrivalEvent(
    #         elevator=self.elevators[1],
    #         time=765,
    #         floor=11
    #     ))
    #     self.assertEqual(
    #         state.elevator_states[self.elevators[1]].position, 11
    #     )
    #     self.assertEqual(
    #         state.elevator_states[self.elevators[1]].direction, Direction.NONE
    #     )

    # def test_door_open(self):
    #     state = self.env_state
    #     state.elevator_states.persons.append(Person(
    #         arrival_time=10,
    #         destination_floor=6
    #     ))

if __name__ == '__main__':
    unittest.main()
