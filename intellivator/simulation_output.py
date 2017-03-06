from math import log10, ceil

from intellivator.elevator_environment import SimulationListener
from intellivator.elevator_environment import NewPersonEvent



class StateDump(SimulationListener):
    def __init__(self, output_file, env_params):
        self.output_file = output_file
        self.env_params = env_params
        self.output_file.write('{} {}\n'.format(
            env_params.number_of_elevators,
            env_params.number_of_floors
        ))

    def env_state_has_changed(self, env_state_change):
        new_env_state = env_state_change.new_env_state

        self.output_file.write(str(new_env_state.time))

        for elevator, elevator_state in new_env_state.elevator_states.items():
            self.output_file.write(' {}'.format(elevator_state.position))

        for elevator, elevator_state in new_env_state.elevator_states.items():
            self.output_file.write(' {}'.format(len(elevator_state.persons)))

        for f in range(self.env_params.number_of_floors):
            number_of_waiting_persons = len([
                wp for wp in new_env_state.waiting_persons
                if wp.arrival_floor == f
            ])
            self.output_file.write(' {}'.format(number_of_waiting_persons))

        self.output_file.write('\n')

    def done(self):
        self.output_file.close()


class ProgressOutput(SimulationListener):
    def __init__(self, arrivals_file, output_file):
        self.number_of_arrivals = sum(1 for _ in arrivals_file)
        arrivals_file.seek(0)
        self.output_file = output_file
        self.arrivals_count = 0
        self._update()

    def env_state_has_changed(self, env_state_change):
        if type(env_state_change.event) is NewPersonEvent:
            self.arrivals_count += 1
        self._update()

    def _update(self):
        width = int(max(1, ceil(log10(self.number_of_arrivals))))
        self.output_file.write('\rProgress: {} / {}'.format(
            str(self.arrivals_count).rjust(width), self.number_of_arrivals
        ))

    def done(self):
        self.output_file.write('\n')


class StateChangeStatistic(SimulationListener):
    def __init__(self, start_value, map_reduce):
        self._value = start_value
        self._map_reduce = map_reduce

    def env_state_has_changed(self, env_state_change):
        self._value = map_reduce(self._value, env_state_change)

    def result(self):
        return self._value

class StateChangeTimeSeries(SimulationListener):
    def __init__(self, column_names, state_change_to_data_point, data_file):
        self._state_change_to_data_point = state_change_to_data_point
        self._data_file = data_file

        column_names = ('Time',) + column_names
        self._data_file.write('\t'.join(map(lambda s: '"{}"'.format(s), column_names)) + '\n')

    def env_state_has_changed(self, env_state_change):
        data_point = self._state_change_to_data_point(env_state_change)
        data_point = (env_state_change.new_env_state.time,) + data_point
        self._data_file.write('\t'.join(map(str, data_point)) + '\n')

    def done(self):
        self._data_file.close()


def number_of_persons_waiting(env_state_change):
    return (len(env_state_change.new_env_state.waiting_persons),)


def write_summary(duration, statistics, output_file):
    output_file.write('Simulation duration:  {:.2f}\n'.format(duration))
    output_file.write('Served persons:       {}\n'.format(statistics.served_persons))
    output_file.write('Average waiting time: {:.2f}\n'.format(
        statistics.total_waiting_time / statistics.served_persons)
    )
    output_file.write('Total waiting time:   {:.2f}\n'.format(statistics.total_waiting_time))
    output_file.write('Average service time: {:.2f}\n'.format(
        statistics.total_service_time / statistics.served_persons)
    )
    output_file.write('Total service time:   {:.2f}\n'.format(statistics.total_service_time))
