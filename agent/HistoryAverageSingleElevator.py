from agent.HistorySingleElevator import HistorySingleElevator
from environment.elevator_environment import Action, Direction, NewPersonEvent

class HistoryAverageSingleElevator(HistorySingleElevator):
    def __init__(self, env_params):
        super(HistoryAverageSingleElevator, self).__init__(env_params)

    def _rest_floor_from_history(self, history, bucket):
        if history[bucket]:
            return int(sum(history[bucket]) / len(history[bucket]) + 0.5)
        else:
            return None
