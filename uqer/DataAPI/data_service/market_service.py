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

import re
import logging
import pandas as pd
import numpy as np
import datetime
import copy
import bisect
from . loader import (
    load_daily_equity_data,
    load_intraday_equity_data,
    load_common_factor_data,
    load_daily_futures_data,
    load_minute_futures_data,
    load_financial_statements
)
from . loader.cache_api import load_minute_bar_map
from . const import (
    FUTURES_DAILY_FIELDS,
    STOCK_ADJ_FIELDS,
    FUTURES_MINUTE_FIELDS,
    EQUITY_DAILY_FIELDS,
    EQUITY_MINUTE_FIELDS,
    EQUITY_MIN_BAR,
    EQUITY_5MIN_BAR,
    EQUITY_15MIN_BAR,
    EQUITY_30MIN_BAR,
    EQUITY_60MIN_BAR,
    ALIAS_DAILY_PRICE,
    ALIAS_MINUTE_PRICE,
)
from . utils.datetime_utils import (
    previous_trading_day,
)

from . asset_service import AssetService


def _stylish(raw_data_dict, symbols, time_bars, fields, style, rtype='frame'):
    """
    将raw_data_dict按照style和rtype转化成对应的格式，其中raw_data_dict为满足ast格式的dict

    Args:
        raw_data_dict(dict of ndarray, 'ast' style):  需要转化的原始数据，一般为MarketData.slice返回数据，样式为ast
        symbols(list of str): raw_data_dict中包含的symbol列表，需要与ndarray中colume对应
        time_bars(list of str): raw_data_dict中包含的time_bars列表，需要与ndarray中的index对应
        fields(list of str): raw_data_dict中包含的attributes列表，与其key值对应
        style('tas'/'ast'/'sat'): 需要转化为的目标样式
        rtype('frame'/'dict'): 需要转化为的目标格式，dict或者DataFrame

    Returns:
        dict or frame：将raw_data_dict转化完成后，满足style样式的rtype类型的数据结构
    """
    if style == 'ast':
        history_data = {}
        for attribute in fields:
            if rtype == 'frame':
                history_data[attribute] = pd.DataFrame(data=raw_data_dict[
                                                       attribute] if attribute in raw_data_dict else dict(), columns=symbols, index=time_bars)
            if rtype == 'dict':
                history_data[attribute] = {s: raw_data_dict[attribute][:, i] for (
                    i, s) in enumerate(symbols)} if attribute in raw_data_dict else dict()
                history_data[attribute]['time'] = np.array(time_bars)
    # sat+dict也是分钟线默认的切割方式
    elif style == 'sat':
        history_data = {}
        for idx, symbol in enumerate(symbols):
            if rtype == 'frame':
                history_data[symbol] = pd.DataFrame(data={a: raw_data_dict[a][
                                                    :, idx] for a in fields if a in raw_data_dict}, index=time_bars, columns=fields)
            if rtype == 'dict':
                history_data[symbol] = {
                    a: raw_data_dict[a][:, idx] for a in fields if a in raw_data_dict}
                history_data[symbol]['time'] = np.array(time_bars)
    elif style == 'tas':
        history_data = {}
        for idx, trade_date in enumerate(time_bars):
            if rtype == 'frame':
                history_data[trade_date] = pd.DataFrame(data={a: raw_data_dict[a][idx, :] for a in fields if a in raw_data_dict},
                                                        index=symbols, columns=fields)
            if rtype == 'dict':
                history_data[trade_date] = {
                    a: raw_data_dict[a][idx, :] for a in fields}
                history_data[trade_date]['symbol'] = np.array(symbols)
    else:
        raise ValueError('Exception in "MarketService._ast_stylish": '
                         'history style \'%s\' is not supported here, please refer to document for details' % style)
    return history_data


def _ast_slice(raw_data_dict, symbols, end_time_str, fields, start_time_str=None,
               time_range=None, **options):
    """
    函数未实现随意切割功能。对raw_data_dict进行slice操作，其中raw_data_dict为满足ast结构的dict，其中time_range和start_time_str必须有一个有值

    Args:
        raw_data_dict(dict of DataFrame, ast style): 需要进行slice的原始数据
        symbols(list of str): 需要slice出的符号数据
        end_time_str(date formatted str): slice出数据的截止时间，日线数据格式为'YYYYmmdd'，分钟线数据格式为'YYYYmmdd HH:MM'
        fields(list of str): 需要slice出的字段列表
        start_time_str(date formatted str or None): slice出数据的开始时间，日线数据格式为'YYYYmmdd'，分钟线数据格式为'YYYmmdd HH:MM'，该字段和time_range必须有一个不为空
        check_attribute(str): 用于检查raw_data_dict是否为空的字段，raw_data_dict不含有该字段，则表示数据为空
        time_range(int or None): 从end_time_str向前slice时间长度
    """

    result = {}
    for attribute in fields:
        # 切分的时候要对raw_data_dict 补全
        attribute_df = raw_data_dict[attribute]
        for s in symbols:
            if s not in attribute_df.columns:
                attribute_df[s] = float('nan')
        # 然后切分
        df_matrix = attribute_df.as_matrix()
        symbol_idxs = [
            raw_data_dict[attribute].columns.get_loc(s) for s in symbols if s in raw_data_dict[attribute].columns]

        result[attribute] = df_matrix[:, symbol_idxs]
    return result


