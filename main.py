from typing import Type, Set

from events import SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent, Event, \
    SecurityChallengeFailedEvent, SecurityChallengePresentedEvent, SecurityChallengeAnsweredEvent
from events_generator import RandomEventsGenerator, SequentialEventsGenerator
from file_writer import EventsFileWriter

if __name__ == '__main__':
    security_challenge_response_events = {SecurityChallengePassedEvent, SecurityChallengeFailedEvent}
    uid = 'uid'
    generator = SequentialEventsGenerator([
        SignInStartedEvent,
        SecurityChallengePresentedEvent,
        SecurityChallengeAnsweredEvent,
        RandomEventsGenerator(security_challenge_response_events, uid, 1)
    ], uid)
    with open('events.json', 'w') as file:
        EventsFileWriter.write(generator, file)
    print('Done !')
