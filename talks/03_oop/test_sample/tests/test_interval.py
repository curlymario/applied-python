import unittest
from unittest.mock import patch
from datetime import datetime

from interval import TimeInterval

class TimeIntervalTestCase(unittest.TestCase):
    def setUp(self):
        self._interval = TimeInterval(
            datetime(2017, 1, 1),
            datetime(2018, 1, 1),
        )

    def test_init(self):
        interval = self._interval

        self.assertEqual(
            interval._begin,
            datetime(2017, 1, 1)
        )

        self.assertEqual(
            interval._end,
            datetime(2018, 1, 1)
        )

    def test_str(self):
        interval = self._interval
        
        self.assertEqual(
            str(interval),
            '2017-01-01 00:00:00 -> 2018-01-01 00:00:00'
        )