def _rolling_load_data(data, trading_days, universe, max_cache_days, data_load_func, fields, freq):
    """
    加载trading_days对应的行情数据，其中data中已有数据不做从重新加载

    Args:
        data(dict of dict): 原有数据，其中含有的trading_days数据不会做重新加载
        trading_days(list of datetime): 需要滚动加载数据的交易日列表
        universe(list of str): 需要滚动加载的股票池，必须与data中的universe保持一致
        max_cache_days(int or None): 需要保留的data中原有数据的长度，如果为None则表示保留所有原有数据
        data_load_func(func: universe, trading_days, fields => dict of dict): 数据加载函数
        fields(list of str): 需要加载的数据字段

    Returns:
        dict of DataFrame, ast style: 滚动加载之后新的数据内容
    """
    data = copy.copy(data)
    if len(data) == 0:
        trading_days_in_loaded = []
    else:
        trading_days_in_loaded = [
            datetime.datetime.strptime(t, '%Y-%m-%d') for t in data['tradeDate'].index]
    target_days = sorted(set(trading_days_in_loaded) | set(trading_days))
    if max_cache_days is not None:
        target_days = target_days[-max_cache_days:]
    to_reserve_days = sorted(set(trading_days_in_loaded) & set(target_days))
    to_load_trading_days = sorted(set(target_days) - set(to_reserve_days))
    if len(to_load_trading_days) == 0:
        return data
    new_data = data_load_func(
        universe, to_load_trading_days, fields, freq=freq)
    # 修改了如下行为，不去遍历field，而是遍历取出数据中的key
    if len(data) == 0 or len(to_reserve_days) == 0:
        for var in new_data:
            data[var] = new_data[var].sort_index()
    else:
        for var in new_data:
            to_reserve_tdays = [
                t.strftime('%Y-%m-%d') for t in to_reserve_days]
            data[var] = pd.concat(
                [data[var].loc[to_reserve_tdays], new_data[var]], axis=0).sort_index()
    return data


def _uncompress_minute_bars(minute_bars, columns, index_field, index_series=None):
    """
    展开压缩的分钟线数据，要求该分钟线数据必须在时间上可对齐
    """
    result_dict = {}
    for column in columns:
        result_dict[column] = np.concatenate(minute_bars[column].as_matrix())
    result_df = pd.DataFrame(result_dict)
    if index_series is not None:
        result_df[index_field] = pd.Series(index_series, name=index_field)
    return result_df.set_index(index_field)


def _concat_data(data_list, rtype='frame', axis=0):
    """
    对dict或dataframe数据进行拼装的共用方法

    Args:
        data_list(list of dict of dict): 需要进行拼装的数据
        rtype(dict or frame): 原始数据类型
        axis(0 or 1): 0表示row拼装，1表示column拼装

    Returns:
        dict of dict or dict of DataFrame
    """
    data_list = [d for d in data_list if d is not None]
    if rtype == 'frame':
        return pd.concat(data_list, axis=axis)
    elif rtype == 'dict':
        result = {}
        if axis == 1:
            for data in data_list:
                result.update(data)
        if axis == 0:
            for data in data_list:
                for key, value in data.iteritems():
                    result.setdefault(key, [])
                    result[key].append(value)
            for key, value in result.iteritems():
                result[key] = np.concatenate(value)
        return result


def _append_data(raw_data, sliced_data, style, rtype='frame'):
    """
    将slice并stylish之后的数据进行组合拼装

    Args:
        raw_data(dict of DataFrame or dict of dict): 需要进行拼装数据的原始数据，格式和style及rtype对应
        sliced_data(dict of DataFrame or dict of dict): 需要进行拼装数据的新数据，格式和raw_data必须保持一致
        style(ast or sat or tas): 拼装数据的数据格式
        rtype(frame or dict): 拼装数据的数据类型

    Returns:
        dict of dict or dict of DataFrame
    """
    result = {}
    if style == 'ast':
        for attribute in set(raw_data.keys()) | set(sliced_data.keys()):
            a_data = _concat_data([raw_data.get(attribute, None), sliced_data.get(
                attribute, None)], axis=1, rtype=rtype)
            result[attribute] = a_data
    if style == 'sat':
        result.update(raw_data)
        result.update(sliced_data)
    if style == 'tas':
        for tdays in set(raw_data.keys()) | set(sliced_data.keys()):
            t_data = _concat_data(
                [raw_data.get(tdays), sliced_data.get(tdays)], axis=0, rtype=rtype)
            result[tdays] = t_data
    return result


