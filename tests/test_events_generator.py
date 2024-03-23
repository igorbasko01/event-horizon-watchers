import unittest

from events import SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent, \
    SecurityChallengePresentedEvent, SecurityChallengeAnsweredEvent, SecurityChallengeFailedEvent
from events_generator import RandomEventsGenerator, SequentialEventsGenerator


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

    def test_random_events_generator_generates_empty_list_if_times_negative(self):
        generator = RandomEventsGenerator({SignInStartedEvent, SecurityChallengePassedEvent}, 'uid', -1)
        events = list(generator.generate())
        self.assertEqual(0, len(events))
        self.assertEqual([], events)

    def test_sequential_events_generator_generates_list_of_events(self):
        generator = SequentialEventsGenerator(
            [SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent], 'uid')
        events = list(generator.generate())
        self.assertEqual(3, len(events))
        self.assertIsInstance(events[0], SignInStartedEvent)
        self.assertIsInstance(events[1], OneTimePasswordSentEvent)
        self.assertIsInstance(events[2], SecurityChallengePassedEvent)

    def test_sequential_events_generator_generates_empty_list(self):
        generator = SequentialEventsGenerator([], 'uid')
        events = list(generator.generate())
        self.assertEqual(0, len(events))
        self.assertEqual([], events)

    def test_sequential_events_generator_also_accepts_random_events_generator(self):
        uid = 'uid'
        generator = SequentialEventsGenerator([
            SignInStartedEvent,
            SecurityChallengePresentedEvent,
            SecurityChallengeAnsweredEvent,
            RandomEventsGenerator({SecurityChallengePassedEvent, SecurityChallengeFailedEvent}, uid, 1)
        ], uid)
        events = list(generator.generate())
        self.assertEqual(4, len(events))
        self.assertIsInstance(events[0], SignInStartedEvent)
        self.assertIsInstance(events[1], SecurityChallengePresentedEvent)
        self.assertIsInstance(events[2], SecurityChallengeAnsweredEvent)
        self.assertTrue(
            isinstance(events[3], SecurityChallengePassedEvent) or isinstance(events[3], SecurityChallengeFailedEvent))
