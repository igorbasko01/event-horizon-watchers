import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, Type, Generator, List, Union

from events import Event, UserId
from time_generator import TimeGenerator


class EventsGenerator(ABC):
    @abstractmethod
    def generate(self) -> Generator[Event, None, None]:
        pass


class RandomEventsGenerator(EventsGenerator):
    def __init__(self, event_types: Set[Type[Event]], user_id: UserId, times: int, time_generator=None):
        self.event_types = event_types
        self.user_id = user_id
        self.times = times
        self.time_generator = time_generator or TimeGenerator(int(datetime.now().timestamp() * 1000))

    def generate(self) -> Generator[Event, None, None]:
        for _ in range(self.times):
            random_event_type = random.choice(list(self.event_types))
            yield random_event_type(time=self.time_generator.next(),
                                    user_id=self.user_id)


class SequentialEventsGenerator(EventsGenerator):
    def __init__(self, event_types: List[Union[Type[Event], Type[EventsGenerator]]], user_id: UserId, time_generator=None):
        self.event_types = event_types
        self.user_id = user_id
        self.time_generator = time_generator or TimeGenerator(int(datetime.now().timestamp() * 1000))

    def generate(self):
        for event_type in self.event_types:
            if isinstance(event_type, EventsGenerator):
                yield from event_type.generate()
            elif issubclass(event_type, Event):
                yield event_type(time=self.time_generator.next(),  # milliseconds
                                 user_id=self.user_id)
            else:
                raise ValueError('Invalid event type')