def tas_data_tick_expand(data, fields=['barTime', 'closePrice'], tick_time_field='barTime'):
    """
    返回展开的tas分钟线数据

    Args:
        data(DataFrame): 压缩好的分钟线数据
        fields(list of attribute): 如['highPrice', 'closePrice']
        tick_time_field(str): data中的分钟列名，不建议修改

    Returns:
        dict of dict，key为分钟时点，value如{'RM701':('09:01', 2287.0, 2286.0, 2289.0, 2283.0, 656.0)}
    """
    minute_ticks = {}
    data = data.dropna()
    for stk in data.index:
        for item in zip(*[data.at[stk, field] for field in [tick_time_field] + fields]):
            ttime = item[0]
            minute_ticks.setdefault(ttime, {})
            minute_ticks[ttime][stk] = item[1:]
    return minute_ticks


class MarketService(object):
    """
    行情数据服务类
    * market_data_list: 含各AssetType的MarketData的集合
    * minute_bar_map: 含分钟线行情时的每个交易日bar_time
    * universe_service: UniverseService
    """

    def __init__(self):
        self.stock_market_data = None
        self.futures_market_data = None
        self.fund_market_data = None
        self.index_market_data = None
        self.market_data_list = []
        self.universe = None
        self.minute_bar_map = None
        self._available_daily_fields = None
        self._available_minute_fields = None

    @staticmethod
    def create_with_service(universe, mkt_daily_field=[],
                            mkt_minute_field=[], stock_factors=[], fs_field=[], adj=True, **kwargs):
        """
        通过静态方法创建MarketService实例，market_data_list中含asset_service中各类资产的MarketData

        Args:
            asset_service: AssetService
            universe_service: UniverseService
            stock_factors: 可传入非equity_daily及fq因子外的其他因子

        Returns:
            MarketService
        """
        mkt_service = MarketService()
        mkt_service.universe = universe
        stock_universe = AssetService.findout_stocks(universe)
        # 定义股票结构
        if len(stock_universe) > 0:
            mkt_service.stock_market_data = StockMarketData(stock_universe,
                                                            list(
                                                                set(mkt_daily_field) & (set(EQUITY_DAILY_FIELDS) | set(ALIAS_DAILY_PRICE))),
                                                            list(
                                                                set(mkt_minute_field) & (set(EQUITY_MINUTE_FIELDS) | set(ALIAS_MINUTE_PRICE))),
                                                            stock_factors,
                                                            fs_field,
                                                            adj=adj,
                                                            **kwargs)
            mkt_service.market_data_list.append(mkt_service.stock_market_data)

        # 定义期货结构
        futures_universe = AssetService.findout_futures(universe)
        if len(futures_universe) > 0:
            mkt_service.futures_market_data = FuturesMarketData(futures_universe,
                                                                list(set(mkt_daily_field) & (set(FUTURES_DAILY_FIELDS) | set(
                                                                    ALIAS_DAILY_PRICE) - set(['preClose', 'preCloseIndex']))),
                                                                list(set(mkt_minute_field) & (set(FUTURES_MINUTE_FIELDS) | set(ALIAS_MINUTE_PRICE))))
            mkt_service.market_data_list.append(
                mkt_service.futures_market_data)
        # 定义指数结构
        index_universe = AssetService.findout_indexes(universe)

        if len(index_universe) > 0:
            mkt_service.index_market_data = IndexMarketData(index_universe,
                                                            list(
                                                                set(mkt_daily_field) & (set(EQUITY_DAILY_FIELDS) | set(ALIAS_DAILY_PRICE))),
                                                            list(set(mkt_minute_field) & (set(EQUITY_MINUTE_FIELDS) | set(ALIAS_MINUTE_PRICE))))
            mkt_service.market_data_list.append(mkt_service.index_market_data)
        # 定义基金结构
        fund_universe = AssetService.findout_funds(universe)
        if len(fund_universe) > 0:
            mkt_service.fund_market_data = FundMarketData(fund_universe,
                                                          list(
                                                              set(mkt_daily_field) & (set(EQUITY_DAILY_FIELDS) | set(ALIAS_DAILY_PRICE))),
                                                          list(
                                                              set(mkt_minute_field) & (set(EQUITY_MINUTE_FIELDS) | set(ALIAS_MINUTE_PRICE))),
                                                          adj=adj)
            mkt_service.market_data_list.append(mkt_service.fund_market_data)
        return mkt_service

    def slice(self, symbols, fields, end_date, freq='d', time_range=1, style='ast', rtype='frame', start_date=None,
              **options):
        """
        依次对market_data_list各项进行slice

        Args:
            symbols(list of symbol): 对universe中特定symbol的列表进行slice
            fields(list of str): 返回***_bars行情中所选择字段
            end_date: slice截止日期
            freq: 'd' or 'm'
            time_range(int): end_date往前交易日天数
            style: 'ast', 'sat' or 'tas', 默认'ast'
            rtype: 默认'frame'(dict of DataFrame) or 'dict'(dict of dict)

        Returns:
            dict of dict: 格式视style与rtype参数输入
        """
        result = {}
        if symbols == 'all':
            symbols = list(self.universe)
        for market_data in self.market_data_list:
            result = _append_data(result,
                                  market_data.slice(symbols, fields, end_date, freq=freq, style=style,
                                                    time_range=time_range, rtype=rtype, start_date=start_date,
                                                    **options),
                                  style, rtype=rtype)
        return result

    def batch_load_daily_data(self, trading_days):
        """
        批量加载日线数据

        Args:
            trading_days(list of datetime): 批量加载日线的具体交易日列表
        """
        self.rolling_load_daily_data(trading_days)

    def rolling_load_daily_data(self, trading_days, max_cache_days=None):
        """
        依次对market_data_list中各项MarketData进行日行情加载。

        Args:
            trading_days(list of datetime): backtest时所传入含max_window_history
            max_cache_days(int): market_data_list中daily_bars最大载入天数
        """
        for market_data in self.market_data_list:
            if market_data is not None:
                market_data.rolling_load_daily_data(
                    trading_days, max_cache_days)

    def rolling_load_minute_data(self, trading_days, max_cache_days=5, freq='1m'):
        """
        依次对market_data_list中各项MarketData进行分钟线行情加载。
        Args:
            trading_days(list of datetime): 批量加载日线的具体交易日列表
            max_cache_days(int): 最大保留的分钟线天数
        """
        for market_data in self.market_data_list:
            if market_data is not None:
                market_data.rolling_load_minute_data(
                    trading_days, max_cache_days, freq)
        normalized_trading_days = [
            td.strftime('%Y-%m-%d') for td in trading_days]
        self.minute_bar_map = load_minute_bar_map(
            normalized_trading_days, self.universe, freq)


