# -*- coding: utf-8 -*-

import re
import time
import datetime
import dateutil
from dateutil.relativedelta import relativedelta

space_pattern = re.compile(r"[\s\xa0]+")
second_pattern = re.compile(r"(\d+)秒([前后]?)")
minute_pattern = re.compile(r"(\d+)分[钟]?([前后]?)")
hour_pattern = re.compile(r"(\d+)小时([前后]?)")
day_pattern = re.compile(r"(\d+)天([前后]?)")
week_pattern = re.compile(r"(\d+)星期([前后]?)")
month_pattern = re.compile(r"(\d+)月([前后]?)")
year_pattern = re.compile(r"(\d+)年([前后]?)")
stop_words = ["个", "的", "小", "以", "钟", "今天", ]
format_time_map = [
    ["大前天", "3天前"],
    ["前天", "2天前"],
    ["昨天", "1天前"],
    ["半天", "12小时后"],
    ["明天", "1天后"],
    ["两天", "2天"],
    ["后天", "2天后"],
    ["大后天", "3天后"],
    ["上周", "1周前周"],
    ["下周", "1周后周"],
    ["下下周", "2周后"],
    ["周日", "周7"],
    ["星期天", "周7"],
    ["星期", "周"],
    ["上月", "1月前"],
    ["下月", "1月后"],
    ["去年", "1年前"],
    ["明年", "1年后"],
    ["半", "30分"],
]


def _now():
    """datetime.datetime(2018, 11, 3, 21, 44, 34, 259451)"""
    return datetime.datetime.now()


def parse_second(time_str):
    seconds = relativedelta(seconds=0)
    m = second_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return seconds - relativedelta(seconds=int(m[0][0]))
        else:
            return seconds + relativedelta(seconds=int(m[0][0]))
    return seconds


def parse_minute(time_str):
    minutes = relativedelta(minutes=0)
    m = minute_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return minutes - relativedelta(minutes=int(m[0][0]))
        else:
            return minutes + relativedelta(minutes=int(m[0][0]))
    return minutes


def parse_hour(time_str):
    hours = relativedelta(hours=0)
    m = hour_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return hours - relativedelta(hours=int(m[0][0]))
        else:
            return hours + relativedelta(hours=int(m[0][0]))
    return hours


def parse_day(time_str):
    days = relativedelta(days=0)
    m = day_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return days - relativedelta(days=int(m[0][0]))
        else:
            return days + relativedelta(days=int(m[0][0]))

    return days


def parse_week(time_str):
    weeks = relativedelta(weeks=0)
    m = week_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return weeks - relativedelta(weeks=int(m[0][0]))
        else:
            return weeks + relativedelta(weeks=int(m[0][0]))
    return weeks


def parse_month(time_str):
    months = relativedelta(months=0)
    m = month_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return months - relativedelta(months=int(m[0][0]))
        else:
            return months + relativedelta(months=int(m[0][0]))
    return months


def parse_year(time_str):
    years = relativedelta(years=0)
    m = year_pattern.findall(time_str)
    if m:
        if m[0][1] == "前":
            return years + relativedelta(years=int(m[0][0]))
        else:
            return years - relativedelta(years=int(m[0][0]))
    return years


def match_and_replace(time_str):
    pass


def _preprocess(time_str):
    """
    time string preprocessing eg: encode or space repalce
    :param time_str:
    :return: time_str
    """
    time_str = space_pattern.sub(" ", time_str.strip())
    return time_str


def parse(time_str):
    """
    processing time string
    :param time_str:
    :return:
    """
    if not isinstance(time_str, str):
        return None

    time_str = _preprocess(time_str=time_str)
    seconds = parse_second(time_str)
    minutes = parse_minute(time_str)
    hours = parse_hour(time_str)
    days = parse_day(time_str)
    weeks = parse_week(time_str)
    months = parse_month(time_str)
    years = parse_year(time_str)
    p_time = _now() + seconds + minutes + hours + days + weeks + months + years
    return p_time


if __name__ == '__main__':
    # print(parse("3秒前"))
    print(parse("２天前"))