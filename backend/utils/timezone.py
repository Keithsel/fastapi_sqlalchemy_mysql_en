#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zoneinfo

from datetime import datetime
from datetime import timezone as datetime_timezone

from backend.core.conf import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE) -> None:
        """
        Initialize the timezone converter

        :param tz: Timezone name, defaults to settings.DATETIME_TIMEZONE
        :return:
        """
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """Get the current time in the configured timezone"""
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        Convert a datetime object to the configured timezone

        :param dt: The datetime object to convert
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        Convert a time string to a datetime object in the configured timezone

        :param date_str: The time string
        :param format_str: The time format string, defaults to settings.DATETIME_FORMAT
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def t_str(dt: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        Convert a datetime object to a formatted time string

        :param dt: The datetime object
        :param format_str: The time format string, defaults to settings.DATETIME_FORMAT
        :return:
        """
        return dt.strftime(format_str)

    @staticmethod
    def f_utc(dt: datetime) -> datetime:
        """
        Convert a datetime object to UTC (GMT) timezone

        :param dt: The datetime object to convert
        :return:
        """
        return dt.astimezone(datetime_timezone.utc)


timezone: TimeZone = TimeZone()
