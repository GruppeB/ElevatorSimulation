from intellivator.elevator_environment import *
from intellivator.PersonStream import PersonStream
from intellivator.SimpleSingleElevator import SimpleSingleElevator

def main():
    params = EnvironmentParameters(
        number_of_elevators=1,
        elevator_capacity=10,
        number_of_floors=13,
        elevator_acceleration_duration=2,
        elevator_speed=3,
        door_duration=2,
        idle_time = float('inf')
    )

    personstream =  PersonStream(open("test.txt","r"))
    brain = SimpleSingleElevator(params)

    duration, statistics = run_simulation(params, personstream, brain)
    print(statistics)
    print(statistics.total_service_time / statistics.served_persons)
