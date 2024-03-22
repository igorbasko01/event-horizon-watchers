import unittest
from unittest.mock import Mock, call

from events_generator import EventsGenerator
from file_writer import EventsFileWriter


class MockEvent:
    def to_json(self):
        return '{"event": "test_event"}'


class MockEventsGenerator(EventsGenerator):
    def generate(self):
        return [MockEvent() for _ in range(3)]


class EventsFileWriterTests(unittest.TestCase):
    def test_write(self):
        mock_generator = MockEventsGenerator()
        mock_file = Mock()

        EventsFileWriter.write(mock_generator, mock_file)

        self.assertEqual(3, mock_file.write.call_count)
        expected_calls = [call('{"event": "test_event"}\n')] * 3
        mock_file.write.assert_has_calls(expected_calls, any_order=True)

