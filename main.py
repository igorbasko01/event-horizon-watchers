from datetime import datetime

from events import SignInStartedEvent, SecurityChallengePassedEvent, \
    SecurityChallengeFailedEvent, SecurityChallengePresentedEvent, SecurityChallengeAnsweredEvent
from events_generator import RandomEventsGenerator, SequentialEventsGenerator, MultipleUsersEventsGenerator
from file_writer import EventsFileWriter
from time_generator import TimeGenerator

if __name__ == '__main__':
    security_challenge_response_events = {SecurityChallengePassedEvent, SecurityChallengeFailedEvent}
    time_generator = TimeGenerator(int(datetime.now().timestamp() * 1000))
    seq_events_generator = SequentialEventsGenerator([
        SignInStartedEvent,
        SecurityChallengePresentedEvent,
        SecurityChallengeAnsweredEvent,
        RandomEventsGenerator(security_challenge_response_events, time_generator=time_generator)
    ], time_generator=time_generator)
    generator = MultipleUsersEventsGenerator(seq_events_generator, 300)
    with open('events.json', 'w') as file:
        EventsFileWriter.write(generator, file)
    print('Done !')
