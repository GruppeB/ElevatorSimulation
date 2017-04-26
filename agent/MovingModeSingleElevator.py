from agent.SimpleSingleElevator import SimpleSingleElevator
from environment.elevator_environment import Action, Direction, NewPersonEvent

class MovingModeSingleElevator(SimpleSingleElevator):
    def __init__(self, env_params):
        super(MovingModeSingleElevator, self).__init__(env_params)
        self.last_arrivals = []

    def _get_rest_floor(self, env_state, event):
        if type(event) is NewPersonEvent:
            self.last_arrivals.append(event.arrival_floor)
            while len(self.last_arrivals) > 15:
                self.last_arrivals.pop(0)

        return max(set(self.last_arrivals), key=self.last_arrivals.count)
