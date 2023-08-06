# -*- utf-8 -*-
# @Time: 2021/5/30 10:17
# @Author: CACode
import time
from datetime import datetime


def conversion_types(val):
    """
    将val的类型转换为字符串并插入array
    """
    if isinstance(val, datetime):
        val = val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def date_format(time_obj=time, fmt='%Y-%m-%d %H:%M:%S'):
    """
    时间转字符串
    :param time_obj:
    :param fmt:
    :return:
    """
    _tm = time_obj.time()
    _t = time.localtime(_tm)
    return time.strftime(fmt, _t)


def datetime_to_time(d_time):
    pass


def time_to_datetime(t_time):
    """
    时间戳转datetime
    """
    try:
        d_time = datetime.fromtimestamp(t_time)
    except OSError as ose:
        return None
    return d_time
