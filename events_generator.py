import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, Type, Generator, List, Union

from events import Event, UserId


class EventsGenerator(ABC):
    @abstractmethod
    def generate(self) -> Generator[Event, None, None]:
        pass


class RandomEventsGenerator(EventsGenerator):
    def __init__(self, event_types: Set[Type[Event]], user_id: UserId, times: int):
        self.event_types = event_types
        self.user_id = user_id
        self.times = times

    def generate(self) -> Generator[Event, None, None]:
        for _ in range(self.times):
            random_event_type = random.choice(list(self.event_types))
            yield random_event_type(time=int(datetime.now().timestamp() * 1000),  # milliseconds
                                    user_id=self.user_id)


class SequentialEventsGenerator(EventsGenerator):
    def __init__(self, event_types: List[Union[Type[Event], Type[EventsGenerator]]], user_id: UserId):
        self.event_types = event_types
        self.user_id = user_id

    def generate(self):
        for event_type in self.event_types:
            if isinstance(event_type, EventsGenerator):
                yield from event_type.generate()
            elif issubclass(event_type, Event):
                yield event_type(time=int(datetime.now().timestamp() * 1000),  # milliseconds
                                 user_id=self.user_id)
            else:
                raise ValueError('Invalid event type')
