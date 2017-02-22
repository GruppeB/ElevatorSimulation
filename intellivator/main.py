import elevator_environment

def main():
    params = elevator_environment.EnvironmentParameters(
        number_of_elevators=2,
        number_of_floors=13,
        elevator_acceleration_duration=2,
        elevator_speed=3,
        door_duration=2
    )
    elevator_environment.run_simulation(params, None, None)

main()
