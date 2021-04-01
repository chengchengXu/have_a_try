# -*- coding: utf-8 -*-
# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2020
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2020 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.

# -*- coding: utf-8 -*-

"""
datetime_utils.py

date and time functions

@author: yudi.wu
"""

import os
import pandas as pd
from datetime import datetime

from .. loader.cache_api import (
    get_td_from_cache,
    get_directed_td_list_from_cache,
    get_directed_td_from_cache,
    get_week_first_tds,
    get_week_last_tds,
    get_month_first_tds,
    get_month_last_tds,
)


def normalize_date(date):
    """
    将日期标准化为datetime.datetime格式

    Args:
        date (datetime or str): 日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        datetime: 标准化之后的日期

    Examples:
        >> normalize_date(datetime(2015, 1, 1))
        >> normalize_date('2015-01-01')
        >> normalize_date('20150101')
    """

    try:
        date = pd.tseries.tools.normalize_date(pd.Timestamp(date))
    except:
        raise Exception("Invalid date: {}".format(date))

    return datetime(date.year, date.month, date.day)


def is_valid_dateinput(start, end):
    """
    检查start和end的格式和范围是否合法，否则抛出异常

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        end (datetime or str): 结束日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        tuple of datetime: 长度为2，标准化之后的起始和结束日期

    Examples:
        >> is_valid_dateinput(datetime(2015, 1, 1), datetime(2016, 1, 1))
        >> is_valid_dateinput('2015-01-01', '2016-01-01')
        >> is_valid_dateinput('20150101', '20160101')
    """

    if start is None:
        start = datetime(2015, 1, 1)
    if end is None:
        end = datetime(2016, 1, 1)

    start = normalize_date(start)
    end = normalize_date(end)

    if not isinstance(start, datetime):
        raise Exception('Invalid start!')
    if not isinstance(end, datetime):
        raise Exception('Invalid end!')
    if start > end:
        raise BacktestInputError('Start ({}) must earlier than end ({})!'.format(
            start.strftime("%Y%m%d"), end.strftime("%Y%m%d")))
    return start, end


def get_trading_days(start=None, end=None, validation=True):
    """
    获取一段时间的交易日列表，包含两头

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        end (datetime or str): 结束日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        validation (bool): 是否需要对起始和结束日期进行合法性检查

    Returns:
        list of datetime: start到end之间的交易日列表，包含两头

    Examples:
        >> get_trading_days(datetime(2015, 1, 1), datetime(2016, 1, 1), False)
        >> get_trading_days('2015-01-01', '2016-01-01')
        >> get_trading_days('20150101', '20160101')
    """

    if validation:
        start, end = is_valid_dateinput(start, end)
    else:
        start = normalize_date(start)
        end = normalize_date(end)

    start = start.strftime('%Y%m%d')
    end = end.strftime('%Y%m%d')
    trading_days = [datetime.strptime(x, '%Y%m%d')
                    for x in get_td_from_cache(start, end)]

    return trading_days


def get_direct_trading_day_list(start, step, forward=True):
    """
    获取指定方向和步长的交易日列表，包含两头

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        step (int): 步长，即最远的日期距start的交易日数量
        forward (bool): True为比start大的方向，False为start小的方向

    Returns:
        list of datetime: 满足条件的交易日列表，包含两头，按从小到大排列

    Examples:
        >> get_direct_trading_day_list(datetime(2015, 1, 1), 10, False)
        >> get_direct_trading_day_list('2015-01-01', 10)
    """

    start = normalize_date(start).strftime('%Y%m%d')
    trading_days = [datetime.strptime(x, '%Y%m%d') for x in
                    get_directed_td_list_from_cache(start, step, forward)]
    return trading_days


def get_direct_trading_day(start, step, forward=True):
    """
    获取指定方向和步长的交易日列表，包含两头

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        step (int): 步长，即最远的日期距start的交易日数量
        forward (bool): True为比start大的方向，False为start小的方向

    Returns:
        datetime: 满足条件的交易日日期

    Examples:
        >> get_direct_trading_day(datetime(2015, 1, 1), 10, False)
        >> get_direct_trading_day('2015-01-01', 10)
    """
    start = normalize_date(start).strftime('%Y%m%d')
    trading_day = get_directed_td_from_cache(start, step, forward)
    trading_day = datetime.strptime(trading_day, '%Y%m%d')
    return trading_day


