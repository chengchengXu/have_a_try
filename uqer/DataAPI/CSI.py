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

__doc__="中证指数"
def CsiTickRTSnapshotGet(ticker = "", marketCode = "", field = "", pandas = "1"):
    """
    高频数据，获取一只或多只中证指数最新市场信息快照。
    
    :param ticker: 中证指数代码,可以是列表,ticker、marketCode至少选择一个
    :param marketCode: 指数所在市场范围，1-上证所，2-深交所，3-沪深，4-香港，5-亚太，0-全球，9-其他,可以是列表,ticker、marketCode至少选择一个
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
    requestString.append('/api/csiMarket/getCsiTickRTSnapshot.csv?ispandas=1&') 
    requestString.append("ticker=")
    if hasattr(ticker,'__iter__') and not isinstance(ticker, str):
        if len(ticker) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = ticker
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in ticker]))
    else:
        requestString.append(str(ticker) if not isinstance(ticker, unicode) else ticker)
    requestString.append("&marketCode=")
    if hasattr(marketCode,'__iter__') and not isinstance(marketCode, str):
        if len(marketCode) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = marketCode
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in marketCode]))
    else:
        requestString.append(str(marketCode) if not isinstance(marketCode, unicode) else marketCode)
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
            api_base.handle_error(csvString, 'CsiTickRTSnapshotGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'CsiTickRTSnapshotGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'ticker', u'indexName', u'tradeDate', u'localDate', u'dataTime', u'marketCode', u'lastPrice', u'highPrice', u'lowPrice', u'openPrice', u'preClosePrice', u'closePrice', u'change', u'chgPct', u'volume', u'value', u'currency', u'exchangeRate', u'closePrice2', u'closePrice3', u'amplitude', u'VR']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'ticker': 'str','indexName': 'str','dataTime': 'str','currency': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def CsiTickRTIntraDayGet(ticker = "", marketCode = "", startTime = "", endTime = "", field = "", pandas = "1"):
    """
    高频数据，获取一只或多只中证指数当日某一时间段市场信息快照。
    
    :param ticker: 中证指数代码,可以是列表,ticker、marketCode至少选择一个
    :param marketCode: 指数所在市场范围，1-上证所，2-深交所，3-沪深，4-香港，5-亚太，0-全球,ticker、marketCode至少选择一个
    :param startTime: 开始时间，格式为HH:MM,可空
    :param endTime: 结束时间，格式为HH:MM,可空
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
    requestString.append('/api/csiMarket/getCsiTickRTIntraDay.csv?ispandas=1&') 
    requestString.append("ticker=")
    if hasattr(ticker,'__iter__') and not isinstance(ticker, str):
        if len(ticker) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = ticker
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in ticker]))
    else:
        requestString.append(str(ticker) if not isinstance(ticker, unicode) else ticker)
    if not isinstance(marketCode, str) and not isinstance(marketCode, unicode):
        marketCode = str(marketCode)

    requestString.append("&marketCode=%s"%(marketCode))
    if not isinstance(startTime, str) and not isinstance(startTime, unicode):
        startTime = str(startTime)

    requestString.append("&startTime=%s"%(startTime))
    if not isinstance(endTime, str) and not isinstance(endTime, unicode):
        endTime = str(endTime)

    requestString.append("&endTime=%s"%(endTime))
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
            api_base.handle_error(csvString, 'CsiTickRTIntraDayGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'CsiTickRTIntraDayGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'ticker', u'indexName', u'tradeDate', u'localDate', u'dataTime', u'marketCode', u'lastPrice', u'highPrice', u'lowPrice', u'openPrice', u'preClosePrice', u'closePrice', u'change', u'chgPct', u'volume', u'value', u'currency', u'exchangeRate', u'closePrice2', u'closePrice3']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'ticker': 'str','indexName': 'str','dataTime': 'str','currency': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def EtfTickRTIntraDayGet(ticker = "", marketCode = "", startTime = "", endTime = "", field = "", pandas = "1"):
    """
    高频数据，获取一只或多只ETF在当日某一时间段的参考净值快照。
    
    :param ticker: ETF证券代码,可以是列表,ticker、marketCode至少选择一个
    :param marketCode: 指数所在市场范围，1-上证所，2-深交所，3-沪深，4-香港，5-亚太，0-全球,ticker、marketCode至少选择一个
    :param startTime: 开始时间，格式为HH:MM,可空
    :param endTime: 结束时间，格式为HH:MM,可空
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
    requestString.append('/api/csiMarket/getEtfTickRTIntraDay.csv?ispandas=1&') 
    requestString.append("ticker=")
    if hasattr(ticker,'__iter__') and not isinstance(ticker, str):
        if len(ticker) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = ticker
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in ticker]))
    else:
        requestString.append(str(ticker) if not isinstance(ticker, unicode) else ticker)
    if not isinstance(marketCode, str) and not isinstance(marketCode, unicode):
        marketCode = str(marketCode)

    requestString.append("&marketCode=%s"%(marketCode))
    if not isinstance(startTime, str) and not isinstance(startTime, unicode):
        startTime = str(startTime)

    requestString.append("&startTime=%s"%(startTime))
    if not isinstance(endTime, str) and not isinstance(endTime, unicode):
        endTime = str(endTime)

    requestString.append("&endTime=%s"%(endTime))
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
            api_base.handle_error(csvString, 'EtfTickRTIntraDayGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'EtfTickRTIntraDayGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'ticker', u'shortName', u'marketCode', u'dataDate', u'dataTime', u'IOPV']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'ticker': 'str','shortName': 'str','dataTime': 'str','IOPV': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

