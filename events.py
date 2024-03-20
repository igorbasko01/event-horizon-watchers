import json
from dataclasses import dataclass, asdict
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


@dataclass
class Event:
    time: int

    def to_json(self) -> str:
        return json.dumps(asdict(self), cls=EnumEncoder)


@dataclass
class SignInStartedEvent(Event):
    user_id: UserId


@dataclass
class OneTimePasswordSentEvent(Event):
    user_id: UserId
    password: str
    delivery_method: DeliveryMethod
    expires_at: int
    correlation_id: str


@dataclass
class OneTimePasswordSubmittedEvent(Event):
    user_id: UserId
    password: str
    correlation_id: str


@dataclass
class PasswordResetRequestedEvent(Event):
    user_id: UserId


@dataclass
class SecurityChallengePresentedEvent(Event):
    user_id: UserId
    challenge_type: SecurityChallengeType
    challenge_id: str


@dataclass
class SecurityChallengeAnsweredEvent(Event):
    user_id: UserId
    challenge_id: str
    answer: str


@dataclass
class SecurityChallengeFailedEvent(Event):
    user_id: UserId
    challenge_id: str
    reason: str


@dataclass
class SecurityChallengePassedEvent(Event):
    user_id: UserId
    challenge_id: str