def previous_trading_day(date):
    """
    获取前一交易日的日期

    Args:
        date (datetime or str): 日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        datetime: 前一交易日日期

    Examples:
        >> previous_trading_day(datetime(2015, 1, 1))
        >> previous_trading_day(datetime(2015, 6, 1))
    """

    return get_direct_trading_day(date, 1, False)


def get_week_first_trading_days(start, end):
    """
    获取一段时间内每周第一个交易日列表，包含两头所在的周

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        end (datetime or str): 结束日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        list of datetime: start到end之间的每周第一个交易日列表，包含两头

    Examples:
        >> get_week_first_trading_days(datetime(2015, 1, 1), datetime(2016, 1, 1))
        >> get_week_first_trading_days('2015-01-01', '2016-01-01')
        >> get_week_first_trading_days('20150101', '20160101')
    """

    start = normalize_date(start).strftime('%Y%m%d')
    end = normalize_date(end).strftime('%Y%m%d')
    trading_days = [datetime.strptime(x, '%Y%m%d')
                    for x in get_week_first_tds(start, end)]

    return trading_days


def get_week_last_trading_days(start, end):
    """
    获取一段时间内每周最后一个交易日列表，包含两头所在的周

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        end (datetime or str): 结束日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        list of datetime: start到end之间的每周最后一个交易日列表，包含两头

    Examples:
        >> get_week_last_trading_days(datetime(2015, 1, 1), datetime(2016, 1, 1))
        >> get_week_last_trading_days('2015-01-01', '2016-01-01')
        >> get_week_last_trading_days('20150101', '20160101')
    """

    start = normalize_date(start).strftime('%Y%m%d')
    end = normalize_date(end).strftime('%Y%m%d')
    trading_days = [datetime.strptime(x, '%Y%m%d')
                    for x in get_week_last_tds(start, end)]

    return trading_days


def get_month_first_trading_days(start, end):
    """
    获取一段时间内每月第一个交易日列表，包含两头所在的月

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        end (datetime or str): 结束日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        list of datetime: start到end之间的每月第一个交易日列表，包含两头

    Examples:
        >> get_month_first_trading_days(datetime(2015, 1, 1), datetime(2016, 1, 1))
        >> get_month_first_trading_days('2015-01-01', '2016-01-01')
        >> get_month_first_trading_days('20150101', '20160101')
    """

    start = normalize_date(start).strftime('%Y%m%d')
    end = normalize_date(end).strftime('%Y%m%d')
    trading_days = [datetime.strptime(x, '%Y%m%d')
                    for x in get_month_first_tds(start, end)]

    return trading_days


def get_month_last_trading_days(start, end):
    """
    获取一段时间内每月最后一个交易日列表，包含两头所在的月

    Args:
        start (datetime or str): 起始日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式
        end (datetime or str): 结束日期输入，支持datetime和str两种，str形式的日期可以是任何可被pd.tseries.tools.normalize_date处理的形式

    Returns:
        list of datetime: start到end之间的每月最后一个交易日列表，包含两头

    Examples:
        >> get_month_last_trading_days(datetime(2015, 1, 1), datetime(2016, 1, 1))
        >> get_month_last_trading_days('2015-01-01', '2016-01-01')
        >> get_month_last_trading_days('20150101', '20160101')
    """

    start = normalize_date(start).strftime('%Y%m%d')
    end = normalize_date(end).strftime('%Y%m%d')

    trading_days = [datetime.strptime(x, '%Y%m%d')
                    for x in get_month_last_tds(start, end)]

    return trading_days


def get_trading_days_by_period_type(period_type, start, end):
    if period_type == 'week_first':
        res = get_week_first_trading_days(start, end)
    elif period_type == 'week_last':
        res = get_week_last_trading_days(start, end)
    elif period_type == 'month_first':
        res = get_month_first_trading_days(start, end)
    else:
        res = get_month_last_trading_days(start, end)
    res = sorted(filter(lambda x: (x >= start and x <= end), res))
    return res
