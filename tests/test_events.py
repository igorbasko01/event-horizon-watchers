import unittest

from events import Event, SignInStartedEvent, OneTimePasswordSentEvent, DeliveryMethod


class EventTests(unittest.TestCase):

    def test_event_creation(self):
        event = Event(1)
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)

    def test_event_to_json(self):
        event = Event(1)
        self.assertEqual('{"time": 1}', event.to_json())

    def test_sign_in_started_event_creation(self):
        event = SignInStartedEvent(1, 'ggg')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('ggg', event.user_id)

    def test_sign_in_started_event_to_json(self):
        event = SignInStartedEvent(1, 'ggg')
        self.assertEqual('{"time": 1, "user_id": "ggg"}', event.to_json())

    def test_one_time_password_sent_event_creation(self):
        event = OneTimePasswordSentEvent(1, 'ggg', 'pwd', DeliveryMethod.EMAIL, 123, 'corr_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('ggg', event.user_id)
        self.assertEqual('pwd', event.password)
        self.assertEqual(DeliveryMethod.EMAIL, event.delivery_method)
        self.assertEqual(123, event.expires_at)
        self.assertEqual('corr_id', event.correlation_id)

    def test_one_time_password_sent_event_to_json(self):
        event = OneTimePasswordSentEvent(1, 'ggg', 'pwd', DeliveryMethod.EMAIL, 123, 'corr_id')
        self.assertEqual(
            '{"time": 1, "user_id": "ggg", "password": "pwd", "delivery_method": "email", "expires_at": 123, "correlation_id": "corr_id"}',
            event.to_json())
