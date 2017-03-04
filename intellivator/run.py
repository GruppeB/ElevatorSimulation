from intellivator.elevator_environment import *
from intellivator.PersonStream import PersonStream

class NoBrain():

    def init(self, env_state):
        pass

    def get_next_actions(self, env_state, next_event):
        elevators = list(env_state.elevator_states.keys())
        actions = [
            Action(elevators[0], [], (env_state.elevator_states[elevators[0]].position + 1) % 13)
            # Action(elevators[1], [], (env_state.elevator_states[elevators[1]].position + 1) % 13)
        ]

        return actions

def main():
    params = EnvironmentParameters(
        number_of_elevators=2,
        number_of_floors=13,
        elevator_acceleration_duration=2,
        elevator_speed=3,
        door_duration=2,
        idle_time = float('inf')
    )

    personstream =  PersonStream(open("test.txt","r"))
    brain = NoBrain()

    run_simulation(params, personstream, brain)

main()
