# -*- coding: utf-8 -*-

import re
import datetime
from dateutil import tz
from dateutil import parser
from dateutil.relativedelta import relativedelta

__all__ = ["parse"]

SPACE_PATTERN = re.compile(r"[\s\xa0]+")
UNICODE_STRING_1 = re.compile(r'([\u4E00-\u9FA5]+)([^\s\u4E00-\u9FA5])')  # \u4E00-\u9FA5是中文字符集
UNICODE_STRING_2 = re.compile(r'([^\s\u4E00-\u9FA5])([\u4E00-\u9FA5]+)')

# 处理固定格式的时间
FORMAT_STRINGS = (
    u"%Y-%m-%d %H:%M:%S",  # 2014-09-16 13:47:05
    u"%Y/%m/%d %H:%M:%S",  # 2014/09/16 13:47:05
    u"%Y-%m-%dT%H:%M:%S.%fZ",  # 2014-09-18T10:42:16.126Z  我怀疑这个而不是UTC时间
    u"%Y-%m-%dT%H:%M:%S%z",  # 2014-09-18T10:42:16+08:00
    u"%Y-%m-%dT%H:%M:%S%z",  # 2014-09-18T10:42:16
    u"%Y-%m-%dT%H:%M:%S",  # 2014-09-18T10:42:16
    u"%Y,%m,%d,%H,%M,%S",  # 2017,06,14,10,33,00
    u"%Y-%m-%d %H:%M",  # 2014-09-16 13:47
    u"%Y/%m/%d",  # 2017/06/10
    u"%m/%d/%Y",  # 06/10/2017
    u"%y-%m-%d %H:%M",  # 14-09-16 13:47
    u"%Y-%m-%d",  # 2014-09-16
    u"%y-%m-%d",  # 15-10-08
    u"%Y.%m.%d",  # 2016.04.25
    u"%m-%d %H:%M",  # 09-16 13:47
    u"%m-%d %H:%M:%S",  # 09-16 13:47:05
    u"%H:%M:%S",  # 13:47:01
    u"%m-%d",  # 09-16
    u"%H:%M",  # 13:47
    u"%m 月 %d 日 %H:%M",  # 10月23日 15:23
    u"%m 月 %d 日",  # 10月23日
    u"%Y/%m/%d %H:%M",  # 2017/06/27 07:37
    u"%Y 年 %m 月 %d 日",  # 2017年10月23日
    u"今天 %H:%M",  # 今天 15:23
    u"今天 %H:%M:%S",  # 今天 09:36:44
    u"%Y 年 %m 月 %d 日 %H:%M",  # 2016年10月23日 15:23
    u"%Y 年 %m 月 %d 日 %H:%M:%S",  # 2017年06月28日 10:14:15
    u"%Y 年 %m 月 %d 日 %H 时 %M 分",  # 2017年06月06日  10时49分
)


