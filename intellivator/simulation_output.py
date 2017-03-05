class SimulationDump():
    def __init__(self, output_file, env_params):
        self.output_file = output_file
        self.env_params = env_params
        self.output_file.write('{} {}\n'.format(
            env_params.number_of_elevators,
            env_params.number_of_floors
        ))

    def env_state_has_changed(self, old_env_state, event, new_env_state):
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

    def close(self):
        self.output_file.close()


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
