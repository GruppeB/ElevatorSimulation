import unittest
from intellivator.elevator_environment import *
from intellivator.elevator_environment import _init_state

class NextState(unittest.TestCase):

    def setUp(self):
        self.params = EnvironmentParameters(
            number_of_elevators=2,
            elevator_capacity=10,
            number_of_floors=13,
            elevator_acceleration_duration=2,
            elevator_speed=1/3,
            door_duration=2,
            idle_time=float('inf')
        )
        env_state, elevators = _init_state(self.params)
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

    def test_close_door(self):
        state = self.env_state
        elevator_state = state.elevator_states[self.elevators[1]]
        state.elevator_states[self.elevators[1]] = elevator_state._replace(door_open = True)
        next_state(state, CloseDoorEvent(
            elevator = self.elevators[1],
            time = 40
        ))
        self.assertEqual(state.elevator_states[self.elevators[1]].door_open, False)

    def test_elevator_arrival(self):
        state = self.env_state
        elevator_state = state.elevator_states[self.elevators[1]]
        state.elevator_states[self.elevators[1]] = elevator_state._replace(direction = Direction.UP)
        next_state(state, ElevatorArrivalEvent(
            elevator = self.elevators[1],
            time = 50,
            arrival_floor = 10,
            start_position = 0,
            start_time = 11
        ))
        self.assertEqual(state.elevator_states[self.elevators[1]].position, 10)

    def test_open_door(self):
        state = self.env_state
        elevator_state = state.elevator_states[self.elevators[1]]
        state._replace_elevator_state(
            self.elevators[1],
            persons = elevator_state.persons + (
                Person(
                    arrival_time = 20,
                    destination_floor = 2
                ),
                Person(
                    arrival_time = 21,
                    destination_floor = 7
                )
            )
        )
        elevator_state = state.elevator_states[self.elevators[1]]
        state._replace_elevator_state(self.elevators[1], position = 2)
        next_state(state, OpenDoorEvent(
            elevator = self.elevators[1],
            time = 41
        ))
        self.assertEqual(state.elevator_states[self.elevators[1]].door_open, True)
        self.assertTrue(Person(arrival_time = 21, destination_floor = 7) in state.elevator_states[self.elevators[1]].persons)
        self.assertTrue(Person(arrival_time = 20, destination_floor = 2) not in state.elevator_states[self.elevators[1]].persons)
        self.assertEqual(state.statistics.served_persons, 1)
        self.assertEqual(state.statistics.total_service_time, 41-20)

    def test_load_elevator(self):
        state = self.env_state
        elevator_state = state.elevator_states[self.elevators[1]]
        state.elevator_states[self.elevators[1]] = elevator_state._replace(position = 2)
        person1 = WaitingPerson(
            Person(arrival_time = 90 , destination_floor = 6),
            arrival_floor = 2
            )
        person2 = WaitingPerson(
            Person(arrival_time = 91 , destination_floor = 6),
            arrival_floor = 3
            )
        person3 = WaitingPerson(
            Person(arrival_time = 92 , destination_floor = 8),
            arrival_floor = 2
            )
        state.waiting_persons.extend([person1, person2, person3])

        next_state(state, LoadElevatorEvent(
            elevator = self.elevators[1],
            time = 100,
            persons_to_load = [
                person1
            ]
        ))

        self.assertIn(person2, state.waiting_persons)
        self.assertIn(person3, state.waiting_persons)
        self.assertNotIn(person1, state.waiting_persons)
        self.assertIn(person1.person, state.elevator_states[self.elevators[1]].persons)
        self.assertNotIn(person2.person, state.elevator_states[self.elevators[1]].persons)
        self.assertNotIn(person3.person, state.elevator_states[self.elevators[1]].persons)

    def test_update_elevator_position(self):
        state = self.env_state
        state.time = 15

        state._replace_elevator_state(
            self.elevators[0],
            position = 2,
            direction = Direction.NONE
        )

        state._replace_elevator_state(
            self.elevators[1],
            position = 5.5,
            direction = Direction.DOWN
        )

        next_elevator_events = {self.elevators[0]: NoEvent, self.elevators[1]: ElevatorArrivalEvent(
            elevator = self.elevators[1],
            time = 22,
            arrival_floor = 2,
            start_position = 6,
            start_time = 10
        )}
        update_elevator_positions(state, self.params.elevator_speed, next_elevator_events)
        self.assertEqual(state.elevator_states[self.elevators[0]].position, 2)
        self.assertAlmostEqual(state.elevator_states[self.elevators[1]].position, 6-(5/3))

if __name__ == '__main__':
    unittest.main()