class MarketData(object):
    """
    行情内容包装类

    Attributes:
        * daily_bars: 日线数据，默认格式为ast的dict of DataFrame
        * minute_bars: 分钟线数据，默认格式为ast的dict of dict of ndarray
    """

    def __init__(self, universe, daily_fields, minute_fields, daily_bars_loader, minute_bars_loader, minute_extend_fields=[],
                 cache_expand_minute_bars=False, asset_type=None):
        self.universe = universe
        self.asset_type = asset_type

        self.daily_bars = {}
        self.daily_fields = daily_fields
        self._daily_bars_loader = daily_bars_loader
        self._daily_bars_loaded_days = []

        self.minute_bars = {}
        self.minute_fields = minute_fields
        self.minute_extend_fields = minute_extend_fields
        self._minute_bars_loader = minute_bars_loader
        self._minute_bars_expanded = {}
        self._minute_bars_loaded_days = []
        self._cache_expanded_minute_bars = cache_expand_minute_bars

    def _valid_symbols(self, symbols):
        """
        slice的helper函数，过滤本类别的资产，不要删除
        """
        if isinstance(symbols, list):
            symbols = set(symbols)
        elif isinstance(symbols, set):
            pass
        else:
            symbols = {symbols}
        valid_symbols = self.universe
        return list(set(symbols) & set(valid_symbols))

    def valid_fields(self, fields, freq='d'):
        """
        slice的helper函数，过滤valid_fields
        """
        fields = fields if isinstance(fields, list) else [fields]
        if freq in ['d', '1d']:
            return list(set(fields) & set(self.daily_fields))
        elif freq in ['m', '1m', '5m', '15m', '30m', '60m']:
            return list(set(fields) & set(self.minute_fields))

    def rolling_load_daily_data(self, trading_days, max_cache_days=None, freq='1d'):
        """
        MarketData的日行情加载方法

        Args:
            trading_days(list of datetime): 需加载的交易日，backtest中已含max_window_history
            max_cache_days(int): daily_bars最大加载的交易天数，默认加载全部交易日
        """
        self.daily_bars = _rolling_load_data(self.daily_bars, trading_days, self.universe, max_cache_days,
                                             self._daily_bars_loader, self.daily_fields, freq)
        self._daily_bars_loaded_days = trading_days

    def load_expanded_minute_data(self, fields):
        raise NotImplementedError(
            'Need to implement load_expanded_minute_data.')

    def rolling_load_minute_data(self, trading_days, max_cache_days, freq='1m'):
        """
        MarketData滚动加载分钟线数据, 如cache_minute_bars则展开分钟线行情数据

        Args:
            trading_days(list of datetime): 需加载分钟线的交易日
            max_cache_days: minute_bars中最大加载的交易日

        Returns:
            dict of DataFrame (ast格式)，当前增量加载完成之后的分钟线数据
        """
        if not set(trading_days) <= set(self._daily_bars_loaded_days):
            raise AttributeError('Exception in "MarketData.rolling_load_minute_data": '
                                 'minute increment load data must be in scope of daily trading data')
        self.minute_bars = _rolling_load_data(self.minute_bars, trading_days, self.universe, max_cache_days,
                                              self._minute_bars_loader, self.minute_fields, freq)
        self._minute_bars_loaded_days = trading_days
        if self.minute_extend_fields:
            self.load_expanded_minute_data(self.minute_extend_fields)

        return self.minute_bars

    def _check_time_range(self, end_date, freq):
        """
        检查slice时end_date和freq是否合法
        """
        valid_trading_days = []
        if freq in ['m', '1m', '5m', '15m', '30m', '60m']:
            valid_trading_days = self._minute_bars_loaded_days
        elif freq in ['d', '1d']:
            valid_trading_days = self._daily_bars_loaded_days
        return valid_trading_days[0] <= end_date <= valid_trading_days[-1]

    def slice(self, symbols, fields, end_date=None, freq='d', style='ast', time_range=1, rtype='frame', start_date=None,
              **options):
        """
        行情Panel数据的筛选

        Args:
            symbols(list of symbol): 需要筛选的symbols列表
            fields(list of str): 需要筛选的字段列表
            end_date(datetime): 需要获取的行情结束时间
            freq('d' or 'm'): 需要获取的行情数据频率，'d'代表日线，'m'代表分钟线
            style('ast', 'sat' or 'tas'): 返回数据Panel的层次样式顺序（field->column->index），其中'a'表示attribute，'s'表示symbol，'t'表示time，默认'ast'
            time_range(int): 切割end_date前time_range个交易日
            rtype('frame' or 'dict'): 返回的Panel数据的格式，frame表示dict of DataFrame, dict表示dict of dict

        Returns:
            dict, 格式视style与rtype参数输入
        -------
         """
        end_time_str = end_date.strftime('%Y-%m-%d')
        start_time_str = start_date.strftime(
            '%Y-%m-%d') if start_date is not None else None
        if freq in ['d', '1d']:
            data = self.daily_bars
        elif freq in ['m', '1m', '5m', '15m', '30m', '60m']:
            data = self.minute_bars
        else:
            raise AttributeError(
                'Exception in "MarketData.slice": unknown data slice query')
        self._check_time_range(end_date, freq)
        symbols = self._valid_symbols(symbols)
        fields = self.valid_fields(fields, freq)
        raw_data_dict = _ast_slice(data, symbols, end_time_str=end_time_str, fields=fields,
                                   time_range=time_range, start_time_str=start_time_str,
                                   **options)
        return _stylish(raw_data_dict, symbols, [item.strftime('%Y-%m-%d') for item in self._daily_bars_loaded_days], fields, style, rtype=rtype)


