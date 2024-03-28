import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, Type, Generator, List, Union

import events
from events import Event, UserId
from time_generator import TimeGenerator


class EventsGenerator(ABC):
    @abstractmethod
    def generate(self, user_id: UserId  = None) -> Generator[Event, None, None]:
        pass


class RandomEventsGenerator(EventsGenerator):
    def __init__(self, event_types: Set[Type[Event]], user_id: UserId = None, times: int = 1, time_generator=None):
        self.event_types = event_types
        self.user_id = user_id or UserId(events.userid_generator())
        self.times = times
        self.time_generator = time_generator or TimeGenerator(int(datetime.now().timestamp() * 1000))

    def generate(self, user_id: UserId = None) -> Generator[Event, None, None]:
        for _ in range(self.times):
            random_event_type = random.choice(list(self.event_types))
            yield random_event_type(time=self.time_generator.next(),
                                    user_id=user_id or self.user_id)


class SequentialEventsGenerator(EventsGenerator):
    def __init__(self, event_types: List[Union[Type[Event], Type[EventsGenerator]]], user_id: UserId = None, time_generator=None):
        self.event_types = event_types
        self.user_id = user_id or UserId(events.userid_generator())
        self.time_generator = time_generator or TimeGenerator(int(datetime.now().timestamp() * 1000))

    def generate(self, user_id: UserId = None) -> Generator[Event, None, None]:
        for event_type in self.event_types:
            if isinstance(event_type, EventsGenerator):
                yield from event_type.generate(user_id=user_id or self.user_id)
            elif issubclass(event_type, Event):
                yield event_type(time=self.time_generator.next(),  # milliseconds
                                 user_id=user_id or self.user_id)
            else:
                raise ValueError('Invalid event type')


class MultipleUsersEventsGenerator(EventsGenerator):
    def __init__(self, events_generator: EventsGenerator, users: int):
        self.events_generator = events_generator
        self.users = {UserId(events.userid_generator()) for _ in range(users)}

    def generate(self, user_id: UserId = None) -> Generator[Event, None, None]:
        for user in self.users:
            yield from self.events_generator.generate(user)
