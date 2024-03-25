import unittest

from time_generator import TimeGenerator


class TimeGeneratorTests(unittest.TestCase):
    def test_time_generator(self):
        time_generator = TimeGenerator(1)
        time = time_generator.next()
        next_time = time_generator.next()
        self.assertEqual(1, time)
        self.assertEqual(2, next_time)