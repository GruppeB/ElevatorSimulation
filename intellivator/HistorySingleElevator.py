from intellivator.SimpleSingleElevator import SimpleSingleElevator
from intellivator.elevator_environment import Action, Direction, NewPersonEvent

class HistorySingleElevator(SimpleSingleElevator):
    def __init__(self, env_params):
        super(HistorySingleElevator, self).__init__(env_params)
        self._bucket_size = 5 * 60 # 5 min
        self._number_of_buckets = (60 * 60 * 24 * 7) // self._bucket_size
        self._history = [[] for i in range(self._number_of_buckets)]

    def _rest_floor_from_history(self, history, bucket):
        return None

    def _get_rest_floor(self, env_state, event):
        mod = self._number_of_buckets * self._bucket_size
        bucket = int((event.time % mod) // self._number_of_buckets)

        if type(event) is NewPersonEvent:
            self._history[bucket].append(event.arrival_floor)

        return self._rest_floor_from_history(self._history, bucket)
