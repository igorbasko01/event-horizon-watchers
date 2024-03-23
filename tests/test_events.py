import unittest

from events import Event, SignInStartedEvent, OneTimePasswordSentEvent, DeliveryMethod, OneTimePasswordSubmittedEvent, \
    SecurityChallengePresentedEvent, SecurityChallengeType, SecurityChallengeAnsweredEvent, \
    SecurityChallengeFailedEvent, SecurityChallengePassedEvent


class EventTests(unittest.TestCase):

    def test_event_creation(self):
        event = Event(1, 'user_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)

    def test_event_to_json(self):
        event = Event(1, 'user_id')
        self.assertEqual('{"time": 1, "user_id": "user_id", "event_name": "Event"}', event.to_json())

    def test_sign_in_started_event_creation(self):
        event = SignInStartedEvent(1, 'user_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('user_id', event.user_id)

    def test_sign_in_started_event_to_json(self):
        event = SignInStartedEvent(1, 'user_id')
        self.assertEqual('{"time": 1, "user_id": "user_id", "event_name": "SignInStartedEvent"}', event.to_json())

    def test_one_time_password_sent_event_creation(self):
        event = OneTimePasswordSentEvent(1, 'user_id', 'pwd', DeliveryMethod.EMAIL, 123, 'corr_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('user_id', event.user_id)
        self.assertEqual('pwd', event.password)
        self.assertEqual(DeliveryMethod.EMAIL, event.delivery_method)
        self.assertEqual(123, event.expires_at)
        self.assertEqual('corr_id', event.correlation_id)

    def test_one_time_password_sent_event_to_json(self):
        event = OneTimePasswordSentEvent(1, 'u_id', 'pwd', DeliveryMethod.EMAIL, 123, 'corr_id')
        self.assertEqual(
            '{"time": 1, "user_id": "u_id", "password": "pwd", "delivery_method": "email", "expires_at": 123, "correlation_id": "corr_id", "event_name": "OneTimePasswordSentEvent"}',
            event.to_json())

    def test_one_time_password_sent_event_default(self):
        event = OneTimePasswordSentEvent(1, 'u_id')
        self.assertIsNotNone(event.password)
        self.assertIsNotNone(event.delivery_method)
        self.assertEqual(61, event.expires_at)
        self.assertIsNotNone(event.correlation_id)

    def test_one_time_password_submitted_event_creation(self):
        event = OneTimePasswordSubmittedEvent(1, 'user_id', 'pwd', 'corr_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('user_id', event.user_id)
        self.assertEqual('pwd', event.password)
        self.assertEqual('corr_id', event.correlation_id)

    def test_one_time_password_submitted_event_default(self):
        event = OneTimePasswordSubmittedEvent(1, 'u_id')
        self.assertEqual(1, event.time)
        self.assertEqual('u_id', event.user_id)
        self.assertIsNotNone(event.password)
        self.assertIsNotNone(event.correlation_id)

    def test_security_challenge_presented_event_creation(self):
        event = SecurityChallengePresentedEvent(1, 'user_id', SecurityChallengeType.CAPTCHA, 'challenge_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('user_id', event.user_id)
        self.assertEqual(SecurityChallengeType.CAPTCHA, event.challenge_type)
        self.assertEqual('challenge_id', event.challenge_id)

    def test_security_challenge_presented_event_default(self):
        event = SecurityChallengePresentedEvent(1, 'user_id')
        self.assertEqual(1, event.time)
        self.assertEqual('user_id', event.user_id)
        self.assertIsNotNone(event.challenge_type)
        self.assertIsNotNone(event.challenge_id)

    def test_security_challenge_answered_event_creation(self):
        event = SecurityChallengeAnsweredEvent(1, 'user', 'challenge_id', 'answer')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('user', event.user_id)
        self.assertEqual('challenge_id', event.challenge_id)
        self.assertEqual('answer', event.answer)

    def test_security_challenge_answered_event_default(self):
        event = SecurityChallengeAnsweredEvent(1, 'user')
        self.assertEqual(1, event.time)
        self.assertEqual('user', event.user_id)
        self.assertIsNotNone(event.challenge_id)
        self.assertIsNotNone(event.answer)

    def test_security_challenge_failed_event_creation(self):
        event = SecurityChallengeFailedEvent(1, 'uid', 'challenge_id', 'reason')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('challenge_id', event.challenge_id)
        self.assertEqual('reason', event.reason)

    def test_security_challenge_failed_event_default(self):
        event = SecurityChallengeFailedEvent(1, 'uid')
        self.assertEqual(1, event.time)
        self.assertEqual('uid', event.user_id)
        self.assertIsNotNone(event.challenge_id)
        self.assertIsNotNone(event.reason)

    def test_security_challenge_passed_event_creation(self):
        event = SecurityChallengePassedEvent(1, 'uid', 'challenge_id')
        self.assertIsInstance(event, Event)
        self.assertEqual(1, event.time)
        self.assertEqual('uid', event.user_id)
        self.assertEqual('challenge_id', event.challenge_id)

    def test_security_challenge_passed_event_default(self):
        event = SecurityChallengePassedEvent(1, 'uid')
        self.assertEqual(1, event.time)
        self.assertEqual('uid', event.user_id)
        self.assertIsNotNone(event.challenge_id)

    def test_event_adds_event_name_to_json(self):
        event = SignInStartedEvent(1, 'user_id')
        self.assertEqual('{"time": 1, "user_id": "user_id", "event_name": "SignInStartedEvent"}', event.to_json())