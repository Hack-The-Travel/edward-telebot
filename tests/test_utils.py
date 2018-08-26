# -*- coding: utf-8 -*-
import pytest
from bot import runtime


class TestUtils():
    @pytest.mark.parametrize(
        'start_time, check_time, runtime_str', (
            (1535285964, 1535199564, 'Up 1 day.'),
            (1535285964, 1535113164, 'Up 2 days.'),
        ))
    def test_runtime(self, start_time, check_time, runtime_str):
        assert runtime(start_time=start_time, check_time=check_time) == runtime_str
