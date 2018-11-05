# -*- coding: utf-8 -*-
# To run these tests, install nose(pip install nose) and run `nosetests` at parent folder

import datetime
from timeformat import dateformatting
from dateutil import tz
from freezegun import freeze_time

DEFAULT_DATETIME = "2014-09-16 13:47:05"
to_zone = tz.gettz('Asia/Shanghai')


@freeze_time(DEFAULT_DATETIME)
def assert_equal_after_parse(v1, v2):
    v = dateformatting.parse(v1)
    print("Origin: %s, Parsed: %s, Need: %s" % (v1, v, v2))
    assert v == v2


def test_parse_normal():
    for v1, v2 in (
            (u"2014-09-16 13:47:05", datetime.datetime(2014, 9, 16, 13, 47, 5)),
            (u"2017-07-07T09:44:52", datetime.datetime(2017, 7, 7, 9, 44, 52)),
            (u"2017-09-18T18:42:16.126Z", datetime.datetime(2017, 9, 18, 18, 42, 16, 126000)),
            (u"2017-07-07T09:44:52+0800", datetime.datetime(2017, 7, 7, 9, 44, 52, tzinfo=to_zone)),
            (u"2017-07-07T09:44:52+08:00", datetime.datetime(2017, 7, 7, 9, 44, 52, tzinfo=to_zone)),
            (u"2014/09/16 13:47:05", datetime.datetime(2014, 9, 16, 13, 47, 5)),
            (u"2017,06,14,10,33,00", datetime.datetime(2017, 6, 14, 10, 33, 0)),
            (u"2014/09/16", datetime.datetime(2014, 9, 16, 0, 0, 0)),
            (u"09/16/2014", datetime.datetime(2014, 9, 16, 0, 0, 0)),
            (u"2014/09/16 5:47:05", datetime.datetime(2014, 9, 16, 5, 47, 5)),
            (u"2014-09-16 13:47", datetime.datetime(2014, 9, 16, 13, 47, 0)),
            (u"14-09-16 13:47", datetime.datetime(2014, 9, 16, 13, 47, 0)),
            (u"2014-09-16", datetime.datetime(2014, 9, 16, 0, 0, 0)),
            (u"14-09-16", datetime.datetime(2014, 9, 16, 0, 0, 0)),
            (u"2014.09.16", datetime.datetime(2014, 9, 16, 0, 0, 0)),
            (u"09-16 13:47", datetime.datetime(2014, 9, 16, 13, 47, 0)),
            (u"09-16 13:47:05", datetime.datetime(2014, 9, 16, 13, 47, 5)),
            (u"13:47:05", datetime.datetime(2014, 9, 16, 13, 47, 5)),
            (u"09-16", datetime.datetime(2014, 9, 16, 0, 0, 0)),
            (u"13:47", datetime.datetime(2014, 9, 16, 13, 47, 0)),
            (u"昨天 13:47", datetime.datetime(2014, 9, 15, 13, 47, 0)),
            (u"5 天前 13:47", datetime.datetime(2014, 9, 11, 13, 47, 0)),
            (u"1 年前", datetime.datetime(2013, 9, 16, 0, 0, 0)),
            (u"2 年前", datetime.datetime(2012, 9, 16, 0, 0, 0)),
            (u"10 月前", datetime.datetime(2013, 11, 16, 0, 0, 0)),
            (u"10 个月前", datetime.datetime(2013, 11, 16, 0, 0, 0)),
            (u"20 天前", datetime.datetime(2014, 8, 27, 0, 0, 0)),
            (u"20days", datetime.datetime(2014, 8, 27, 0, 0, 0)),
            (u"30 小时前", datetime.datetime(2014, 9, 15, 7, 0, 0)),
            (u"半小时前", datetime.datetime(2014, 9, 16, 13, 17, 0)),
            (u"30hour", datetime.datetime(2014, 9, 15, 7, 0, 0)),
            (u"30hours", datetime.datetime(2014, 9, 15, 7, 0, 0)),
            (u"40 分钟前", datetime.datetime(2014, 9, 16, 13, 7, 0)),
            (u"50 秒前", datetime.datetime(2014, 9, 16, 13, 46, 15)),
            (u"1476175444", datetime.datetime(2016, 10, 11, 16, 44, 4)),
            (1476175444, datetime.datetime(2016, 10, 11, 16, 44, 4)),
            (u"昨天", datetime.datetime(2014, 9, 15, 0, 0, 0)),
            (u"前天", datetime.datetime(2014, 9, 14, 0, 0, 0)),
            (u"刚刚", datetime.datetime(2014, 9, 16, 13, 47, 5)),
            (u"一天内", datetime.datetime(2014, 9, 15, 0, 0, 0)),
            (u"2014年10月23日", datetime.datetime(2014, 10, 23, 0, 0, 0)),
            (u"10月23日 15:23", datetime.datetime(2013, 10, 23, 15, 23, 0)),
            (u"4月23日 15:23", datetime.datetime(2014, 4, 23, 15, 23, 0)),
            (u"4月5日 15:23", datetime.datetime(2014, 4, 5, 15, 23, 0)),
            (u"4月5日", datetime.datetime(2014, 4, 5, 0, 0, 0)),
            (u"今天 15:23", datetime.datetime(2014, 9, 16, 15, 23, 0)),
            (u"今天 15:23:05", datetime.datetime(2014, 9, 16, 15, 23, 5)),
            (u"2016年10月23日 15:23", datetime.datetime(2016, 10, 23, 15, 23, 0)),
            (u"2017年10月23日 7:49:02", datetime.datetime(2017, 10, 23, 7, 49, 2)),
            (u"2017年06月06日 10时49分", datetime.datetime(2017, 6, 6, 10, 49, 0)),
    ):
        yield assert_equal_after_parse, v1, v2


def test_parse_unnormal():
    for v1, v2 in (
            (u"2014-09-16 13:47  ", datetime.datetime(2014, 9, 16, 13, 47, 0)),  # whitespace after string
            (u"  14-09-16 13:47", datetime.datetime(2014, 9, 16, 13, 47, 0)),  # whitespace before string
            (u" 09-16   13:47", datetime.datetime(2014, 9, 16, 13, 47, 0)),  # multi whitespace in string
            (u"昨天13:47", datetime.datetime(2014, 9, 15, 13, 47, 0)),  # no whitespace
            (u"10月前  ", datetime.datetime(2013, 11, 16, 0, 0, 0)),  # no whitespace
            (u'今天\xa013:30', datetime.datetime(2014, 9, 16, 13, 30, 0)),  # 中文空格
            (u"哈哈哈", None),  # no result
    ):
        yield assert_equal_after_parse, v1, v2


@freeze_time(DEFAULT_DATETIME)
def test_parse_default():
    assert dateformatting.parse(u"No result", default="Hello Maixun!") == "Hello Maixun!"


@freeze_time(DEFAULT_DATETIME)
def test_parse_encoding():
    assert dateformatting.parse(u"50 秒前".encode("gbk"), encoding="gbk") == datetime.datetime(2014, 9, 16, 13, 46, 15)
