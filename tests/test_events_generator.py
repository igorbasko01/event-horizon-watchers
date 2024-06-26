import unittest

from events import SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent, \
    SecurityChallengePresentedEvent, SecurityChallengeAnsweredEvent, SecurityChallengeFailedEvent
from events_generator import RandomEventsGenerator, SequentialEventsGenerator, MultipleUsersEventsGenerator
from time_generator import TimeGenerator


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

    def test_random_events_generator_generates_different_times(self):
        generator = RandomEventsGenerator({SignInStartedEvent}, 'uid', 5)
        events = list(generator.generate())
        self.assertEqual(5, len(events))
        self.assertEqual(events[0].time, events[1].time - 1)
        self.assertEqual(events[1].time, events[2].time - 1)
        self.assertEqual(events[2].time, events[3].time - 1)
        self.assertEqual(events[3].time, events[4].time - 1)

    def test_random_events_generator_generates_different_times2(self):
        time_generator = TimeGenerator(1, increment=2)
        generator = RandomEventsGenerator({SignInStartedEvent}, 'uid', 5, time_generator)
        events = list(generator.generate())
        self.assertEqual(5, len(events))
        self.assertEqual(events[0].time, events[1].time - 2)
        self.assertEqual(events[1].time, events[2].time - 2)
        self.assertEqual(events[2].time, events[3].time - 2)
        self.assertEqual(events[3].time, events[4].time - 2)

    def test_sequential_events_generator_generates_different_times(self):
        generator = SequentialEventsGenerator(
            [SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent], 'uid')
        events = list(generator.generate())
        self.assertEqual(3, len(events))
        self.assertEqual(events[0].time, events[1].time - 1)
        self.assertEqual(events[1].time, events[2].time - 1)

    def test_sequential_events_generator_generates_different_times2(self):
        time_generator = TimeGenerator(1, increment=2)
        generator = SequentialEventsGenerator(
            [SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent], 'uid', time_generator)
        events = list(generator.generate())
        self.assertEqual(3, len(events))
        self.assertEqual(events[0].time, events[1].time - 2)
        self.assertEqual(events[1].time, events[2].time - 2)

    def test_multiple_users_events_generator(self):
        seq_events_generator = SequentialEventsGenerator([
            SignInStartedEvent,
            SecurityChallengePresentedEvent,
            SecurityChallengeAnsweredEvent,
            RandomEventsGenerator({SecurityChallengePassedEvent, SecurityChallengeFailedEvent})
        ])
        generator = MultipleUsersEventsGenerator(seq_events_generator, 3)
        events = list(generator.generate())
        unique_user_ids = {event.user_id for event in events}
        self.assertEqual(12, len(events))
        self.assertEqual(3, len(unique_user_ids))
