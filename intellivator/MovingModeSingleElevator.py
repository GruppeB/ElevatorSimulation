from intellivator.elevator_environment import Action, Direction, NewPersonEvent

class MovingModeSingleElevator():
    def __init__(self, env_params):
        assert env_params.number_of_elevators == 1
        self.capacity = env_params.elevator_capacity
        self.mode = Direction.UP
        self.last_arrivals = []

    def init(self, env_state):
        self.elevator = list(env_state.elevator_states.keys())[0]

    def _should_be_loaded(self, elevator_position, waiting_persons):
        return elevator_position == waiting_persons.arrival_floor

    def _should_be_picked_up(self, elevator_position, waiting_person):
            delta_pos = waiting_person.arrival_floor - elevator_position
            return delta_pos * self.mode > 0

    def get_next_actions(self, env_state, event):
        elevator_state = env_state.elevator_states[self.elevator]
        position = elevator_state.position
        persons = elevator_state.persons

        if type(event) is NewPersonEvent:
            self.last_arrivals.append(event.arrival_floor)
            while len(self.last_arrivals) > 15:
                self.last_arrivals.pop(0)

        if not env_state.waiting_persons and not elevator_state.persons:
            rest_floor = int(sum(self.last_arrivals) / 15 + 0.5)
            max(set(self.last_arrivals), key=self.last_arrivals.count)
            if position == rest_floor:
                return []
            else:
                return [Action(
                    elevator = self.elevator,
                    persons_to_load = [],
                    destination = rest_floor
                )]

        if elevator_state.direction != Direction.NONE:
            return []

        persons_to_pick_up = [
            wp for wp in env_state.waiting_persons
            if self._should_be_picked_up(position, wp)
            and not self._should_be_loaded(position, wp)
        ]
        persons_to_pick_up.sort(key=lambda wp: self.mode * wp.arrival_floor)

        persons_to_load = [
            wp for wp in env_state.waiting_persons
            if self._should_be_loaded(position, wp)
        ]
        persons_to_load.sort(key=lambda wp: wp.person.arrival_time)

        free_capacity = self.capacity - len(elevator_state.persons)
        persons_to_load = persons_to_load[:free_capacity]
        free_capacity -= len(persons_to_load)
        persons_to_pick_up = persons_to_pick_up[:free_capacity]

        if not persons_to_load and not persons_to_pick_up and not persons:
            if env_state.waiting_persons:
                self.mode = Direction.UP if self.mode == Direction.DOWN else Direction.DOWN
                return self.get_next_actions(env_state, event)
            else:
                return []

        plan = [p.destination_floor for p in elevator_state.persons]
        plan.extend([wp.arrival_floor for wp in persons_to_pick_up])
        plan.extend([wp.person.destination_floor for wp in persons_to_load])
        plan.sort(key=lambda f: self.mode * f)

        if plan[0] == position:
            return []

        return [
            Action(
                elevator = self.elevator,
                persons_to_load = persons_to_load,
                destination = plan[0]
            )
        ]
