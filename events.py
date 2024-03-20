import json
import random
from dataclasses import dataclass, asdict, field
from enum import Enum


UserId = str


class DeliveryMethod(Enum):
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'


class SecurityChallengeType(Enum):
    CAPTCHA = 'captcha'
    SECURITY_QUESTION = 'security_question'
    MFA = 'mfa'


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)


digits = '0123456789'
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphanumeric = digits + alphabet


def password_generator():
    return ''.join(random.choices(digits, k=6))


def delivery_method_generator():
    return random.choice(list(DeliveryMethod))


def correlation_id_generator():
    return ''.join(random.choices(alphanumeric, k=10))


def challenge_id_generator():
    return ''.join(random.choices(alphanumeric, k=10))


def security_challenge_type_generator():
    return random.choice(list(SecurityChallengeType))


@dataclass
class Event:
    time: int
    user_id: UserId

    def to_json(self) -> str:
        return json.dumps(asdict(self), cls=EnumEncoder)


@dataclass
class SignInStartedEvent(Event):
    pass


@dataclass
class OneTimePasswordSentEvent(Event):
    password: str = field(default_factory=password_generator)
    delivery_method: DeliveryMethod = field(default_factory=delivery_method_generator)
    expires_at: int = None
    correlation_id: str = field(default_factory=correlation_id_generator)

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.time + 60


@dataclass
class OneTimePasswordSubmittedEvent(Event):
    password: str = field(default_factory=password_generator)
    correlation_id: str = field(default_factory=correlation_id_generator)


@dataclass
class PasswordResetRequestedEvent(Event):
    pass


@dataclass
class SecurityChallengePresentedEvent(Event):
    challenge_type: SecurityChallengeType = field(default_factory=security_challenge_type_generator)
    challenge_id: str = field(default_factory=challenge_id_generator)


@dataclass
class SecurityChallengeAnsweredEvent(Event):
    challenge_id: str = field(default_factory=challenge_id_generator)
    answer: str = 'default'


@dataclass
class SecurityChallengeFailedEvent(Event):
    challenge_id: str = field(default_factory=challenge_id_generator)
    reason: str = 'default'


@dataclass
class SecurityChallengePassedEvent(Event):
    challenge_id: str = field(default_factory=challenge_id_generator)