class FuturesMarketData(MarketData):
    """
    MarketService中加载期货行情的单元

    Attributes:
        * daily_bars(dict of DataFrame): 含各个daily_fields的日行情, ast格式
        * daily_fields(list of str): 日行情需加载的完整字段
        * minute_bars(dict of DataFrame): 含各个daily_fields的分钟行情, ast格式
        * minute_fields(list of str): 分钟线行情需加载的完整字段
        * universe(set of symbol): MarketService中股票类型组成的universe
    """

    def __init__(self, futures_universe, mkt_daily_field=FUTURES_DAILY_FIELDS,
                 mkt_minute_field=FUTURES_MINUTE_FIELDS, minute_freq='1m'):
        """
        Args:
            futures_universe: set of stock symbol, 如：set(['IFM0', 'HCM0'])
        """
        super(FuturesMarketData, self).__init__(futures_universe,
                                                list(
                                                    set(mkt_daily_field + ['tradeDate'])),
                                                list(
                                                    set(mkt_minute_field + ['barTime', 'tradeDate', 'clearingDate'])),
                                                self._daily_data_loader,
                                                self._minute_data_loader,
                                                cache_expand_minute_bars=False)
        self.daily_available_minute_bars = {}
        self._prev_clearing_date_map = {}

    def valid_fields(self, fields, freq='d'):
        """
        slice的helper函数，过滤valid_fields
        """
        fields = fields if isinstance(fields, list) else [fields]
        if freq in ['d', '1d']:
            return list(set(fields) & set(self.daily_fields))
        elif freq in ['m', '1m', '5m', '15m', '30m', '60m']:
            return list(set(fields) & (set(self.minute_fields) | set(['tradeTime'])))

    def rolling_load_daily_data(self, trading_days, max_cache_days=None, freq='1d'):
        """
        FuturesMarketData的rolling_load_daily_data，一次全部加载完整的trading_days。

        Args:
            trading_days(list of datetime): 需加载的交易日，backtest中已含max_window_history
            max_cache_days(int): daily_bars最大加载的交易天数，默认加载全部交易日
        """
        MarketData.rolling_load_daily_data(
            self, trading_days, max_cache_days, freq)
        self._prev_clearing_date_map = dict(zip(
            self._daily_bars_loaded_days, [previous_trading_day(trading_days[0])] + self._daily_bars_loaded_days[:-1]))
        self._prev_clearing_date_map = {key.strftime('%Y-%m-%d'): value.strftime('%Y-%m-%d')
                                        for key, value in self._prev_clearing_date_map.iteritems()}

    def rolling_load_minute_data(self, trading_days, max_cache_days, freq):
        """
        FuturesMarketData加载压缩好的分钟线数据

        Args:
            trading_days(list of datetime): 需加载分钟线的交易日list
            max_cache_days(int): minute_bars最大加载的分钟线交易日数量

        Returns:
            dict, 压缩好的各fields分钟线行情
        """
        minute_data_compressed = MarketData.rolling_load_minute_data(
            self, trading_days, max_cache_days, freq)
        self.daily_available_minute_bars = {}
        for day, row in minute_data_compressed['barTime'].iterrows():
            row_matrix = row.dropna().as_matrix()
            if row_matrix.any():
                self.daily_available_minute_bars[day] = sorted(
                    set(np.concatenate(row_matrix)))
        return minute_data_compressed

    def _daily_data_loader(self, universe, trading_days, fields, freq):
        daily_data = load_daily_futures_data(
            universe, trading_days, fields, freq)
        return daily_data

    def _minute_data_loader(self, universe, trading_days, fields, freq):
        """
        FuturesMarketData.minute_bars的具体加载函数
        """
        # 分批加载
        return_data = load_minute_futures_data(
            universe, trading_days, fields, freq)
        return return_data

    def load_expanded_minute_data(self, fields):
        # 将日线数据扩展到分钟线
        pass

    def get_trade_time(self, clearing_date, minute_bar):
        """
        根据清算日期和分钟线获取对应的trade_time，主要用作expand_slice的查询时的end_time_str
        Args:
            clearing_date(datetime): 清算日期
            minute_bar(str): 分钟线，格式为HH:mm
        """
        prev_trading_day = self._prev_clearing_date_map.get(
            clearing_date, None)
        if prev_trading_day is None:
            raise AttributeError('Exception in "FuturesMarketData.get_trade_time": '
                                 'unknown clearing date {}'.format(clearing_date))
        if minute_bar > '16:00':
            return '{} {}'.format(prev_trading_day, minute_bar)
        else:
            return '{} {}'.format(clearing_date, minute_bar)


