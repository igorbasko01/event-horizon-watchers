import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, Type, Generator

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
