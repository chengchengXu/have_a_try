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

__doc__="华通人"
def __MacroDataDjsjdACMRGet(indicID = "", indicName = "", regionCD = "", region = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人地级市季度数据。历史数据从1998年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param regionCD: 地区代码，国家统计局行政区划编码,可以是列表,可空
    :param region: 地区名称,可空
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataDjsjdACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    requestString.append("&regionCD=")
    if hasattr(regionCD,'__iter__') and not isinstance(regionCD, str):
        if len(regionCD) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = regionCD
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in regionCD]))
    else:
        requestString.append(str(regionCD) if not isinstance(regionCD, unicode) else regionCD)
    if not isinstance(region, str) and not isinstance(region, unicode):
        region = str(region)

    requestString.append("&region=%s"%(region))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataDjsjdACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataDjsjdACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'regionCD', u'region', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','regionCD': 'str','region': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataDjsndACMRGet(indicID = "", indicName = "", regionCD = "", region = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人地级市年度数据。历史数据从1949年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param regionCD: 地区代码，国家统计局行政区划编码,可以是列表,可空
    :param region: 地区名称,可空
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataDjsndACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    requestString.append("&regionCD=")
    if hasattr(regionCD,'__iter__') and not isinstance(regionCD, str):
        if len(regionCD) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = regionCD
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in regionCD]))
    else:
        requestString.append(str(regionCD) if not isinstance(regionCD, unicode) else regionCD)
    if not isinstance(region, str) and not isinstance(region, unicode):
        region = str(region)

    requestString.append("&region=%s"%(region))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataDjsndACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataDjsndACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'regionCD', u'region', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','regionCD': 'str','region': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataDjsydACMRGet(indicID = "", indicName = "", regionCD = "", region = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人地级市月度数据。历史数据从1987年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param regionCD: 地区代码，国家统计局行政区划编码,可以是列表,可空
    :param region: 地区名称,可空
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataDjsydACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    requestString.append("&regionCD=")
    if hasattr(regionCD,'__iter__') and not isinstance(regionCD, str):
        if len(regionCD) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = regionCD
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in regionCD]))
    else:
        requestString.append(str(regionCD) if not isinstance(regionCD, unicode) else regionCD)
    if not isinstance(region, str) and not isinstance(region, unicode):
        region = str(region)

    requestString.append("&region=%s"%(region))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataDjsydACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataDjsydACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'regionCD', u'region', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','regionCD': 'str','region': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataFsjdACMRGet(indicID = "", indicName = "", regionCD = "", region = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人分省季度数据。历史数据从1986年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param regionCD: 地区代码，国家统计局行政区划编码,可以是列表,可空
    :param region: 地区名称,可空
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataFsjdACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    requestString.append("&regionCD=")
    if hasattr(regionCD,'__iter__') and not isinstance(regionCD, str):
        if len(regionCD) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = regionCD
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in regionCD]))
    else:
        requestString.append(str(regionCD) if not isinstance(regionCD, unicode) else regionCD)
    if not isinstance(region, str) and not isinstance(region, unicode):
        region = str(region)

    requestString.append("&region=%s"%(region))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataFsjdACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataFsjdACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'regionCD', u'region', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','regionCD': 'str','region': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataFsndACMRGet(indicID = "", indicName = "", regionCD = "", region = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人分省年度数据。历史数据从1947年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param regionCD: 地区代码，国家统计局行政区划编码,可以是列表,可空
    :param region: 地区名称,可空
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataFsndACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    requestString.append("&regionCD=")
    if hasattr(regionCD,'__iter__') and not isinstance(regionCD, str):
        if len(regionCD) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = regionCD
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in regionCD]))
    else:
        requestString.append(str(regionCD) if not isinstance(regionCD, unicode) else regionCD)
    if not isinstance(region, str) and not isinstance(region, unicode):
        region = str(region)

    requestString.append("&region=%s"%(region))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataFsndACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataFsndACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'regionCD', u'region', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','regionCD': 'str','region': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataFsydACMRGet(indicID = "", indicName = "", regionCD = "", region = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人分省月度数据。历史数据从1986年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param regionCD: 地区代码，国家统计局行政区划编码,可以是列表,可空
    :param region: 地区名称,可空
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataFsydACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    requestString.append("&regionCD=")
    if hasattr(regionCD,'__iter__') and not isinstance(regionCD, str):
        if len(regionCD) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = regionCD
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in regionCD]))
    else:
        requestString.append(str(regionCD) if not isinstance(regionCD, unicode) else regionCD)
    if not isinstance(region, str) and not isinstance(region, unicode):
        region = str(region)

    requestString.append("&region=%s"%(region))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataFsydACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataFsydACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'regionCD', u'region', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','regionCD': 'str','region': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataHgjdACMRGet(indicID = "", indicName = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人全国宏观季度数据。历史数据从1978年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataHgjdACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataHgjdACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataHgjdACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataHgndACMRGet(indicID = "", indicName = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人全国宏观年度数据。历史数据从1949年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataHgndACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataHgndACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataHgndACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroDataHgydACMRGet(indicID = "", indicName = "", beginDate = "", endDate = "", field = "", pandas = "1"):
    """
    华通人全国宏观月度数据。历史数据从1978年开始。
    
    :param indicID: 指标代码，可多值输入。,可以是列表,indicID、indicName至少选择一个
    :param indicName: 指标名称，可模糊查询,indicID、indicName至少选择一个
    :param beginDate: 开始日期，所查询的指标数据起始时间，输入格式“YYYYMMDD”,可空
    :param endDate: 截止日期，所查询的指标数据结束时间，输入格式“YYYYMMDD”,可空
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
    requestString.append('/api/macro/getMacroDataHgydACMR.csv?ispandas=1&') 
    requestString.append("indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s"%(beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s"%(endDate))
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
            api_base.handle_error(csvString, '__MacroDataHgydACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroDataHgydACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'indicName', u'periodDate', u'dataValue', u'unit', u'dataSourceCD', u'dataSource', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'indicID': 'str','indicName': 'str','unit': 'str','dataSourceCD': 'str','dataSource': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroInfoDataACMRGet(dbCode = "", indicID = "", indicName = "", field = "", pandas = "1"):
    """
    包含最近一期华通人库的全国宏观指标数据，划分为宏观月度数据hgyd、宏观季度数据hgjd、宏观年度数据hgnd。输入数据库代码、指标代码或指标名称，可获取指标名称、指标频度、单位、是否目录、层级、注释以及最近一期数据。
    
    :param dbCode: 数据库代码，包含宏观月度(hgyd)、宏观季度(hgjd)、宏观年度(hgnd)、分省月度(fsyd)、分省季度(fsjd)、分省年度(fsnd)、地级市月度(djsyd)、地级市季度(djsjd)、地级市年度(djsnd)9类。,可空
    :param indicID: 指标代码，可多值输入。,可以是列表,可空
    :param indicName: 指标名称，可模糊查询。,可空
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
    requestString.append('/api/macro/getMacroInfoDataACMR.csv?ispandas=1&') 
    if not isinstance(dbCode, str) and not isinstance(dbCode, unicode):
        dbCode = str(dbCode)

    requestString.append("dbCode=%s"%(dbCode))
    requestString.append("&indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
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
            api_base.handle_error(csvString, '__MacroInfoDataACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroInfoDataACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'dbCode', u'indicID', u'indicName', u'frequency', u'unit', u'isList', u'level', u'memo', u'region', u'periodDate', u'dataValue', u'isUpdate']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'dbCode': 'str','indicID': 'str','indicName': 'str','frequency': 'str','unit': 'str','isList': 'str','memo': 'str','region': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

def __MacroInfoRRPACMRGet(dbCode = "", indicID = "", indicName = "", field = "", pandas = "1"):
    """
    包含华通人库的宏观指标数据，划分为宏观月度数据hgyd、宏观季度数据hgjd、宏观年度数据hgnd。输入数据库代码、指标代码或指标名称，可获取指标名称、指标频度、单位、是否目录、层级、注释。
    
    :param dbCode: 数据库代码，包含宏观月度(hgyd)、宏观季度(hgjd)、宏观年度(hgnd)。,可空
    :param indicID: 指标代码，可多值输入。,可以是列表,可空
    :param indicName: 指标名称，可模糊查询。,可空
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
    requestString.append('/api/macro/getMacroInfoRRPACMR.csv?ispandas=1&') 
    if not isinstance(dbCode, str) and not isinstance(dbCode, unicode):
        dbCode = str(dbCode)

    requestString.append("dbCode=%s"%(dbCode))
    requestString.append("&indicID=")
    if hasattr(indicID,'__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(indicName, str) and not isinstance(indicName, unicode):
        indicName = str(indicName)

    requestString.append("&indicName=%s"%(indicName))
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
            api_base.handle_error(csvString, '__MacroInfoRRPACMRGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, '__MacroInfoRRPACMRGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n')+1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'dbCode', u'indicID', u'indicName', u'frequency', u'unit', u'isList', u'level', u'memo', u'isUpdate']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype = {'dbCode': 'str','indicID': 'str','indicName': 'str','frequency': 'str','unit': 'str','isList': 'str','memo': 'str'},  )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()

