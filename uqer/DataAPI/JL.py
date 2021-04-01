# -*- coding: UTF-8 -*-
from . import api_base
try:
    from StringIO import StringIO
except:
    from io import StringIO
import pandas as pd
import sys
from datetime import datetime
from .api_base import get_cache_key, get_data_from_cache, put_data_in_cache, pretty_traceback
import inspect
try:
    unicode
except:
    unicode = str

__doc__="巨灵财经"
def __MktEquwJLGet(secID, startDate = "", finishDate = "", field = "", pandas = "1"):
    """
    本表为衍生表，主要计算个股每周的市场表现。包括最高价、最低价、涨跌、涨跌幅、均价、对数收益率、BETA值等，历史追溯至1990年，每周更新。
    
    :param secID: 证券内部编码，一串流水号,可先通过DataAPI.SecIDGet获取到，如在DataAPI.SecIDGet，选择证券类型为'E',输入'000001'，可获取到ID'000001.XSHE'后，在此输入'000001.XSHE',可以是列表
    :param startDate: 起始日期，输入格式为yyyymmdd,可空
    :param finishDate: 结束日期，输入格式为yyyymmdd,可空
    :param field: 所需字段,可以是列表,可空
    :param pandas: 1表示返回 pandas data frame，0表示返回csv,可空
    :return: :raise e: API查询的结果，是CSV或者被转成pandas data frame；若查询API失败，返回空data frame； 若解析失败，则抛出异常
    """
        
    pretty_traceback()
    frame = inspect.currentframe()
    func_name, cache_key = get_cache_key(frame)
    cache_result = get_data_from_cache(func_name, cache_key)
    if cache_result is not None:
        return cache_result
    split_index = None
    split_param = None
    httpClient = api_base.__getConn__()    
    requestString = []
    requestString.append('/api/market/getMktEquwJL.csv?ispandas=1&') 
    requestString.append("secID=")
    if hasattr(secID,'__iter__') and not isinstance(secID, str):
        if len(secID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = secID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in secID]))
    else:
        requestString.append(str(secID) if not isinstance(secID, unicode) else secID)
    try:
        startDate = startDate.strftime('%Y%m%d')
    except:
        startDate = startDate.replace('-', '')
    requestString.append("&startDate=%s"%(startDate))
    try:
        finishDate = finishDate.strftime('%Y%m%d')
    except:
        finishDate = finishDate.replace('-', '')
    requestString.append("&finishDate=%s"%(finishDate))
    requestString.append("&field=")
    if hasattr(field,'__iter__') and not isinstance(field, str):
        if len(field) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = field
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in field]))
    else:
        requestString.append(str(field) if not isinstance(field, unicode) else field)
    if split_param is None:
        csvString = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
        if csvString is None or len(csvString) == 0 or (csvString[0] == '-' and not api_base.is_no_data_warn(csvString, False)) or csvString[0] == '{':
            api_base.handle_error(csvString, '__MktEquwJLGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MktEquwJLGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'secID', u'ticker', u'secShortName', u'exchangeCD', u'endDate', u'firstTradeDate', u'lastTradeDate', u'numDays', u'preClosePrice', u'openPrice', u'highestPrice', u'dayHigh', u'lowestPrice', u'dayLow', u'closePrice', u'highClosePrice', u'dayHcp', u'lowClosePrice', u'dayLcp', u'avgPrice', u'rangePct', u'adChg', u'adChgPct', u'logReturn', u'turnoverVol', u'turnoverValue', u'turnoverRate', u'avgTurnoverRate', u'adPreClosePrice', u'adOpenPrice', u'adHighestPrice', u'adDayHigh', u'adDayLow', u'adLowestPrice', u'adClosePrice', u'adHighClosePrice', u'adLowClosePrice', u'adDayHcp', u'adDayLcp']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'secID': 'str','ticker': 'str','secShortName': 'str','exchangeCD': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

