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

"""
market_loader.py

benchmark, stock, fund with new caching scheme

@author: yudi.wu
"""

import datetime

import numpy as np
import pandas as pd

from ..utils.common import find_first_digit
from ...api_base import is_enterprise_user
from . apiconfig import (
    BATCH_DAILY_DATA_SIZE,
    BATCH_INTRADAY_DATA_SIZE,
    MAX_CACHEAPI_THREAD_AMOUNT,
    BATCH_FINANCIAL_STATEMENTS_SIZE
)
from . cache_api import (
    MktDailyDataFrameGet,
    MktIntradayDataFrameGet,
    MktDailyFuturesDataGet,
    MktMinuteFuturesDataGet,
    FinancialStatementsGet,
    INTRADAY_COLS, DAILY_COLS
)
from .. const import (
    FUTURES_DAILY_FIELDS,
    FUTURES_MINUTE_FIELDS,
    FUTURES_SPECIAL,
    FUTURES_ARTIFICIAL
)


def _wrap_sec_data(data, trade_dates, target_trade_dates_idx, fill_content=0.0):
    # 做数据的前后填充
    expected_len = len(target_trade_dates_idx)
    if len(data) == 0:
        return [fill_content] * expected_len
    elif len(trade_dates) == expected_len:
        return data
    else:
        result = [fill_content] * target_trade_dates_idx[str(trade_dates[0])] + data + \
                 [fill_content] * \
            (expected_len - target_trade_dates_idx[str(trade_dates[-1])] - 1)
        return result


