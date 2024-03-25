from typing import Generator


class TimeGenerator:
    def __init__(self, initial_timestamp: int, increment: int = 1):
        self.timestamp = initial_timestamp
        self.increment = increment

    def next(self) -> int:
        current_timestamp = self.timestamp
        self.timestamp += self.increment
        return current_timestamp
