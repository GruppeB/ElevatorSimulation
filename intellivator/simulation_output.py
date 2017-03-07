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


class SimulationStatistic(SimulationListener):
    def __init__(
            self,
            name,
            start_value,
            state_changed = lambda v, *x: v,
            person_finished = lambda v, *x: v,
            person_picked_up = lambda v, *x: v,
            result = lambda v: v
    ):
        self.name = name
        self._value = start_value
        self._state_changed = state_changed
        self._person_finished = person_finished
        self._person_picked_up = person_picked_up
        self._result = result

    def env_state_has_changed(self, env_state_change):
        self._value = self._state_changed(self._value, env_state_change)

    def person_finished(self, time, person, elevator):
        self._value = self._person_finished(self._value, time, person, elevator)

    def person_picked_up(self, time, waiting_person, elevator):
        self._value = self._person_picked_up(self._value, time, waiting_person, elevator)

    def result(self):
        return self._result(self._value)

class SimulationTimeSeries(SimulationListener):
    def __init__(
            self,
            column_names,
            data_file,
            state_changed = None,
            person_finished = None,
            person_picked_up = None
    ):
        self._state_changed = state_changed
        self._person_finished = person_finished
        self._person_picked_up = person_picked_up
        self._data_file = data_file

        column_names = ('Time',) + column_names
        self._data_file.write('\t'.join(map(lambda s: '"{}"'.format(s), column_names)) + '\n')

    def env_state_has_changed(self, env_state_change):
        if self._state_changed:
            data_point = self._state_changed(env_state_change)
            data_point = (env_state_change.new_env_state.time,) + data_point
            self._data_file.write('\t'.join(map(str, data_point)) + '\n')

    def person_finished(self, time, person, elevator):
        if self._person_finished:
            data_point = self._person_finished(time, person, elevator)
            data_point = (time,) + data_point
            self._data_file.write('\t'.join(map(str, data_point)) + '\n')

    def person_picked_up(self, time, waiting_person, elevator):
        if self._person_picked_up:
            data_point = self._person_picked_up(time, waiting_person, elevator)
            data_point = (time,) + data_point
            self._data_file.write('\t'.join(map(str, data_point)) + '\n')

    def done(self):
        self._data_file.close()


def write_summary(duration, statistics, output_file):
    output_file.write('{:<25s} {:.2f}\n'.format('Simulation duration:', duration))
    for statistic in statistics:
        print('{:<25s} {:.2f}'.format(statistic.name + ':', statistic.result()))
