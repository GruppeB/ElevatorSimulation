from environment.elevator_environment import NewPersonEvent, NoEvent


class PersonStream():
    def __init__(self, person_file):
        self.person_file = person_file
        self.next_event = NoEvent
        self._read_next_event()

    def _read_next_event(self):
        line = self.person_file.readline()
        if line:
            time, arrival_floor, destination_floor = line.split('\t')
            time = float(time)
            arrival_floor = int(arrival_floor) - 1
            destination_floor = int(destination_floor) - 1
            self.next_event = NewPersonEvent(
                time,
                arrival_floor,
                destination_floor
            )
        else:
            self.next_event = NoEvent

    def get_next(self):
        event = self.next_event
        self._read_next_event()
        return event

    def peek(self):
        return self.next_event
