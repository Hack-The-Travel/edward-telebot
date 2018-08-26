# -*- coding: utf-8 -*-
import pytest
from bot import runtime


class TestUtils():
    @pytest.mark.parametrize(
        'start_time, check_time, runtime_str', (
            (1535285964, 1535285964, 'Up 0 second.'),
            (1535285964, 1535286024, 'Up 1 second.'),
            (1535285964, 1535286084, 'Up 2 seconds.'),
            (1535285964, 1535289564, 'Up 1 minute.'),
            (1535285964, 1535289564, 'Up 2 minutes.'),
            (1535285964, 1535289564, 'Up 1 hour.'),
            (1535285964, 1535293164, 'Up 2 hours.'),
            (1535285964, 1535372364, 'Up 1 day.'),
            (1535285964, 1535375964, 'Up 1 day, 1 hour.'),
            (1535285964, 1535379564, 'Up 1 day, 2 hours.'),
            (1535285964, 1535458764, 'Up 2 days.'),
            (1535285964, 1535462364, 'Up 2 days, 1 hour.'),
            (1535285964, 1535465964, 'Up 2 days, 2 hours.'),
        ))
    def test_runtime(self, start_time, check_time, runtime_str):
        assert runtime(start_time=start_time, check_time=check_time) == runtime_str
