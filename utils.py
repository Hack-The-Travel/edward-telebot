# -*- coding: utf-8 -*-
from typing import List
import datetime


def uptime(start: datetime.datetime, check: datetime.datetime) -> str:
    delta: datetime.timedelta = check - start
    delta_days: int = delta.days
    delta_hours: int = delta.seconds // 3600
    up: List[str] = []
    if delta_days > 0:
        up.append('{} day{}'.format(delta_days, '' if delta_days == 1 else 's'))
    if delta_hours > 0:
        up.append('{} hour{}'.format(delta_hours, '' if delta_hours == 1 else 's'))
    if len(up) == 0:
        return 'Up 0 hours.'
    return 'Up {}.'.format(', '.join(up))