def _intraday_equity_loader_extend(universe, trading_days, fields=EQUITY_MINUTE_FIELDS,
                                   factors=[], fs_field=[], daily_bar=None, freq='1m'):
    pure_fields = set(fields) & (
        set(EQUITY_MINUTE_FIELDS) | set(ALIAS_MINUTE_PRICE))
    minute_data = {}
    if pure_fields:
        minute_data = load_intraday_equity_data(
            universe, trading_days, list(pure_fields), freq)
    if freq in ['m', '1m']:
        data_len = 241
        equity_intraday_bar = EQUITY_MIN_BAR
    elif freq == '5m':
        data_len = 49
        equity_intraday_bar = EQUITY_5MIN_BAR
    elif freq == '15m':
        data_len = 17
        equity_intraday_bar = EQUITY_15MIN_BAR
    elif freq == '30m':
        data_len = 9
        equity_intraday_bar = EQUITY_30MIN_BAR
    elif freq == '60m':
        data_len = 5
        equity_intraday_bar = EQUITY_60MIN_BAR

    # 交易日索引， 在这里作为基准计算
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]

    if 'tradeDate' in fields:
        tds = [np.array(data_len * [td])
               for td in minute_data['tradeDate'].index]
        minute_data['tradeDate'] = pd.DataFrame({stk: tds for stk in universe},
                                                index=trading_days_index)
    if 'tradeTime' in fields:
        minutes = equity_intraday_bar
        ttimes = [np.array([td + ' ' + m for m in minutes])
                  for td in trading_days_index]
        minute_data['tradeTime'] = pd.DataFrame({stk: ttimes for stk in universe},
                                                index=trading_days_index)
    if 'barTime' in fields:
        minute_bars = np.array(equity_intraday_bar)
        minutes = [minute_bars] * len(trading_days_index)
        minute_data['barTime'] = pd.DataFrame({stk: minutes for stk in universe},
                                              index=trading_days_index)
    # 如果有因子，在这里展开
    if factors and daily_bar:
        # 获取日线因子数据
        for factor in factors:
            minute_bars = np.array(equity_intraday_bar)
            minutes = [minute_bars] * len(trading_days_index)
            factor_data = dict()
            for stk in universe:
                factor_data_per_stk = []
                for date_index in trading_days_index:
                    factor_data_per_stk.append(
                        [daily_bar[factor][stk][date_index]] * data_len)
                factor_data.update({stk: factor_data_per_stk})
            minute_data[factor] = pd.DataFrame(factor_data,
                                               index=trading_days_index)
    if fs_field and daily_bar:
        # 获取三大报表数据
        for one in fs_field:
            minute_bars = np.array(equity_intraday_bar)
            minutes = [minute_bars] * len(trading_days_index)
            fs_data = dict()
            for stk in universe:
                fs_data_per_stk = []
                for date_index in trading_days_index:
                    fs_data_per_stk.append(
                        [daily_bar[one][stk][date_index]] * data_len)
                fs_data.update({stk: fs_data_per_stk})
            minute_data[one] = pd.DataFrame(fs_data,
                                            index=trading_days_index)
    return minute_data


_EQUITY_MINUTE_TRADE_ESSENTIAL_TO_LOAD = EQUITY_MINUTE_FIELDS + \
    ['barTime', 'tradeTime', 'tradeDate']


