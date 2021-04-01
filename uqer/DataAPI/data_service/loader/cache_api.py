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

import os
import re
import time
import logging
import traceback
from copy import deepcopy
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from . apiconfig import __get_service
from .. const import EQUITY_MIN_BAR

DAILY_COLS = [
    'preClosePrice', 'closePrice', 'highPrice', 'lowPrice', 'openPrice', 'turnoverVol',
    'turnoverValue', 'adjFactor', 'chgPct', 'turnoverRate', 'negMarketValue', 'marketValue'
]

INTRADAY_COLS = ['closePrice', 'highPrice', 'lowPrice',
                 'openPrice', 'turnoverVol', 'turnoverValue']

FILTER_MAP = {
    'valueRange': 'filter_value_range',
    'pctRange': 'filter_pct_range',
    'numRange': 'filter_num_range',
    'nlarge': 'filter_n_large',
    'nsmall': 'filter_n_small',
}


def get_principal_name(**kwargs):
    if 'DatayesPrincipalName' in kwargs and kwargs['DatayesPrincipalName'] is not None:
        return kwargs['DatayesPrincipalName']
    return os.getenv(u'DatayesPrincipalName', 'datacube@datayes.com')


def retry_tag(retry_num):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            count = 0
            while count < retry_num:
                try:
                    return func(*args, **kwargs)
                except:
                    count += 1
                    time.sleep(1)
            raise Exception("The data is not available at this moment.")
        return _wrapper
    return wrapper


