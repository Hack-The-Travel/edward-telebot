# -*- coding: utf-8 -*-
import pytest
import datetime
from utils import uptime


now = datetime.datetime.utcnow()


class TestUtils():
    @pytest.mark.parametrize(
        'start, check, uptime_str', (
            (now, now + datetime.timedelta(hours=0.5), 'Up 0 hours.'),
            (now, now + datetime.timedelta(days=1), 'Up 1 day.'),
            (now, now + datetime.timedelta(days=1, hours=1), 'Up 1 day, 1 hour.'),
            (now, now + datetime.timedelta(days=1, hours=2), 'Up 1 day, 2 hours.'),
            (now, now + datetime.timedelta(days=2), 'Up 2 days.'),
            (now, now + datetime.timedelta(days=2, hours=1), 'Up 2 days, 1 hour.'),
            (now, now + datetime.timedelta(days=2, hours=2), 'Up 2 days, 2 hours.'),
        ))
    def test_runtime(self, start, check, uptime_str):
        assert uptime(start, check) == uptime_str
