from typing import TextIO

from events_generator import EventsGenerator


class EventsFileWriter:
    @staticmethod
    def write(events_generator: EventsGenerator, file_object: TextIO):
        for event in events_generator.generate():
            file_object.write(event.to_json() + '\n')