@retry_tag(2)
def is_updated_today():
    """判断指定日期数据是否更新入数据库，只用于判断当天行情数据更新是否完成
    """

    is_updated = False
    try:
        service = __get_service()
        is_updated = service.is_updated_today(get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return is_updated


@retry_tag(2)
def get_factors_updated_date(factors):
    """
    获取因子更新时间
    """
    factor_update_map = {}
    try:
        service = __get_service()
        factor_update_map_raw = service.get_factor_updated_date(
            factors, get_principal_name())
        for dateint, item in factor_update_map_raw.iteritems():
            factor_update_map[datetime.strptime(str(dateint), '%Y%m%d')] = item
    except:
        logging.exception("error happens")
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return factor_update_map


@retry_tag(2)
def get_updated_date(collection):
    """
    获取当日各类数据更新完成时间
    Args:
        collection(str): 检查的集合名称
        - daily_equ: 个股日行情
        - daily_fund: 基金日行情
        - daily_idx: 指数日行情
        - daily_adj: 赋权因子
        - min_data: 分钟线行情
        - future: 期货行情
    """
    yesterday = datetime.now().date() - timedelta(days=1)
    latest_date = yesterday
    try:
        service = __get_service()
        latest_date_str, _ = service.get_updated_date(
            collection, get_principal_name())
        latest_date = datetime.strptime(str(latest_date_str), '%Y%m%d')

    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return latest_date


# ================== MARKET DATA FETCH APIS ==================
@retry_tag(2)
def MktDailyDataFrameGet(universe, trading_days, field=DAILY_COLS):
    """
    从CACHE数据库里取A股、基金、指数的日线数据，速度比从DataAPI中获取更快。
    可获取的数据有：前收盘价(preClosePrice), 收盘价(closePrice), 最高价(highPrice), 最低价(lowPrice), 开盘价(openPrice), 换手量(turnoverVol), 换手率(turnoverValue)

    Args:
        universe (list of str): 股票池列表
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的数据字段名称
    Returns:
        dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = set_universe('A')
        >> trading_days = get_trading_days()
        >> a_daily_prices = MktDailyDataFrameGet(universe, trading_days, ['closePrice', 'preClosePrice'])

    """

    result_from_cache = {}
    try:
        service = __get_service()
        result_from_cache = service.get_daily_data_raw_by_tdlist(
            trading_days,
            universe,
            field,
            get_principal_name(),
            False
        )
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        print (traceback.format_exc())
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()

    return result_from_cache


@retry_tag(2)
def MktIntradayDataFrameGet(universe, trading_days, field=INTRADAY_COLS, freq='1m'):
    """
    从CACHE数据库里取A股、基金、指数的分钟线数据
    可获取的数据有： 收盘价(closePrice), 最高价(highPrice), 最低价(lowPrice), 开盘价(openPrice), 换手量(turnoverVol), 换手率(turnoverValue)

    Args:
        universe (list of str): 股票池列表
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的数据字段名称
    Returns:
        dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = set_universe('A')
        >> trading_days = get_trading_days()
        >> a_daily_prices = MktIntradayDataFrameGet(universe, trading_days, ['closePrice', 'openPrice'])

    """

    translation_dict = {}
    for i, sec in enumerate(universe):
        if sec[-4:] == 'ZICN':
            if sec[0] == '0':
                sec_new = sec[:-4] + 'XSHG'
            else:
                sec_new = sec[:-4] + 'XSHE'
            translation_dict[sec_new] = sec
            universe[i] = sec_new

    result_from_cache = {}
    try:
        service = __get_service()
        result_from_cache = service.get_min_data_raw_by_tdlist(
            trading_days,
            universe,
            field,
            get_principal_name(),
            False,
            freq
        )
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()

    dict_of_df = {}
    for item, result in result_from_cache.iteritems():
        for sec_new, sec_raw in translation_dict.iteritems():
            result[sec_raw] = deepcopy(result[sec_new])
            del result[sec_new]
        for sec, value in result.iteritems():
            result[sec] = map(np.array, value)
        dict_of_df[item] = result
    return dict_of_df


# ================== USER DEFINED FACTOR DATA FETCH APIS =================
@retry_tag(2)
def UserDefinedFactorValuesGet(universe, trading_days, field, **kwargs):
    """
    从CACHE数据库里取用户自定义的因子数据
    可获取的因子数据类型可参考DataAPI中的MktStockFactorsOneDayGet

    Args:
        universe (list of str): 股票池列表
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的因子数据字段名称
    Returns:
        dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = set_universe('A')
        >> trading_days = get_trading_days()
        >> factor_values = FactorValuesGet(universe, trading_days, ['PE', 'PB'])

    """
    try:
        service = __get_service()
        result_from_cache = service.get_user_factors(
            universe,
            field,
            None,
            None,
            get_principal_name(**kwargs),
            trading_days
        )
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()

    return result_from_cache

# do not use retry annotation


def TranslateFactors(factors, start_date, **kwargs):

    try:
        service = __get_service()
        result_from_cache = service.translate_user_factors(
            factors,
            get_principal_name(**kwargs),
            start_date,
            False
        )
    except Exception as e:
        error_msg = str(e)
        if "[Name Check]" in error_msg:
            raise Exception(error_msg[error_msg.find('[Name Check]') + 12:])
        if '[Restriction]' in error_msg:
            raise Exception(error_msg[error_msg.find('[Restriction]') + 13:])
        else:
            logging.error(traceback.format_exc().replace('\n', ''))
            raise Exception("The data is not available at this moment.")
    finally:
        service.close()

    return result_from_cache


@retry_tag(2)
def FinancialStatementsGet(universe, trading_days, field):
    result_from_cache = {}
    try:
        service = __get_service()
        result_from_cache = service.get_financial_statement(
            universe,
            field,
            trading_days[0],
            trading_days[-1],
            get_principal_name()
        )

    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return result_from_cache

# ================== UNIVERSE FILTER APIS ==================


@retry_tag(2)
def get_untradable_dict(start, end, universes):
    """
    从CACHE数据库中获取交易日对应的不可交易股票字典
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
        universes (list of str): 股票池列表
    Returns:
        dict of str=>str: 交易日为key，value为该日未停牌的股票列表
    """
    try:
        service = __get_service()
        untradable_dict = service.get_untradable_dict(
            start, end, universes, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return untradable_dict


@retry_tag(2)
def get_nonhalt_dict(start, end, universes):
    """
    从CACHE数据库中获取交易日对应的未停牌股票字典
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
        universes (list of str): 股票池列表
    Returns:
        dict of str=>str: 交易日为key，value为该日未停牌的股票列表
    """
    secID_dict = None
    try:
        service = __get_service()
        secID_dict = service.get_nonhalt_dict(
            start, end, universes, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return secID_dict


@retry_tag(2)
def get_halt_dict(start, end, universes):
    """
    从CACHE数据库中获取交易日对应的停牌股票字典
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
        universes (list of str): 股票池列表
    Returns:
        dict of str=>str: 交易日为key，value为该日停牌的股票列表
    """
    secID_dict = None
    try:
        service = __get_service()
        secID_dict = service.get_halt_dict(
            start, end, universes, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return secID_dict


@retry_tag(2)
def filter_delisted_universes(end, universes):
    """
    从CACHE数据库中获取过滤掉在指定日期前退市的股票
    Args:
        end (str): 指定截止日期，必须是YYYYMMDD格式的字符串
        universes (list of str): 股票池列表
    Returns:
        list of str: 去掉了退市股票的列表
    """
    filtered_universe = []
    try:
        service = __get_service()
        filtered_universe = service.exclude_delist_tickers(
            end, universes, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return filtered_universe


def __ConvertFromDT2Str(tds_in_datetime):
    return {key.strftime('%Y%m%d'): val.strftime('%Y%m%d') for key, val in tds_in_datetime.iteritems()}


def __ConvertDT2StrOnKey(universe_dict):
    return {key.strftime('%Y%m%d'): list(val) for key, val in universe_dict.iteritems()}


def __ConvertRVInDT(result):
    return {datetime.strptime(key, '%Y%m%d'): set(val) for key, val in result.iteritems()}


@retry_tag(2)
def FilteredUniverseGet(factor, condition, lbound, ubound, trading_days_map, universe_dict):
    # todo: docstring need to finish
    """
    利用CACHE server对股票列表使用因子值进行条件过滤，过滤条件与univ_filter.Condition中结构对应
    Args:
        factor (str): 用户过滤的因子
        condition (str): condition类型
        lbound (float): 因子下界
        rbound (float): 因子上界
        trading_days_map:
        universe_dict:
    Returns:
        result_dict
    """

    result_dict = {}
    try:
        service = __get_service()
        func = getattr(service, FILTER_MAP[condition])
        result_dict = func(factor, lbound, ubound, __ConvertFromDT2Str(
            trading_days_map), __ConvertDT2StrOnKey(universe_dict), get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return __ConvertRVInDT(result_dict)


# =============== TRADING DAYS APIS ================
@retry_tag(2)
def get_td_from_cache(start, end):
    """
    从CACHE数据库中获取交易日列表
    Args:
        start: 查询开始时间，必须是YYYYMMDD格式的字符串
        end: 查询结束时间，必须是YYYYMMDD格式的字符串
    Returns:
        trading_days_str: 字符串格式的交易日列表
    """
    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_trading_days(
            start, end, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


@retry_tag(2)
def get_directed_td_list_from_cache(start, step, forward=True):
    """
    从CACHE数据库中获取某个起始日期至向后多个交易日的交易日列表
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        step (int): 从start开始的日期步长
        forward (boolean): True为向时间增长方向，Flase向时间减少方向
    Returns:
        list for str: 字符串格式的交易日列表，返回长度为step+1
    """
    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_directed_trading_day_list(start,
                                                                 step, forward, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


@retry_tag(2)
def get_directed_td_from_cache(start, step, forward=True):
    """
    从CACHE数据库中获取某个日期向后的第几个交易日
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        step (int): 从start开始的日期步长
        forward (boolean): True为向时间增长方向，Flase向时间减少方向
    Returns:
        str: 字符串格式的交易日，格式为YYYYMMDD
    """
    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_directed_one_trading_day(start,
                                                                step, forward, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


@retry_tag(2)
def get_week_first_tds(start, end):
    """
    获取每周第一个交易日
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
    Returns:
        list of str: 每周第一个交易日列表，格式为YYYYMMDD
    """
    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_week_start_day(
            start, end, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


@retry_tag(2)
def get_week_last_tds(start, end):
    """
    获取每周最后一个交易日
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
    Returns:
        list of str: 每周最后一个交易日列表，交易日为YYYYMMDD的字符串
    """
    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_week_last_day(
            start, end, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


@retry_tag(2)
def get_month_first_tds(start, end):
    """
    获取每月第一个交易日
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
    Returns:
        list of str: 每月第一个交易日列表，交易日为YYYYMMDD的字符串
    """
    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_month_start_day(
            start, end, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


@retry_tag(2)
def get_month_last_tds(start, end):
    """
    获取每月最后一个交易日
    Args:
        start (str): 查询开始时间，必须是YYYYMMDD格式的字符串
        end (str): 查询结束时间，必须是YYYYMMDD格式的字符串
    Returns:
        list of str: 每月最后一个交易日列表，交易日为YYYYMMDD的字符串
    """

    trading_days_str = []
    try:
        service = __get_service()
        trading_days_str = service.get_month_last_day(
            start, end, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return trading_days_str


# ============ futures renamed apis ============
@retry_tag(2)
def get_futures_base_info(tickers):
    return_data = pd.DataFrame()
    try:
        service = __get_service()
        values, indexes = service.get_future_base_info(
            tickers, get_principal_name())
        return_data = pd.DataFrame(values, index=indexes)
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return return_data


@retry_tag(2)
def get_futures_artificial_info(contract_ids, trading_days):
    return_data = dict()
    try:
        service = __get_service()
        data = service.get_aritificial_info_by_tdlist(
            trading_days, contract_ids, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    if data:
        for item in data:
            ticker = item.pop('_id')
            return_data[ticker] = pd.DataFrame(
                data=item).set_index('tradeDate')
    return return_data


@retry_tag(2)
def load_minute_bar_map(days, tickers, freq):
    minute_bar_map = {}
    try:
        service = __get_service()
        stock_tickers = filter(lambda x: len(
            re.findall(re.compile('\d'), x)) == 6, tickers)
        if stock_tickers:
            stock_minute_bars = EQUITY_MIN_BAR
        else:
            stock_minute_bars = []
        futures_tickers = filter(lambda x: len(x) <= 6, tickers)
        if futures_tickers:
            futures_minute_bars = service.get_future_min_bar(
                days, futures_tickers, get_principal_name())
        else:
            futures_minute_bars = dict()
        if stock_tickers or futures_tickers:
            for trade_date in days:
                minute_bars = list(set(futures_minute_bars.get(
                    trade_date, list())) | set(stock_minute_bars))
                minute_bars = sorted(
                    map(lambda minute_bar: str(minute_bar), minute_bars))
                minute_bars = filter(lambda minute_bar: minute_bar > '16:00',
                                     minute_bars) + \
                    filter(lambda minute_bar: minute_bar <=
                           '16:00', minute_bars)
                minute_bar_map[str(trade_date)] = minute_bars
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return minute_bar_map


@retry_tag(2)
def MktDailyFuturesDataGet(tickers, trading_days, field):
    return_data = dict()
    try:
        service = __get_service()
        return_data = service.get_future_daily_data_raw_by_tdlist(
            trading_days, tickers, get_principal_name(), list(set(field)))
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return return_data


@retry_tag(2)
def MktMinuteFuturesDataGet(tickers, trading_days, field, freq=1):
    return_data = dict()
    try:
        service = __get_service()
        data = service.get_future_min_data_by_tdlist(
            trading_days, tickers, get_principal_name(), list(set(field)), freq)
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    if data:
        for item in data:
            ticker = item.pop('_id')
            item['clearingDate'] = ['%s-%s-%s' %
                                    (dt[:4], dt[4:6], dt[6:]) for dt in item['clearingDate']]
            item['tradeTime'] = []
            for i in range(len(item['tradeDate'])):
                trade_date_with_bars = []
                for j in range(len(item['tradeDate'][i])):
                    dt = item['tradeDate'][i][j]
                    item['tradeDate'][i][j] = '%s-%s-%s' % (
                        dt[:4], dt[4:6], dt[6:])
                    trade_date_with_bars.append(
                        item['tradeDate'][i][j] + ' ' + item['barTime'][i][j])
                item['tradeTime'].append(trade_date_with_bars)
            return_data[ticker] = item
    return return_data

# @retry_tag(2)
# def MktMinuteFuturesDataGet(tickers, start, end, field):
#     return_data = dict()
#     try:
#         service = __get_service()
#         return_data = service.get_future_min_data_raw(start, end, tickers, get_principal_name(), list(set(field)))
#     except:
#         logging.error(traceback.format_exc().replace('\n', ''))
#         raise Exception("The data is not available at this moment.")
#     finally:
#         service.close()
# #     if data:
# #         for item in data:
# #             ticker = item.pop('_id')
# #             item['clearingDate'] = ['%s-%s-%s' % (dt[:4], dt[4:6], dt[6:]) for dt in item['clearingDate']]
# #             item['tradeTime'] = []
# #             for i in range(len(item['tradeDate'])):
# #                 trade_date_with_bars = []
# #                 for j in range(len(item['tradeDate'][i])):
# #                     dt = item['tradeDate'][i][j]
# #                     item['tradeDate'][i][j] = '%s-%s-%s' % (dt[:4], dt[4:6], dt[6:])
# #                     trade_date_with_bars.append(item['tradeDate'][i][j] + ' ' + item['barTime'][i][j])
# #                 item['tradeTime'].append(trade_date_with_bars)
# #             return_data[ticker] = item
#     return return_data


@retry_tag(2)
def MktFutureBaseInfo(tickers):
    return_data = pd.DataFrame()
    try:
        service = __get_service()
        values, indexes = service.get_future_base_info(
            tickers, get_principal_name())
        return_data = pd.DataFrame(values, index=indexes)
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return return_data


@retry_tag(2)
def MktFutureArtificialInfo(trading_days, contract_objects):
    return_data = dict()
    try:
        service = __get_service()
        data = service.get_aritificial_info_by_tdlist(
            trading_days, contract_objects, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    if data:
        for item in data:
            # try:
            ticker = item.pop('_id')
            # item['tradeDate'] = map(lambda x:str(x), item['tradeDate'])
            return_data[ticker] = pd.DataFrame(
                data=item, index=item['tradeDate'])
            # except:
            #     logging.info('error {} '.format(ticker))
    return return_data


@retry_tag(2)
def MktTradingDays(start, end):
    data = []
    try:
        service = __get_service()
        data = service.get_future_trading_days(
            start, end, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def MktDirectTradingDays(day, step):
    data = []
    try:
        service = __get_service()
        data = service.get_directed_future_trading_day_list(
            day, step, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def StocksGet():
    data = []
    try:
        service = __get_service()
        data = service.get_stocks(get_principal_name())
    except Exception as e:
        logging.exception(e)
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def FundsGet():
    data = []
    try:
        service = __get_service()
        data = service.get_funds(get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def IndexesGet():
    data = []
    try:
        service = __get_service()
        data = service.get_indexes(get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def FuturesGet():
    data = []
    try:
        service = __get_service()
        data = service.get_futures(get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def StockFundTDatesGet(symbols):
    data = dict()
    try:
        service = __get_service()
        data = service.get_stock_fund_tdates(symbols, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


@retry_tag(2)
def FutureTDatesGet(symbols):
    data = dict()
    try:
        service = __get_service()
        data = service.get_future_tdates(symbols, get_principal_name())
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
        raise Exception("The data is not available at this moment.")
    finally:
        service.close()
    return data


def HelloUser(params_dict):
    try:
        service = __get_service()
        params_dict.update({'get_principal_name()': get_principal_name()})
        service.hello_user(params_dict)
    except:
        logging.error(traceback.format_exc().replace('\n', ''))
    finally:
        service.close()
