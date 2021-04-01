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
factors.py

factors data loader

@author: yudi.wu
"""

import pandas as pd

from . apiconfig import (
    BATCH_DAILY_DATA_SIZE,
    MAX_CACHEAPI_THREAD_AMOUNT,
    BATCH_FACTOR_DATA_SIZE
)
from . cache_api import UserDefinedFactorValuesGet, TranslateFactors


def load_common_factor_data(universe=None, trading_days=None, field=None, **kwargs):
    """
    从Mercury Cache中并发获取获得因子日线数据

    Args:
        universe (list of str): 股票池列表
        trading_days (list of datetime): 交易日列表
        field (list of string): 需要获取的因子数据字段名称

    Returns:
        dict of str=>DataFrame: 证券因子数据，key值为字段名称，value为该字段日线数据(DataFrame, column为证券代码, index为交易日[YYYYMMDD])的dict
    Examples:
        >> universe = set_universe('A')
        >> trading_days = get_trading_days()
        >> factor_values = load_common_factor_data(universe, trading_days, ['PE', 'PB'])
    """

    # 去除universe中的指数
    new_universe = []
    for stk in universe:
        if stk[-4:] in ['XSHE', 'XSHG']:
            new_universe.append(stk)
    # universe = new_universe
    trading_days_index = [dt.strftime("%Y-%m-%d") for dt in trading_days]
    trading_days = [dt.strftime("%Y%m%d") for dt in trading_days]
    T = len(trading_days)
    S = len(new_universe)

    # grouping for gevent, lower bound is 20
    N = max(5, BATCH_FACTOR_DATA_SIZE // T)
    batches = [new_universe[i:min(i + N, S)] for i in range(0, S, N)]

    def gload(idx, bat):
        mkt_data = UserDefinedFactorValuesGet(
            universe=bat, trading_days=trading_days, field=list(field), **kwargs)
        return idx, mkt_data
    from gevent.pool import Pool
    pool = Pool(MAX_CACHEAPI_THREAD_AMOUNT)
    requests = [pool.spawn(gload, idx, bat)
                for (idx, bat) in enumerate(batches)]
    pool.join()

    data_all = {var: {} for var in field}

    for response in sorted(requests, key=lambda x: x.value[0]):
        _, data = response.value
        for var in data_all:
            for sec in data[var]:
                data_all[var][sec] = data[var][sec]
    zero_column = [float('nan')] * T
    for var, values in data_all.iteritems():
        for sec in set(universe) - set(data_all[var].keys()):
            values[sec] = zero_column
        data_all[var] = pd.DataFrame(
            values, index=trading_days, columns=universe)
        data_all[var].index = trading_days_index
    return data_all


def translate_factors(factors, start_date, **kwargs):
    factor_dict = TranslateFactors(factors, start_date, **kwargs)
    return_arr = []
    if factor_dict:
        for item in factor_dict:
            return_arr += factor_dict[item].values()

    return return_arr