class FundMarketData(MarketData):
    """
    MarketService中加载交易所基金行情的单元
    """

    def __init__(self, fund_universe, mkt_daily_field, mkt_minute_field, adj):
        """
        Parameters
        ----------
        fund_universe: set of fund symbol, 如：set(['511010.XSHG', '150195.XSHE'])
        """

        daily_fields = mkt_daily_field
        # 当出现行情字段的时候，需要带上tradeDate用来作为基准对行情数据补全
        if mkt_daily_field:
            daily_fields = list(set(mkt_daily_field + ['tradeDate']))
        minute_fields = list(
            set(mkt_minute_field + ['tradeTime', 'tradeDate']))
        if (mkt_daily_field or minute_fields) and adj:
            # adj 只有当行情字段存在的时候才有价值，否则没有用
            daily_fields = list(set(daily_fields + ['adjFactor', 'tradeDate']))

        super(FundMarketData, self).__init__(fund_universe, daily_fields,
                                             minute_fields,
                                             self._daily_data_loader,
                                             self._minute_data_loader,
                                             cache_expand_minute_bars=False)
        self._adj = adj

    def _daily_data_loader(self, universe, trading_days, fields=EQUITY_DAILY_FIELDS, freq='d'):
        """
        同StockMarketData的日行情加载方法，主要用来处理复权
        """
        daily_equity_data = load_daily_equity_data(
            universe, trading_days, fields)
        daily_bars = {}
        if self._adj:
            adj_factor_matrix = daily_equity_data['adjFactor'].as_matrix()
            index = daily_equity_data['adjFactor'].index
            columns = daily_equity_data['adjFactor'].columns
            for var in (set(STOCK_ADJ_FIELDS) - set(['volume', 'turnoverVol']) & set(fields)):
                daily_equity_data[var] = pd.DataFrame(
                    data=np.round(
                        daily_equity_data[var].as_matrix() * adj_factor_matrix, 3),
                    index=index, columns=columns)
            if 'turnoverVol' in fields:
                daily_equity_data['turnoverVol'] = pd.DataFrame(
                    np.round(
                        daily_equity_data['turnoverVol'].as_matrix() / adj_factor_matrix, 3),
                    index=index, columns=columns)
            if 'volume' in fields:
                daily_equity_data['volume'] = pd.DataFrame(
                    np.round(
                        daily_equity_data['volume'].as_matrix() / adj_factor_matrix, 3),
                    index=index, columns=columns)
        daily_bars.update(daily_equity_data)
        return daily_bars

    def _minute_data_loader(self, universe, trading_days, fields=EQUITY_MINUTE_FIELDS, freq='1m'):
        """
        同StockMarketData的分钟行情加载方法，主要用来处理复权
        """
        trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
        minute_data = _intraday_equity_loader_extend(
            universe, trading_days, fields, [], [], self.daily_bars, freq)
        if self._adj:

            adj_factor_matrix = self.daily_bars['adjFactor'].as_matrix()
            columns = self.daily_bars['adjFactor'].columns
            for var in (set(STOCK_ADJ_FIELDS) - set(['volume', 'turnoverVol'])) & set(fields):
                if var == 'preClosePrice':
                    continue
                minute_data[var] = pd.DataFrame(adj_factor_matrix * minute_data[var].as_matrix(),
                                                index=trading_days_index, columns=columns)
            if 'turnoverVol' in fields:
                minute_data['turnoverVol'] = pd.DataFrame(minute_data['turnoverVol'] / adj_factor_matrix,
                                                          index=trading_days_index, columns=columns)
            if 'volume' in fields:
                minute_data['volume'] = pd.DataFrame(minute_data['volume'] / adj_factor_matrix,
                                                     index=trading_days_index, columns=columns)

        return minute_data


class IndexMarketData(MarketData):
    """
    MarketService中加载指数行情的单元
    """

    def __init__(self, index_universe, mkt_daily_field, mkt_minute_field):
        """
        Parameters
        ----------
        index_universe: set of index symbol, 如：set(['000016.ZICN', '000905.ZICN'])
        """
        super(IndexMarketData, self).__init__(index_universe, list(set(mkt_daily_field + ['tradeDate'])) if mkt_daily_field else mkt_daily_field,
                                              list(
                                                  set(mkt_minute_field + ['tradeTime', 'tradeDate'])),
                                              load_daily_equity_data,
                                              _intraday_equity_loader_extend,
                                              cache_expand_minute_bars=False)


