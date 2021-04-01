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
__init__.py

Configuration for following data-APIs:
    cache service
    Datayes DataAPI
    ext.MFHandler

@author: yudi.wu
"""

import requests
import logging
import os

dev = os.getenv('env', 'dev') == 'dev'
prd = os.getenv('env', 'dev') == 'prd'

# ============= DATA TRANSFER CONFIGRATION ==============

BATCH_DAILY_DATA_SIZE = 20000     # 日间数据一次传输数据上限
BATCH_INTRADAY_DATA_SIZE = 200    # 日内数据一次传输数据上限
BATCH_FILTER_DAY_SIZE = 100       # 条件过滤器一次处理交易日数量上限
MAX_CACHEAPI_THREAD_AMOUNT = 4    # cache_api协程并发上限
BATCH_FACTOR_DATA_SIZE = 10000
BATCH_FINANCIAL_STATEMENTS_SIZE = 50000


# ============= CACHE SERVICE CONFIGRATION ==============

if not dev:
    CACHE_HOST = "tcp://mercury-cache:1111"  # prd
else:
    CACHE_HOST = 'tcp://Please set the cache server host, or set the environment "env":1111'  # stg
CACHE_API_TIMEOUT = 300


def __get_service():
    """private function to wrap the get client method"""

    # Tried adding a pool in client, not create new one every time, but
    # seems no goods, and need efforts to maintain the connection pool
    # Disable heartbeat, in heavy network, heartbeat lost will
    # throw exception and which will impact the normal query
    import zerorpc
    service = zerorpc.Client(heartbeat=None, timeout=CACHE_API_TIMEOUT)
    service.connect(CACHE_HOST)
    return service