RE_PATTERNS = (
    (re.compile(r"昨天 (\d{2}):(\d{2})"), lambda r: (_now() - relativedelta(days=1)).replace(hour=int(r[0]), minute=int(r[1]), second=0, microsecond=0)),  # 昨天 13:47
    (re.compile(r"前天 (\d{2}):(\d{2})"), lambda r: (_now() - relativedelta(days=2)).replace(hour=int(r[0]), minute=int(r[1]), second=0, microsecond=0)),  # 前天 13:47
    (re.compile(r"^(\d+) 天前 (\d{2}):(\d{2})"), lambda r: (_now() - relativedelta(days=int(r[0]))).replace(hour=int(r[1]), minute=int(r[2]), second=0, microsecond=0)),  # 5 天前 13:47
    (re.compile(r"^(\d+) 月前$"), lambda r: _zero(_now() - relativedelta(months=int(r)))),  # 2月前
    (re.compile(r"^(\d+) 个月前$"), lambda r: _zero(_now() - relativedelta(months=int(r)))),  # 2月前
    (re.compile(r"^(\d+) 年前$"), lambda r: _zero(_now() - relativedelta(years=int(r)))),  # 1年前
    (re.compile(r"^(\d+) 天前$"), lambda r: _zero(_now() - relativedelta(days=int(r)))),  # 1天前
    (re.compile(r"^(\d+)days$"), lambda r: _zero(_now() - relativedelta(days=int(r)))),  # 1天前
    (re.compile(r"^(\d+) 小时前$"), lambda r: (_now() - relativedelta(hours=int(r))).replace(minute=0, second=0, microsecond=0)),  # 1小时前
    (re.compile(r"^(\d+)hour$"), lambda r: (_now() - relativedelta(hours=int(r))).replace(minute=0, second=0, microsecond=0)),  # 1小时前
    (re.compile(r"^(\d+)hours$"), lambda r: (_now() - relativedelta(hours=int(r))).replace(minute=0, second=0, microsecond=0)),  # 1小时前
    (re.compile(r"^(\d+) 分钟前$"), lambda r: (_now() - relativedelta(minutes=int(r))).replace(second=0, microsecond=0)),  # 5分钟前
    (re.compile(r"^半小时前$"), lambda r: (_now() - relativedelta(minutes=int(30))).replace(second=0, microsecond=0)),  # 半小时前
    (re.compile(r"^(\d+) 秒前$"), lambda r: (_now() - relativedelta(seconds=int(r), microsecond=0))),  # 10秒前
    (re.compile(r"^(\d+)$"), lambda r: datetime.datetime.fromtimestamp(int(r))),  # 1423476240
    (re.compile(r"^昨天$"), lambda r: _zero(_now() - datetime.timedelta(days=1))),  # 昨天
    (re.compile(r"^前天$"), lambda r: _zero(_now() - datetime.timedelta(days=2))),  # 前天
    (re.compile(r"^刚刚$"), lambda r: _now()),  # 刚刚
    (re.compile(r"^一天内$"), lambda r: _zero(_now() - datetime.timedelta(days=1))),  # 刚刚
)


def _now():
    return datetime.datetime.now()


def _zero(time_obj):
    return time_obj.replace(hour=0, minute=0, second=0, microsecond=0)


def _patch(format_string, time_obj):
    """
    对于没有年月日的数据，解析后的年月日不是当前日期，要修改
    """
    now = _now()
    if not ("%d" in format_string):
        time_obj = time_obj.replace(day=now.day)
    if not ("%m" in format_string):
        time_obj = time_obj.replace(month=now.month)
    if not ("%y" in format_string or "%Y" in format_string):
        time_obj = time_obj.replace(year=now.year)
        if (time_obj > now) and ("%m" in format_string):  # 处理跨年的问题
            time_obj = time_obj.replace(year=now.year-1)
    return time_obj


def _normalize(time_string, encoding):
    """
    @:function:
    - 统一使用 unicode 编码
    - 中文空格替换成英文空格
    - 去掉字符串前后的空格
    - 字符串内部的连续空格换成一个空格
    - 中文字符和其他字符之间保证有一个空格
    """
    if not isinstance(time_string, str):
        time_string = str(time_string)
    time_string = SPACE_PATTERN.sub(u" ", time_string.strip())
    time_string = UNICODE_STRING_1.sub(lambda x: x.group(1) + " " + x.group(2), time_string)
    time_string = UNICODE_STRING_2.sub(lambda x: x.group(1) + " " + x.group(2), time_string)
    return time_string


def parse(time_string, encoding="utf-8", default=None):
    """
    parse("2014-09-16") -> datetime.datetime(2014, 9, 16, 0, 0, 0,)
    parse("2017-07-07T09:44:52+08:00") -> datetime.datetime(2017, 7, 7, 10, 44, 52, tzinfo=tzfile('PRC'))
    """
    time_string = _normalize(time_string, encoding)
    utf8_time_string = time_string.encode("utf-8", "ignore")
    for format_string in FORMAT_STRINGS:
        try:
            time_obj = datetime.datetime.strptime(utf8_time_string, format_string.encode("utf-8", "ignore"))
            return _patch(format_string, time_obj)
        except:
            continue
    if "+" in time_string or "-" in time_string:
        to_zone = tz.gettz("Asia/Shanghai")
        return parser.parse(time_string).astimezone(to_zone)
    for re_pattern, callback in RE_PATTERNS:
        result = re_pattern.findall(time_string)
        if result:
            return callback(result[0])
    return default