class StockMarketData(MarketData):
    """
    MarketService中加载股票行情、因子数据的单元。

    Attributes:
        * asset_type(str): 'stock'
        * daily_bars(dict of DataFrame): 含各个daily_fields的日行情, ast格式
        * daily_fields(list of str): 日行情需加载的完整字段
        * factors(list of str): 因子列表，fq_factor除外
        * minute_bars(dict of DataFrame): 含各个daily_fields的分钟行情, ast格式
        * minute_fields(list of str): 分钟线行情需加载的完整字段
        * universe(set of symbol): MarketService中股票类型组成的universe
    """

    def __init__(self, stock_universe, mkt_daily_field=EQUITY_DAILY_FIELDS,
                 mkt_minute_field=EQUITY_MINUTE_FIELDS, stock_factors=list(),
                 fs_field=list(), adj=True, **kwargs):
        """
        Args:
            stock_universe: set of stock symbol, 如：set(['601328.XSHG', '000559.XSHE'])
            stock_factors(list of str): StockMarketData加入的特有因子(如['PB', "ROE'])，默认无
            adj(boolean): 是否根据fq_factor调整，默认True
            minute_with_trade_dates(boolean): 获取的数据中是否包含'barTime'和'tradeTime'
        """
        daily_fields = mkt_daily_field
        # 当出现行情字段的时候，需要带上tradeDate用来作为基准对行情数据补全

        if mkt_daily_field:
            daily_fields = list(set(mkt_daily_field + ['tradeDate']))
        minute_fields = list(
            set(mkt_minute_field + ['tradeTime', 'tradeDate']))
        if (mkt_daily_field or minute_fields) and adj:
            # adj 只有当行情字段存在的时候才有价值，否则没有用
            daily_fields = list(set(daily_fields + ['adjFactor', 'tradeDate']))

        MarketData.__init__(self, stock_universe, daily_fields, minute_fields,
                            self._daily_data_loader,
                            self._minute_data_loader, [],
                            cache_expand_minute_bars=False)
        self._adj = adj
        self.factors = stock_factors
        self.fs_field = fs_field
        self.__principal_name = None
        if 'DatayesPrincipalName' in kwargs and kwargs['DatayesPrincipalName'] is not None:
            self.__principal_name = kwargs['DatayesPrincipalName']

    def valid_fields(self, fields, freq='d'):
        """
        slice的helper函数，过滤valid_fields
        """
        fields = fields if isinstance(fields, list) else [fields]
        if freq in ['d', '1d']:
            return list(set(fields) & (set(self.daily_fields) | set(self.factors) | set(self.fs_field)))
        elif freq in ['m', '1m', '5m', '15m', '30m', '60m']:
            return list(set(fields) & (set(self.minute_fields) | set(self.factors) | set(self.fs_field)))

    def set_factors(self, factors):
        """
        设置StockMarketData的特有因子self.factors及self.daily_fields, 将原本的equity_daily_fields加上传入的factor。

        Args:
            factors: list of 因子，如通联因子

        Returns:
            list of fields
        """
        self.factors = factors
        self.daily_fields = EQUITY_DAILY_FIELDS + list(factors)

    def _daily_data_loader(self, universe, trading_days, fields=EQUITY_DAILY_FIELDS,
                           freq='d', **kwargs):
        """
        StockMarketData的日行情加载方法
        """
        daily_bars = {}
        # 是否有行情需要加载
        if self.daily_fields:

            daily_equity_data = load_daily_equity_data(
                universe, trading_days, fields)
            if self._adj:
                adj_factor_matrix = daily_equity_data['adjFactor'].as_matrix()
                index = daily_equity_data['adjFactor'].index
                columns = daily_equity_data['adjFactor'].columns
                for var in (set(STOCK_ADJ_FIELDS) - set(['volume', 'turnoverVol'])) & set(fields):
                    daily_equity_data[var] = pd.DataFrame(
                        data=np.round(
                            daily_equity_data[var].as_matrix() * adj_factor_matrix, 3),
                        index=index, columns=columns)
                if 'turnoverVol' in fields:
                    daily_equity_data['turnoverVol'] = pd.DataFrame(
                        np.round(
                            daily_equity_data['turnoverVol'].as_matrix() / adj_factor_matrix, 3),
                        index=index, columns=columns)
                if 'volume' in fields:
                    daily_equity_data['volume'] = pd.DataFrame(
                        np.round(
                            daily_equity_data['volume'].as_matrix() / adj_factor_matrix, 3),
                        index=index, columns=columns)
            daily_bars.update(daily_equity_data)
        # 是否有因子需要加载
        if len(self.factors) > 0:
            factor_data = load_common_factor_data(
                universe, trading_days, self.factors, DatayesPrincipalName=self.__principal_name)
            daily_bars.update(factor_data)
        # 是否有财报需要加载
        if len(self.fs_field) > 0:
            fs_data = load_financial_statements(
                universe, trading_days, self.fs_field)
            daily_bars.update(fs_data)
        return daily_bars

    def _minute_data_loader(self, universe, trading_days, fields=EQUITY_MINUTE_FIELDS,
                            freq='1m'):
        """
        StockMarketData的分钟线行情加载方法
        """
        minute_data = _intraday_equity_loader_extend(universe, trading_days, fields,
                                                     self.factors, self.fs_field, self.daily_bars, freq)
        if self._adj:
            # 交易日索引， 在这里作为基准计算
            trading_days_index = [dt.strftime(
                "%Y-%m-%d") for dt in trading_days]

            adj_factor_matrix = self.daily_bars['adjFactor'].as_matrix()
            for var in (set(STOCK_ADJ_FIELDS) - set(['volume', 'turnoverVol'])) & set(fields):
                if var == 'preClosePrice':
                    continue
                minute_data[var] = pd.DataFrame(minute_data[var].as_matrix() * adj_factor_matrix,
                                                index=trading_days_index, columns=universe)
            if 'turnoverVol' in fields:
                minute_data['turnoverVol'] = pd.DataFrame(minute_data['turnoverVol'] / adj_factor_matrix,
                                                          index=trading_days_index, columns=universe)
            if 'volume' in fields:
                minute_data['volume'] = pd.DataFrame(minute_data['volume'] / adj_factor_matrix,
                                                     index=trading_days_index, columns=universe)

        return minute_data
