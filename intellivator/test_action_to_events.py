import unittest
from intellivator.elevator_environment import *
from intellivator.elevator_environment import _init_state


class ActionToEvents(unittest.TestCase):

    def setUp(self):
        self.params = EnvironmentParameters(
            number_of_elevators=2,
            number_of_floors=13,
            elevator_acceleration_duration=2,
            elevator_speed=1/3,
            door_duration=2,
            idle_time=float('inf')
        )
        env_state, elevators = _init_state(self.params)

        env_state.elevator_states[elevators[1]].position = 6

        self.person1 = WaitingPerson(
            Person(arrival_time = 90 , destination_floor = 9),
            arrival_floor = 6
            )
        self.person2 = WaitingPerson(
            Person(arrival_time = 91 , destination_floor = 6),
            arrival_floor = 3
            )
        self.person3 = WaitingPerson(
            Person(arrival_time = 92 , destination_floor = 8),
            arrival_floor = 2
            )
        env_state.waiting_persons.extend([self.person1, self.person2, self.person3])

        self.env_state = env_state
        self.elevators = elevators



    def test_action_to_event_direction_up(self):
        elevator = self.elevators[1]
        elevator_state = self.env_state.elevator_states[elevator]
        elevator_state.direction = Direction.UP
        elevator_stream_update =  action_to_events(
            Action(
                elevator = elevator,
                persons_to_load = [],
                destination = 9
            ),
            self.env_state,
            self.params
        )

        self.assertEqual(elevator, elevator_stream_update.elevator)
        event_list = elevator_stream_update.events

        current_time = self.env_state.time

        start_time = current_time
        departure_event = event_list[0]
        self.assertEqual(
            departure_event,
            ElevatorDepartureEvent(
                elevator = elevator,
                time = start_time,
                direction = Direction.UP
            )
        )


        current_time = start_time + (9-6) / self.params.elevator_speed
        arrival_event = event_list[1]
        self.assertEqual(
            arrival_event,
            ElevatorArrivalEvent(
                elevator = elevator,
                time = current_time,
                arrival_floor = 9,
                start_position = 6,
                start_time = start_time
            )
        )

        current_time += self.params.elevator_acceleration_duration + self.params.door_duration
        open_event2 = event_list[2]
        self.assertEqual(
            open_event2,
            OpenDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )

        current_time += self.params.door_duration
        close_event2 = event_list[3]
        self.assertEqual(
            close_event2,
            CloseDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )

    def test_action_to_event_direction_down(self):
        elevator = self.elevators[1]
        elevator_state = self.env_state.elevator_states[elevator]
        elevator_state.direction = Direction.DOWN
        elevator_stream_update =  action_to_events(
            Action(
                elevator = elevator,
                persons_to_load = [],
                destination = 9
            ),
            self.env_state,
            self.params
        )

        self.assertEqual(elevator, elevator_stream_update.elevator)
        event_list = elevator_stream_update.events

        current_time = self.env_state.time

        departure_event = event_list[0]
        start_time = current_time + 2 * self.params.elevator_acceleration_duration
        self.assertEqual(
            departure_event,
            ElevatorDepartureEvent(
                elevator = elevator,
                time = start_time,
                direction = Direction.UP
            )
        )

        current_time = start_time + (9-6) / self.params.elevator_speed
        arrival_event = event_list[1]
        self.assertEqual(
            arrival_event,
            ElevatorArrivalEvent(
                elevator = elevator,
                time = current_time,
                arrival_floor = 9,
                start_position = 6,
                start_time = start_time
            )
        )

        current_time += self.params.elevator_acceleration_duration + self.params.door_duration
        open_event2 = event_list[2]
        self.assertEqual(
            open_event2,
            OpenDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )

        current_time += self.params.door_duration
        close_event2 = event_list[3]
        self.assertEqual(
            close_event2,
            CloseDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )
    def test_action_to_event_direction_none(self):
        elevator = self.elevators[1]
        elevator_state = self.env_state.elevator_states[elevator]
        elevator_state.direction = Direction.NONE
        elevator_stream_update =  action_to_events(
            Action(
                elevator = elevator,
                persons_to_load = [self.person1],
                destination = 9
            ),
            self.env_state,
            self.params
        )

        self.assertEqual(elevator, elevator_stream_update.elevator)
        event_list = elevator_stream_update.events

        current_time = self.env_state.time

        load_event = event_list[0]
        self.assertEqual(
            load_event,
            LoadElevatorEvent(
                elevator = elevator,
                time = current_time,
                persons_to_load = [self.person1]
            )
        )

        current_time += self.params.door_duration
        open_event1 = event_list[1]
        self.assertEqual(
            open_event1,
            OpenDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )

        current_time += self.params.door_duration
        close_event1 = event_list[2]
        self.assertEqual(
            close_event1,
            CloseDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )


        start_time = current_time + self.params.elevator_acceleration_duration

        departure_event = event_list[3]
        self.assertEqual(
            departure_event,
            ElevatorDepartureEvent(
                elevator = elevator,
                time = start_time,
                direction = Direction.UP
            )
        )
        current_time = start_time + (9-6) / self.params.elevator_speed
        arrival_event = event_list[4]
        self.assertEqual(
            arrival_event,
            ElevatorArrivalEvent(
                elevator = elevator,
                time = current_time,
                arrival_floor = 9,
                start_position = 6,
                start_time = start_time
            )
        )

        current_time += self.params.elevator_acceleration_duration + self.params.door_duration
        open_event2 = event_list[5]
        self.assertEqual(
            open_event2,
            OpenDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )

        current_time += self.params.door_duration
        close_event2 = event_list[6]
        self.assertEqual(
            close_event2,
            CloseDoorEvent(
                elevator = elevator,
                time = current_time
            )
        )




if __name__ == '__main__':
    unittest.main()
