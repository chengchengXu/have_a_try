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

__doc__="申万"
def __MktSWidxdGet(ticker = "", tradeDate = "", field = "", pandas = "1"):
    """
    获取申万指数日度收盘行情信息，包含开盘价、最高价、最低价、收盘价、涨跌幅、成交量、成交金额、总市值、、流通市值、市盈率、市净率等。注：指数代码未转换为通联证券编码。
    
    :param ticker: 指数通用交易代码,可以是列表,ticker、tradeDate至少选择一个
    :param tradeDate: 交易日期,ticker、tradeDate至少选择一个
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
    requestString.append('/api/idxMarket/getMktSWidxd.csv?ispandas=1&') 
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
    try:
        tradeDate = tradeDate.strftime('%Y%m%d')
    except:
        tradeDate = tradeDate.replace('-', '')
    requestString.append("&tradeDate=%s"%(tradeDate))
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
            api_base.handle_error(csvString, '__MktSWidxdGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MktSWidxdGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'ticker', u'secShortName', u'tradeDate', u'openIndex', u'lowIndex', u'highIndex', u'closeIndex', u'chg', u'chgPct', u'value', u'volume', u'PE', u'PB', u'negMarketValueA', u'marketValue']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'ticker': 'str','secShortName': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def SWTickRTSnapshotGet(ticker = "", field = "", pandas = "1"):
    """
    高频数据，获取一只或多只获取申万指数（包含行业指数）最新市场信息快照。 5～15秒更新一次。
    
    :param ticker: 申万指数代码,可以是列表,可空
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
    requestString.append('/api/swMarket/getSWTickRTSnapshot.csv?ispandas=1&') 
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
            api_base.handle_error(csvString, 'SWTickRTSnapshotGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'SWTickRTSnapshotGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'dataDate', u'dataTime', u'ticker', u'shortNM', u'prevClosePrice', u'openPrice', u'highPrice', u'lowPrice', u'lastPrice', u'value', u'volume', u'cRatio', u'amplitude', u'VR', u'change', u'changePct', u'bidVolume123', u'bidPrice2', u'bidVolume2', u'bidPrice3', u'bidVolume3', u'askVolume123', u'askPrice2', u'askVolume2', u'askPrice3', u'askVolume3', u'upLead']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'dataDate': 'str','dataTime': 'str','ticker': 'str','shortNM': 'str','upLead': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def SWTickRTIntraDayGet(ticker = "", startTime = "", endTime = "", field = "", pandas = "1"):
    """
    高频数据，获取一只或多只获取申万指数（包含行业指数）当日某一时间段的市场信息快照。 每日8点清空昨日数据。
    
    :param ticker: 申万指数代码,可以是列表,ticker、startTime、endTime至少选择一个
    :param startTime: 开始时间，格式为HH:MM,ticker、startTime、endTime至少选择一个
    :param endTime: 结束时间，格式为HH:MM,ticker、startTime、endTime至少选择一个
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
    requestString.append('/api/swMarket/getSWTickRTIntraDay.csv?ispandas=1&') 
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
            api_base.handle_error(csvString, 'SWTickRTIntraDayGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'SWTickRTIntraDayGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'dataDate', u'dataTime', u'ticker', u'shortNM', u'prevClosePrice', u'openPrice', u'highPrice', u'lowPrice', u'lastPrice', u'value', u'volume', u'cRatio', u'bidVolume123', u'bidPrice2', u'bidVolume2', u'bidPrice3', u'bidVolume3', u'askVolume123', u'askPrice2', u'askVolume2', u'askPrice3', u'askVolume3']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'dataDate': 'str','dataTime': 'str','ticker': 'str','shortNM': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def SWBarRTIntraDayGet(unit, ticker = "", startTime = "", endTime = "", field = "", pandas = "1"):
    """
    高频数据，获取一只或多只获取申万指数（包含行业指数）当日分钟线数据。
    
    :param unit: Bar(s)的时间宽度，单位分钟。取值范围： 1/3/5/15/30/60/120（分钟）
    :param ticker: 指数代码。,可以是列表,可空
    :param startTime: 分钟线起始时间， 如09:40，就是从早上九点四十开始。 默认开始时间早上开市时间，即09:30，不选即为默认值,可空
    :param endTime: 分钟线终止时间， 如14:00, 就是到下午14点结束。 如终止时间是空， 则截止到最新数据或到关市为止，即15:00，不选即为默认值,可空
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
    requestString.append('/api/swMarket/getSWBarRTIntraDay.csv?ispandas=1&') 
    if not isinstance(unit, str) and not isinstance(unit, unicode):
        unit = str(unit)

    requestString.append("unit=%s"%(unit))
    requestString.append("&ticker=")
    if hasattr(ticker,'__iter__') and not isinstance(ticker, str):
        if len(ticker) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = ticker
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in ticker]))
    else:
        requestString.append(str(ticker) if not isinstance(ticker, unicode) else ticker)
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
            api_base.handle_error(csvString, 'SWBarRTIntraDayGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'SWBarRTIntraDayGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'date', u'unit', u'ticker', u'shortNM', u'barTime', u'openPrice', u'closePrice', u'highPrice', u'lowPrice', u'totalVolume', u'totalValue']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'ticker': 'str','shortNM': 'str','barTime': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

