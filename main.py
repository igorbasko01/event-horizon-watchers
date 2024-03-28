from datetime import datetime

from events import SignInStartedEvent, SecurityChallengePassedEvent, \
    SecurityChallengeFailedEvent, SecurityChallengePresentedEvent, SecurityChallengeAnsweredEvent
from events_generator import RandomEventsGenerator, SequentialEventsGenerator
from file_writer import EventsFileWriter
from time_generator import TimeGenerator

if __name__ == '__main__':
    security_challenge_response_events = {SecurityChallengePassedEvent, SecurityChallengeFailedEvent}
    uid = 'uid'
    time_generator = TimeGenerator(int(datetime.now().timestamp() * 1000))
    generator = SequentialEventsGenerator([
        SignInStartedEvent,
        SecurityChallengePresentedEvent,
        SecurityChallengeAnsweredEvent,
        RandomEventsGenerator(security_challenge_response_events, uid, 1, time_generator)
    ], uid, time_generator)
    with open('events.json', 'w') as file:
        EventsFileWriter.write(generator, file)
    print('Done !')
