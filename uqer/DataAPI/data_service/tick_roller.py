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
import bisect
import numpy as np
import pandas as pd
import math
from . const import HISTORY_ESSENTIAL_FIELDS_MINUTE


def at_data_tick_expand(at_data):
    expanded_tick_data = {}
    for attr, data in at_data.iteritems():

        if attr == 'time' or data is None:
            continue
        if attr in ['clearingDate', 'symbol']:
            valid_data_list = []
            for idx, cont in enumerate(at_data['tradeTime']):
                if isinstance(cont, list):
                    valid_data_list.append([data[idx]] * len(cont))
        else:
            valid_data_list = [
                d for d in data if isinstance(d, list) or isinstance(d, np.ndarray) or not math.isnan(d)]
        if len(valid_data_list) > 0:
            expanded_tick_data[attr] = np.concatenate(valid_data_list)
    return expanded_tick_data


def st_data_tick_expand(st_data):
    return {s: np.concatenate(data) for (s, data) in st_data.iteritems() if s != 'time' and data is not None}


class TickRoller(object):

    def __init__(self, market_service):
        self.market_service = market_service
        self._inner_sat_data = None
        self._inner_sat_trade_dates = []
        self._inner_ast_data = None
        self._inner_ast_trade_dates = []
        self._pooled_tick_data = []

    def ast_slice(self, prepare_dates, end_time, time_range, fields=None, symbols=None):
        if not set(prepare_dates) <= set(self._inner_ast_trade_dates):
            ast_data = self.market_service.slice(
                symbols='all', fields=HISTORY_ESSENTIAL_FIELDS_MINUTE, freq='m', style='ast',
                end_date=prepare_dates[-1], time_range=len(prepare_dates), rtype='dict')

            self._inner_ast_data = {
                a: st_data_tick_expand(st_data) for (a, st_data) in ast_data.iteritems()}
            self._inner_ast_trade_dates = prepare_dates
            if len(self._pooled_tick_data) > 0:
                for minute_bar, trade_time, trade_date, tick_data in self._pooled_tick_data:
                    self._push_tick_item_to_ast(
                        minute_bar, trade_time, tick_data)
                    if trade_date not in self._inner_ast_trade_dates:
                        self._inner_ast_trade_dates.append(trade_date)
        result = {}
        fields = self._inner_ast_data.keys() if fields is None else fields
        trade_time_st = self._inner_ast_data['tradeTime']
        symbols = self._inner_ast_data[
            'tradeTime'].keys() if symbols == 'all' or symbols is None else symbols
        end_idx_by_symbol = {symbol: bisect.bisect_right(
            trade_time_st[symbol], end_time) for symbol in symbols}
        for attr in fields:
            st_data = self._inner_ast_data[attr]
            result[attr] = {symbol: st_data[symbol][end_idx_by_symbol[symbol] - time_range: end_idx_by_symbol[symbol]]
                            for symbol in symbols}
        return result

    def sat_slice(self, prepare_dates, end_time, time_range, fields=HISTORY_ESSENTIAL_FIELDS_MINUTE,
                  symbols='all'):

        if not set(prepare_dates) <= set(self._inner_sat_trade_dates):
            sat_data = self.market_service.slice(
                symbols='all', fields=fields, freq='m', style='sat',
                end_date=prepare_dates[-1], time_range=len(prepare_dates), rtype='dict')
            self._inner_sat_data = {
                s: at_data_tick_expand(at_data) for (s, at_data) in sat_data.iteritems()}
            self._inner_sat_trade_dates = prepare_dates
            if len(self._pooled_tick_data) > 0:
                for minute_bar, trade_time, trade_date, tick_data in self._pooled_tick_data:
                    self._push_tick_item_to_sat(
                        minute_bar, trade_time, tick_data)
                    if trade_date not in self._inner_sat_trade_dates:
                        self._inner_sat_trade_dates.append(trade_date)
        result = {}
        symbols = self._inner_sat_data.keys(
        ) if symbols is None or symbols == 'all' else symbols
        for symbol in symbols:
            at_data = self._inner_sat_data[symbol]
            if len(at_data) == 0:
                continue
            end_idx = bisect.bisect_right(at_data['tradeTime'], end_time)
            field = at_data.keys() if fields is None else list(
                set(fields) & set(at_data.keys()))
            st_result = {
                a: at_data[a][end_idx - time_range: end_idx] for a in field}
            result[symbol] = st_result
        return result

    def slice(self, prepare_dates, end_time, time_range, fields=None, symbols='all', style='sat', rtype='dict'):
        """
        对展开后的分钟线数据进行筛选获取

        Args:
            prepare_date(list of datetime): 为了完成slice，需要确保分钟线已经加载并展开的日期
            end_time(date formatted str): 需要查询历史数据的截止时间，格式为'YYYYmmdd HH:MM'
            time_range(int): 需要查询历史数据的时间区间
            fields(list of str): 需要查询历史数据的字段列表
            symbols(list of str): 需要查询历史数据的符号列表
            style(sat or ast): 筛选后数据的返回样式
            rtype(dict or frame): 筛选后数据Panel的返回格式，dict表示dict of dict，frame表示dict of DataFrame

        Returns:
            dict，根据style和rtype确定样式和结构
        """
        if style == 'sat':
            if rtype == 'frame':
                fields = fields + ['tradeTime']
            result = self.sat_slice(
                prepare_dates, end_time, time_range, fields, symbols)
            if rtype == 'frame':
                result = {s: pd.DataFrame(at_data).set_index(
                    'tradeTime') for (s, at_data) in result.iteritems()}
        elif style == 'ast':
            if rtype == 'frame':
                fields = fields + ['tradeTime']
                result = self.sat_slice(
                    prepare_dates, end_time, time_range, fields, symbols)
                result = {s: pd.DataFrame(at_data).set_index(
                    'tradeTime') for (s, at_data) in result.iteritems()}
                ast_result = dict(pd.Panel.from_dict(result).swapaxes(0, 2))
                return {item: ast_result[item] for item in ast_result}
            else:
                result = self.ast_slice(
                    prepare_dates, end_time, time_range, fields, symbols)
            if rtype == 'frame':
                trade_times = result['tradeTime'].values()[0]
                for a, st_data in result.iteritems():
                    if a == 'tradeTime':
                        continue
                    result[a] = pd.DataFrame(st_data).set_index(trade_times)
                result.pop('tradeTime')
        else:
            raise AttributeError(
                'unknown slice type {} for TickRoller'.format(style))
        return result
