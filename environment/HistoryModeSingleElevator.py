from environment.HistorySingleElevator import HistorySingleElevator
from environment.elevator_environment import Action, Direction, NewPersonEvent

class HistoryModeSingleElevator(HistorySingleElevator):
    def __init__(self, env_params):
        super(HistoryModeSingleElevator, self).__init__(env_params)

    def _rest_floor_from_history(self, history, bucket):
        if history[bucket]:
            return max(set(history[bucket]), key=history[bucket].count)
        else:
            return None
