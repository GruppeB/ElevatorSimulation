import unittest
from environment.PersonStream import PersonStream
from environment.elevator_environment import NewPersonEvent, NoEvent
from io import StringIO

class PersonStreamTest(unittest.TestCase):

    def setUp(self):
        lines = [
            '0\t1\t3',
            '123.4\t1\t2',
            '234.5\t4\t2'
        ]
        self.events = [
            NewPersonEvent(
                time = 0,
                arrival_floor = 0,
                destination_floor = 2
            ),
            NewPersonEvent(
                time = 123.4,
                arrival_floor = 0,
                destination_floor = 1
            ),
            NewPersonEvent(
                time = 234.5,
                arrival_floor = 3,
                destination_floor = 1
            )
        ]
        self.person_file = StringIO('\n'.join(lines))

    def test_peek_first(self):
        person_stream = PersonStream(self.person_file)
        self.assertEqual(person_stream.peek(), self.events[0])
        self.assertEqual(person_stream.peek(), self.events[0])
        self.assertEqual(person_stream.get_next(), self.events[0])
        self.assertEqual(person_stream.peek(), self.events[1])
        self.assertEqual(person_stream.peek(), self.events[1])
        self.assertEqual(person_stream.get_next(), self.events[1])

    def test_get_first(self):
        person_stream = PersonStream(self.person_file)
        self.assertEqual(person_stream.get_next(), self.events[0])
        self.assertEqual(person_stream.peek(), self.events[1])
        self.assertEqual(person_stream.peek(), self.events[1])
        self.assertEqual(person_stream.get_next(), self.events[1])
        self.assertEqual(person_stream.peek(), self.events[2])
        self.assertEqual(person_stream.peek(), self.events[2])

    def test_empty(self):
        person_stream = PersonStream(self.person_file)
        for event in self.events:
            self.assertEqual(person_stream.peek(), event)
            self.assertEqual(person_stream.peek(), event)
            self.assertEqual(person_stream.get_next(), event)

        self.assertEqual(person_stream.peek(), NoEvent)
        self.assertEqual(person_stream.peek(), NoEvent)
        self.assertEqual(person_stream.get_next(), NoEvent)
        self.assertEqual(person_stream.get_next(), NoEvent)
        self.assertEqual(person_stream.peek(), NoEvent)
