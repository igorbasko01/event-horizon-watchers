import unittest

from events import SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent
from events_generator import RandomEventsGenerator


class EventsGeneratorTests(unittest.TestCase):
    def test_random_events_generator_generates_one_event(self):
        generator = RandomEventsGenerator({SignInStartedEvent}, 'uid', 1)
        events = list(generator.generate())
        self.assertEqual(1, len(events))
        self.assertEqual('uid', events[0].user_id)

    def test_random_events_generator_generates_multiple_events(self):
        generator = RandomEventsGenerator({SignInStartedEvent}, 'uid', 5)
        events = list(generator.generate())
        self.assertEqual(5, len(events))
        self.assertEqual('uid', events[0].user_id)

    def test_random_events_generator_generates_different_events(self):
        generator = RandomEventsGenerator({SignInStartedEvent, OneTimePasswordSentEvent}, 'uid', 5)
        events = list(generator.generate())
        self.assertEqual(5, len(events))
        self.assertEqual('uid', events[0].user_id)

    def test_random_events_generator_generates_empty_list(self):
        generator = RandomEventsGenerator({SignInStartedEvent, SecurityChallengePassedEvent}, 'uid', 0)
        events = list(generator.generate())
        self.assertEqual(0, len(events))
        self.assertEqual([], events)