def load_daily_equity_data(universe=None, trading_days=None, field=DAILY_COLS, freq='d'):
    """
    从Mercury Cache中并发获取证券的日线行情数据
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
        >> equity_data = load_daily_equity_data(universe, trading_days, ['closePrice', 'preClosePrice'])

    """

    universe = list(universe)
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
    trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
    T = len(trading_days)
    S = len(universe)

    # grouping for gevent, lower bound is 20 trading days
    if is_enterprise_user():
        year_days_dict = dict()
        for day in trading_days:
            year = day[:4]
            if year not in year_days_dict:
                year_days_dict[year] = []
            year_days_dict[year].append(day)
        batches = year_days_dict.values()

        def gload(idx, bat):
            mkt_data = MktDailyDataFrameGet(
                universe=universe, trading_days=bat, field=field)
            return idx, mkt_data

        from gevent.pool import Pool
        pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
        requests = [pool.spawn(gload, idx, bat)
                    for (idx, bat) in enumerate(batches)]

        pool.join()

        data_all = {var: {} for var in field}
        df_index = list()
        # trading_days_idx = {td: idx for (idx, td) in enumerate(trading_days)}
        for response in sorted(requests, key=lambda x: x.value[0]):
            i, data = response.value
            df_index.extend(batches[i])
            trading_days_idx = {td: idx for (idx, td) in enumerate(batches[i])}
            for var in data_all:
                for sec in data[var]:
                    tmp = _wrap_sec_data(data[var][sec], data['tradeDate'][sec], trading_days_idx, float('nan'))
                    if sec in data_all[var]:
                        data_all[var][sec].extend(tmp)
                    else:
                        data_all[var][sec] = tmp

        nan_column = [float('nan')] * T
        for var, values in data_all.iteritems():
            for sec in set(universe) - set(data_all[var].keys()):
                values[sec] = nan_column
            data_all[var] = pd.DataFrame(values, index=df_index, columns=universe)
    else:
        N = max(20, BATCH_DAILY_DATA_SIZE // T)
        batches = [universe[i:min(i + N, S)] for i in range(0, S, N)]

        def gload(idx, bat):
            mkt_data = MktDailyDataFrameGet(
                universe=bat, trading_days=trading_days, field=field)
            return idx, mkt_data

        from gevent.pool import Pool
        pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
        requests = [pool.spawn(gload, idx, bat)
                    for (idx, bat) in enumerate(batches)]

        pool.join()

        data_all = {var: {} for var in field}
        trading_days_idx = {td: idx for (idx, td) in enumerate(trading_days)}
        for response in sorted(requests, key=lambda x: x.value[0]):
            _, data = response.value
            for var in data_all:
                for sec in data[var]:
                    data_all[var][sec] = _wrap_sec_data(
                        data[var][sec], data['tradeDate'][sec], trading_days_idx, float('nan'))
        nan_column = [float('nan')] * T
        for var, values in data_all.iteritems():
            for sec in set(universe) - set(data_all[var].keys()):
                values[sec] = nan_column
            data_all[var] = pd.DataFrame(
                values, index=trading_days_index, columns=universe)
    return data_all


def load_financial_statements(universes, trading_days, fields):
    # 去除universe中的指数
    new_universe = []
    for stk in universes:
        if stk[-4:] in ['XSHE', 'XSHG']:
            new_universe.append(stk)
    # universe = new_universe
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
    trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
    all_days = [x.strftime('%Y%m%d') for x in list(
        pd.date_range(start=trading_days[0], end=trading_days[-1]))]
    T = len(trading_days)
    S = len(new_universe)
    F = len(fields)

    # grouping for gevent, lower bound is 20 trading days
    N = max(50, BATCH_FINANCIAL_STATEMENTS_SIZE // (T * F))
    batches = [new_universe[i:min(i + N, S)] for i in range(0, S, N)]

    def gload(idx, bat):
        mkt_data = FinancialStatementsGet(
            universe=bat, trading_days=trading_days, field=list(fields))
        return idx, mkt_data

    from gevent.pool import Pool
    pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
    requests = [pool.spawn(gload, idx, bat)
                for (idx, bat) in enumerate(batches)]
    pool.join()

    data_all = {var: {} for var in fields}

    for response in sorted(requests, key=lambda x: x.value[0]):
        _, data = response.value
        for var in data_all:
            for sec in data[var]:
                data_all[var][sec] = data[var][sec]
    nan_column = [float('nan')] * T
    for var, values in data_all.iteritems():
        for sec in set(universes) - set(data_all[var].keys()):
            values[sec] = nan_column
        # 先用all_days,因为财报发布时间有可能是节假日，如果直接用交易日做index，则节假日的财报会被跳过
        temp = pd.DataFrame(
            values, index=all_days, columns=universes).fillna(method='pad')
        data_all[var] = temp.loc[trading_days]
        data_all[var].index = trading_days_index
    return data_all


def load_intraday_equity_data(universe=None, trading_days=None, field=INTRADAY_COLS, freq='1m'):
    """
    从Mercury Cache获得证券的分钟线行情数据

    从CACHE数据库里取A股、基金、指数的分钟线数据
    可获取的数据有： 收盘价(closePrice), 最高价(highPrice), 最低价(lowPrice), 开盘价(openPrice), 换手量(turnoverVol), 换手率(turnoverValue)

    Args:
        universe (list of str): 证券代码列表，支持A股和开放式基金，必须包含后缀，其中上证证券为.XSHG，深证证券为.XSHE
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的数据字段名称
    Returns:
        dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = set_universe('A')
        >> trading_days = get_trading_days()
        >> intraday_prices = load_intraday_equity_data(universe, trading_days, ['closePrice', 'openPrice'])
    """

    universe = list(universe)
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
    trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
    T = len(trading_days)
    S = len(universe)

    # grouping for gevent, lower bound is 5 trading days
    # N = max(1, BATCH_INTRADAY_DATA_SIZE // S)
    # batches = [trading_days[i:min(i+N, T)] for i in range(0, T, N)]
    N = max(1, BATCH_INTRADAY_DATA_SIZE // T)
    batches = [universe[i:min(i + N, S)] for i in range(0, S, N)]

    def gload(idx, bat):
        mkt_data = MktIntradayDataFrameGet(universe=bat, trading_days=trading_days,
                                           field=field, freq=freq)
        return idx, mkt_data

    from gevent.pool import Pool
    pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
    requests = [pool.spawn(gload, idx, bat)
                for (idx, bat) in enumerate(batches)]
    pool.join()

    if freq in ['m', '1m']:
        data_len = 241
    elif freq == '5m':
        data_len = 49
    elif freq == '15m':
        data_len = 17
    elif freq == '30m':
        data_len = 9
    elif freq == '60m':
        data_len = 5
    data_all = {var: {} for var in field}
    nan_items = np.array([float('nan')] * data_len)
    nans = [nan_items for _ in xrange(T)]
    trading_days_idx = {td: idx for (idx, td) in enumerate(trading_days)}
    for response in sorted(requests, key=lambda x: x.value[0]):
        _, data = response.value
        # 有些股票在这段期间内没有上市，所以取不出数据，但是依然需要补齐
        for var in data_all:
            for sec in data[var]:
                data_all[var][sec] = _wrap_sec_data(data[var][sec], data['tradeDate'][sec],
                                                    trading_days_idx, nan_items)
    for var, values in data_all.iteritems():
        for sec in set(universe) - set(data_all[var].keys()):
            values[sec] = nans
        data_all[var] = pd.DataFrame(
            values, index=trading_days_index, columns=universe)
    return data_all


def load_daily_futures_data(universe=None, trading_days=None, field=FUTURES_DAILY_FIELDS, freq='1d'):
    """
    从Mercury Cache中并发获取期货的日线行情数据
    可获取的数据有：收盘价(closePrice), 最高价(highPrice), 最低价(lowPrice), 开盘价(openPrice), 换手量(turnoverVol), 开仓费率(openInterest), 交割价格(settlementPrice)

    Args:
        universe (list of str): 期货池表
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的数据字段名称
    Returns:
        dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = ['IF1601']
        >> trading_days = get_trading_days()
        >> equity_data = load_daily_futures_data(universe, trading_days, ['closePrice'])

    """

    universe = list(universe)
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
    trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
    T = len(trading_days)
    S = len(universe)

    N = max(20, BATCH_DAILY_DATA_SIZE // T)
    batches = [universe[i:min(i + N, S)] for i in range(0, S, N)]

    def gload(idx, bat):
        mkt_data = MktDailyFuturesDataGet(
            tickers=bat, trading_days=trading_days, field=field)
        return idx, mkt_data

    from gevent.pool import Pool
    pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
    requests = [pool.spawn(gload, idx, bat)
                for (idx, bat) in enumerate(batches)]
    pool.join()

    data_all = {var: {} for var in field}
    trading_days_idx = {td: idx for (idx, td) in enumerate(trading_days)}
    for response in sorted(requests, key=lambda x: x.value[0]):
        _, data = response.value
        for var in data_all:
            for sec in data[var]:
                data_all[var][sec] = _wrap_sec_data(data[var][sec],
                                                    data['tradeDate'][sec],
                                                    trading_days_idx, float('nan'))

    nan_column = [float('nan')] * T
    # 期货有些合约存在段时间所有合约退市的情况
    warn_info_dict = dict()
    for var, values in data_all.iteritems():
        for sec in set(universe) - set(data_all[var].keys()):
            values[sec] = nan_column
        df_list = list()
        for sec in values:
            db_tds = data_all['tradeDate'][sec]
            if len(db_tds) != len(trading_days_index):
                if (sec[-2:] in FUTURES_ARTIFICIAL and sec[:-2] in FUTURES_SPECIAL) \
                        or (sec[:find_first_digit(sec) in FUTURES_SPECIAL]):
                    warn_info_dict[sec[:-2]] = FUTURES_SPECIAL[sec[:-2]]
                missing_days = list()
                index_tds = list()
                tmp = sorted(list(set(db_tds)))
                if isinstance(tmp[0], float) and np.isnan(tmp[0]):
                    tmp.remove(tmp[0])
                for td in trading_days_index:
                    td_str = str(td).replace('-', '')
                    if td_str >= min(tmp) and td_str not in tmp:
                        missing_days.append(td)
                    else:
                        index_tds.append(td)
                missing_days = sorted(missing_days)
                index_tds = sorted(index_tds)
                missing_df = pd.DataFrame(index=missing_days)
                data_df = pd.DataFrame({sec: values[sec]}, index=index_tds, columns=[sec])
                df = pd.concat([data_df, missing_df]).sort_index()
            else:
                df = pd.DataFrame({sec: values[sec]}, index=trading_days_index, columns=[sec])
            df_list.append(df)
        if var == 'tradeDate':
            trade_date_df = pd.concat(df_list, axis=1)
        else:
            data_all[var] = pd.concat(df_list, axis=1)
    if 'tradeDate' in data_all:
        data_all['tradeDate'] = trade_date_df
    for item in warn_info_dict:
        print(u'合约标的%s在%s到%s处于非上市状态，已使用空值填充' %
              (item, warn_info_dict[item]['start'], warn_info_dict[item]['end']))
    return data_all


def load_minute_futures_data(universe=None, trading_days=None, field=FUTURES_MINUTE_FIELDS, freq='1m'):
    """
    从Mercury Cache中并发获取期货的分钟线行情数据
    可获取的数据有：收盘价(closePrice), 最高价(highPrice), 最低价(lowPrice), 开盘价(openPrice), 换手量(turnoverVol), 结算日(clearningDate), 分钟线时间戳(barTime), 交易日(tradeDate)

    Args:
        universe (list of str): 期货池表
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的数据字段名称
    Returns:
        dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = ['IF1601']
        >> trading_days = get_trading_days()
        >> equity_data = load_minute_futures_data(universe, trading_days, ['closePrice'])

    """

    universe = list(universe)
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
    trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
    T = len(trading_days)
    S = len(universe)

    N = max(1, BATCH_INTRADAY_DATA_SIZE // T)
    batches = [universe[i:min(i + N, S)] for i in range(0, S, N)]

    def gload(idx, bat):
        mkt_data = MktMinuteFuturesDataGet(
            tickers=bat, trading_days=trading_days, field=field, freq=freq)
        return idx, mkt_data

    from gevent.pool import Pool
    pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
    requests = [pool.spawn(gload, idx, bat)
                for (idx, bat) in enumerate(batches)]
    pool.join()

    data_all = {}
    zero_item = []
    zeros = [zero_item for _ in xrange(T)]
    for response in sorted(requests, key=lambda x: x.value[0]):
        _, data = response.value
        data_all.update(data)
    data_all = {key: pd.DataFrame.from_dict(item).set_index('clearingDate', drop=False)
                for (key, item) in data_all.iteritems()}
    # 滚动加载是需要数据为dict
    data_all = dict(pd.Panel.from_dict(data_all).swapaxes(0, 2))
    for var, values in data_all.iteritems():
        for sec in set(universe) - set(data_all[var].keys()):
            values[sec] = zeros
        data_all[var] = pd.DataFrame(
            values, index=trading_days_index, columns=universe)
    return data_all


# def load_minute_futures_data(universe=None, trading_days=None, field=FUTURES_MINUTE_FIELDS):
#     """
#     从Mercury Cache中并发获取期货的分钟线行情数据
#     可获取的数据有：收盘价(closePrice), 最高价(highPrice), 最低价(lowPrice), 开盘价(openPrice), 换手量(turnoverVol), 结算日(clearningDate), 分钟线时间戳(barTime), 交易日(tradeDate)
#
#     Args:
#         universe (list of str): 期货池表
#         trading_days (list of datetime): 交易日列表
#         field (list of string): 需要获取的数据字段名称
#     Returns:
#         dict of str=>DataFrame: key值为字段名称，value为该字段日线数据(DataFrame, column为股票ID, index为交易日[YYYYMMDD])的dict
#     Examples:
#         >> universe = ['IF1601']
#         >> trading_days = get_trading_days()
#         >> equity_data = load_minute_futures_data(universe, trading_days, ['closePrice'])
#
#     """
#
#     universe = list(universe)
#     trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
#     trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
#     T = len(trading_days)
#     S = len(universe)
#
#     N = max(1, BATCH_INTRADAY_DATA_SIZE // T)
#     batches = [universe[i:min(i+N, S)] for i in range(0, S, N)]
#
#     def gload(idx, bat):
#         mkt_data = MktMinuteFuturesDataGet(
#             tickers=bat, start=trading_days[0], end=trading_days[-1], field=field)
#         return idx, mkt_data
#
#     pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
#     requests = [pool.spawn(gload, idx, bat) for (idx, bat) in enumerate(batches)]
#     pool.join()
#
#     data_all = {var: {} for var in field}
#     # 期货分钟线当没有行情的时候无法补充
# #     nan_items = []
# #     nans = [nan_items for _ in xrange(T)]
# #     trading_days_idx = {td: idx for (idx, td) in enumerate(trading_days)}
#     for response in sorted(requests, key=lambda x: x.value[0]):
#         _, data = response.value
#         for var in data_all:
#             data_all[var] = pd.DataFrame(data[var], index=trading_days_index, columns=universe)
# #             for sec in data[var]:
# #                 data_all[var][sec] = _wrap_sec_data(data[var][sec], data['clearingDate'][sec], trading_days_idx, nan_items)
#
# #     for var, values in data_all.iteritems():
# #         # 填充完全没有数据的期货合约，不应该发生
# #         for sec in set(universe) - set(data_all[var].keys()):
# #             values[sec] = nans
# #         data_all[var] = pd.DataFrame(values, index=trading_days_index, columns=universe)
#
#     if 'tradeTime' in field:
#         if 'barTime' in data_all and 'tradeDate' in data_all:
#             for i in range(len(data_all['tradeDate'])):
#                 trade_date_with_bars = []
#                 for j in range(len(data_all['barTime'][i])):
#                     dt = item['tradeDate'][i][j]
#                     item['tradeDate'][i][j] = '%s-%s-%s' % (dt[:4], dt[4:6], dt[6:])
#                 trade_date_with_bars.append(item['tradeDate'][i][j] + ' ' + item['barTime'][i][j])
#         minutes = EQUITY_MIN_BAR
#         ttimes = [np.array([td + ' ' + m for m in minutes]) for td in minute_data[checked_field].index]
#         minute_data['tradeTime'] = pd.DataFrame({stk: ttimes for stk in minute_data[checked_field].columns},
#                                                 index=minute_data[checked_field].index)
#
#     print data_all
#     return data_all
