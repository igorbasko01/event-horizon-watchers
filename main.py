from events import SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent
from events_generator import RandomEventsGenerator
from file_writer import EventsFileWriter

if __name__ == '__main__':
    events = [
        SignInStartedEvent, OneTimePasswordSentEvent, SecurityChallengePassedEvent
    ]
    generator = RandomEventsGenerator(events, 'uid', 5)
    with open('events.json', 'w') as file:
        EventsFileWriter.write(generator, file)
    print('Done !')
