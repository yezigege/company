# -*- coding: utf-8 -*-
"""
=========================
        日期工具
=========================
"""
import calendar
import datetime
import math
import time


class DateUtil():
    """
    日期工具类
    """
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    MS_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
    DATETIME_FORMAT_SLASH = '%Y/%m/%d %H:%M'
    UPLOAD_DIR_FORMAT = '%Y%m%d'
    DATE_FORMAT = '%Y-%m-%d'
    DATE_FORMAT_NEW = '%Y%m%d'
    TIME_FORMAT = '%H:%M:%S'
    TIME_FORMAT_H_M = '%H:%M'
    DATE_FORMAT_SLASH = '%Y/%m/%d'
    CHAT_ROOM_DATE_FORMAT = '%m-%d'
    FEED_DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    FEED_DATETIME_FORMAT2 = '%H:%M'
    DATE_FORMAT_MONTH = '%Y-%m'
    FORMAT_YEAR = '%Y'
    FORMAT_MONTH = '%m'

    @classmethod
    def is_end_of_month(cls, timestamp):
        two_day_later_timestamp = timestamp + 86400 * 2
        if time.localtime(two_day_later_timestamp).tm_mon != time.localtime(timestamp).tm_mon:
            return True
        return False

    @classmethod
    def delta_date(cls, delta):
        '''
        周一为0, 周日为6,计算本周的日期
        :param delta:日期差
        '''
        today_date = datetime.datetime.today()
        days = delta - today_date.weekday()
        days = days + 7 if days < 0 else days
        return datetime.datetime.today() + datetime.timedelta(days=(delta - today_date.weekday()))

    @classmethod
    def delta_date_str(cls, delta, x=None, date_type='str'):
        x = x if x else datetime.date.today()
        the_date = (x - datetime.timedelta(days=delta))
        if date_type == 'str':
            return DateUtil.date_to_str(the_date)
        return the_date

    @classmethod
    def datetime_to_str(cls, x=None, fmt=DATETIME_FORMAT):
        x = x if x else datetime.datetime.now()
        return x.strftime(fmt)

    @classmethod
    def str_to_datetime(cls, x='', fmt=DATETIME_FORMAT):
        if not x:
            v = datetime.datetime.now()
        else:
            v = datetime.datetime.strptime(x, fmt)
        return v

    @classmethod
    def date_to_str(cls, x=None, fmt=DATE_FORMAT):
        return cls.datetime_to_str(x, fmt)

    @classmethod
    def str_to_date(cls, x='', fmt=DATE_FORMAT):
        if not x:
            v = datetime.date.today()
        else:
            v = datetime.datetime.strptime(x, fmt).date()
        return v

    @classmethod
    def delta_hour(cls, delta):
        time_now = datetime.datetime.now()
        hourly_time = (time_now - datetime.timedelta(hours=delta)).replace(minute=0, second=0, microsecond=0)
        return hourly_time

    @classmethod
    def str_to_timestamp(cls, x, fmt=DATETIME_FORMAT):
        time_array = time.strptime(x, fmt)
        return int(time.mktime(time_array))

    @classmethod
    def timestamp_to_datetime_str(cls, timestamp=None, digit=10, fmt=DATETIME_FORMAT):
        if timestamp is None:
            timestamp = int(time.time())
        if not isinstance(timestamp, int):
            timestamp = int(timestamp)
        if digit == 13:
            timestamp = timestamp / 1000
        return datetime.datetime.fromtimestamp(timestamp).strftime(fmt)

    @classmethod
    def get_now_and_date_str(cls):
        now = datetime.datetime.now()
        return cls.datetime_to_str(now), cls.date_to_str(now)

    @classmethod
    def get_feed_format_time(cls, ts):
        dt = datetime.datetime.fromtimestamp(ts)
        now_dt = datetime.datetime.now()
        dif = now_dt.date() - dt.date()
        if dif.days == 0:
            return '%s %s' % ('今天', dt.strftime(cls.FEED_DATETIME_FORMAT2))
        elif dif.days == 1:
            return '%s %s' % ('昨天', dt.strftime(cls.FEED_DATETIME_FORMAT2))
        elif dif.days == 2:
            return '%s %s' % ('前天', dt.strftime(cls.FEED_DATETIME_FORMAT2))
        else:
            return dt.strftime(cls.FEED_DATETIME_FORMAT)

    @classmethod
    def get_first_and_last_day(cls):
        # 获取当前年份
        year = datetime.date.today().year
        # 获取当前月份
        month = datetime.date.today().month
        # 获取当前月的第一天的星期和当月总天数
        week_day, month_count_day = calendar.monthrange(year, month)
        # 获取当前月份第一天
        first_day = datetime.date(year, month, day=1)
        # 获取当前月份最后一天
        last_day = datetime.date(year, month, day=month_count_day)
        # 返回每月第一天和最后一天  格式为 '%Y-%m-%d'
        return str(first_day), str(last_day)

    @classmethod
    def get_yesterday_month(cls, fmt):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return cls.date_to_str(yesterday, fmt)

    @classmethod
    def get_year_month(cls):
        # 获取当前年份
        year = datetime.date.today().year
        # 获取当前月份
        month = datetime.date.today().month
        return f'{year}-{month}'

    @classmethod
    def split_duration_by_dt(cls, begin_ts, duration):
        """按天拆分时长"""
        begin_dt = datetime.datetime.fromtimestamp(begin_ts)
        first_day_delta_ts = int((datetime.datetime(
            begin_dt.year, begin_dt.month, begin_dt.day) + datetime.timedelta(
            days=1)).timestamp() - begin_ts)
        left_ts = max(duration - first_day_delta_ts, 0)
        overflow_days = math.ceil(left_ts / 86400)
        data = dict()
        for d in range(overflow_days + 1):
            dt = cls.date_to_str(x=(begin_dt + datetime.timedelta(days=d)))
            if d == 0:
                data[dt] = int(min(duration, first_day_delta_ts))
            elif d == overflow_days:
                left_ts = left_ts % 86400
                data[dt] = left_ts or 86400
            else:
                data[dt] = 86400
        return data

    @classmethod
    def date_span_list(cls, start_date, end_date):
        if isinstance(start_date, str):
            start_date = cls.str_to_date(start_date)
        elif isinstance(start_date, datetime.datetime):
            start_date = start_date.date()

        if isinstance(end_date, str):
            end_date = cls.str_to_date(end_date)
        elif isinstance(end_date, datetime.datetime):
            end_date = end_date.date()

        date_span_list = []
        while start_date <= end_date:
            date_span_list.append(cls.date_to_str(start_date))
            start_date = start_date + datetime.timedelta(days=1)

        return date_span_list

    @staticmethod
    def datetime_of_n_days_and_hour_ago(n: int, hour: int):
        """
        n天前hour点钟
        :param n: 天数
        :param hour: 小时
        :return: 日期
        """
        dt = datetime.datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
        return dt - datetime.timedelta(days=n)

    @classmethod
    def get_now_to_tomorrow_second(cls):
        """
        获取现在到明天0点的剩余秒
        :return:
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow_start_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
        now_time = int(time.time())
        return tomorrow_start_time - now_time


def date2timestamp(date_obj):
    """date or datetime转时间戳"""
    return time.mktime(date_obj.timetuple())


def date2datetime(date_obj):
    """date转datetime"""
    return datetime.datetime(year=date_obj.year, month=date_obj.month, day=date_obj.day)
