import os
import numpy as np
from math import isnan

from ..ufuncs import todotdict
from ..language import text
from ..utils.exceptions import AtReturnError, check_at_return_error
from ..utils.utilfunc import load_mat, run_ignore_exception
from ..utils.datetimefunc import mft_to_str_format
from ..utils.logger import user_warning, user_info, write_log

from . import atserial
from . import recv_serial

ERROR_LEVEL_NO_ERROR = 0
ERROR_LEVEL_ERROR = 1
ERROR_LEVEL_WARNING = 2
ERROR_LEVEL_INFO = 3


class GeneralRes:
    """对应 ATCore 的 Generalres_s 结构体"""
    __slots__ = ['errLevel', 'errCode', 'errInfo']


# noinspection PyPep8Naming
def atReturnChecker(func_name, result: 'GeneralRes'):
    """

    :param func_name: atSendCmd系列函数名
    :param result: OrderDotDict{result:, errInfo:, errCode:}
    :return
    """
    if result.errLevel == ERROR_LEVEL_ERROR:
        error_info = check_at_return_error(result.errInfo, error='ignore')
        error = text.ERROR_CODE_REASON.format(Name=func_name,
                                              Code=result.errCode,
                                              Reason=error_info)
        raise AtReturnError(error)
    elif result.errLevel == ERROR_LEVEL_WARNING and result.errInfo != '':
        error_info = check_at_return_error(result.errInfo, error='ignore')
        error = text.ERROR_CODE_REASON.format(Name=func_name,
                                              Code=result.errCode,
                                              Reason=error_info)
        user_warning(error)
    elif result.errLevel == ERROR_LEVEL_INFO and result.errInfo != '':
        error_info = check_at_return_error(result.errInfo, error='ignore')
        error = text.ERROR_CODE_REASON.format(Name=func_name,
                                              Code=result.errCode,
                                              Reason=error_info)
        user_info(error)
    else:
        pass


# noinspection PyPep8Naming
def atSendCmdAskFactor(ItemName, TargetList, dateBegin, dateEnd, dateBefore):
    func_name = 'atSendCmdAskFactor'
    atserial.ATraderAskFactor_send(ItemName, [todotdict(item) for item in TargetList], dateBegin, dateEnd, dateBefore)
    recv_serial(func_name)


# noinspection PyPep8Naming
def atSendCmdToolboxCheck(wstrLanguage, wstrToolboxVer, listSupportedCore):
    """获取AT相关信息"""

    func_name = 'atSendCmdToolboxCheck'
    atserial.ATraderToolboxCheck_send(wstrLanguage, wstrToolboxVer, listSupportedCore)
    # OrderedDotDict
    # {
    #     'result': OrderedDotDict([('result', 1), ('errCode', ''), ('errInfo', '')]),
    #     'wstrCoreVer': '3.0.006',
    #     'listSupportedToolbox': [''],
    # }
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res


# noinspection PyPep8Naming
def atSendCmdAccountNotifyReceived():
    atserial.ATraderAccountNotifyReceived_send()


# noinspection PyPep8Naming
# TODO 旧接口 等待废弃或者调整
def atSendCmdGetFutureInfo_20190920(listMkCode):
    """  向AT发送请求,获取标的的详细信息
    :param listMkCode: [{'Market':xx, 'Code'}]
    :return: info, OrderedDotDict, 包含 Key 值见 example
    example:
        dict({
            'TargetMarket':'',
            'MarginUnit':1.432111685e-315,
            'Multiple':10.0,
            'TradingFeeOpen':5.405e-05,
            'TargetCode':'',
            'LastTradingDate':20180917.0,
            'TradingFeeClose':5.405e-05,
            'TradingFeeUnit': '',
            'Type':2.0,
            'DeliveryDate':3.14337109e-315,
            'Market':'shfe',
            'LongMargin':0.19,
            'ExerciseDate':1.6067015e-317,
            'ShortMargin':0.19,
            'CMUnit':3e-323,
            'TradingFeeCloseToday':5.405e-05,
            'Code':'ru0000',
            'Name':'天胶1809',
            'ExercisePrice':8.0280138e-316,
            'CallOrPut':'',
            'ListDate':20170918.0,
            'EndDate':-1.803005481629142e-232,
            'MinMove':5.0,
            'OptionType':'',
        })

    """

    func_name = 'atSendCmdGetFutureInfo_20190920'
    atserial.ATraderGetFutureInfo_20190920_send([todotdict(item) for item in listMkCode])
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listInfo


# noinspection PyPep8Naming
def atSendCmdGetKData(targets, kFreq, kFreNum, beginDate, endDate, filledUp, fqType, noReturn):
    """ 向AT发送请求，获取指定时间段内的K 线数据
    :param targets: list, eg: [{'Market':'XXX', 'Code': 'XXX'},]
    :param kFreq: str K线的时间等级
    ::

        'min'   : 分钟
        'hour'  : 小时
        'day'   : 天
        'week'  : 周
        'month' : 月
        'year'  : 年
    :param kFreNum: int K线的频率
    :param beginDate: int 开始时间
    :param endDate:   int 结束时间
    :param filledUp:  bool True: 补齐 False: 不补齐
    :param fqType:   str 复权类型 NA: 不复权 FWard: 前复权 BWard:后复权
    :param noReturn: bool 'True':返回结果 'False':不返回结果
    :return: info, list,每个标的对应mat文件路径
    """
    func_name = 'atSendCmdGetKData'
    atserial.ATraderGetKData_send(todotdict({
        'MarketCode': [todotdict(target) for target in targets],
        'KFrequency': kFreq,
        'KFreNum': kFreNum,
        'BeginDate': beginDate,
        'EndDate': endDate,
        'FilledUp': filledUp,
        'FQ': fqType,
        'NoReturn': noReturn}))

    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.listPaths


# noinspection PyPep8Naming
def atSendCmdGetKDataMultiFilePath(targetList, kFreq, beginDate, endDate, filledUp, fqType):
    func_name = 'atSendCmdGetKDataMultiFilePath'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetKDataMultiFilePath_send(todotdict({
        'KFrequency': kFreq,
        'BeginDate': beginDate,
        'EndDate': endDate,
        'FilledUp': filledUp,
        'FQ': fqType,
        'NoReturn': False,
    }), targets_dot)

    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetKDataMulti(targetList, kFreq, beginDate, endDate, filledUp, fqType):
    """获取多个标的一个时间段的内的K线数据

    :param targetList: list  [{'Market':marketName, 'Code': CodeName },]
    :param kFreq: str K线的频率
    :param beginDate: int 起始时间
    :param endDate: int 结束时间
    :param filledUp: bool 补齐: True, 不补齐: False
    :param fqType: 复权类型: 不复权: NA, 前复权: 'FWard', 后复权: 'BWard'
    :return: info, str,主要包含如下
    ::
        K线数据的mat文件路径
    ..
    """

    func_name = 'atSendCmdGetKDataMulti'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetKDataMulti_send(todotdict({
        'KFrequency': kFreq,
        'BeginDate': beginDate,
        'EndDate': endDate,
        'FilledUp': filledUp,
        'FQ': fqType,
        'NoReturn': False}), targets_dot)

    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetNKDataMulti(targetList, kFreq, kFreNum, nCount, endDate, filledUp, fqType):
    """获取多个标的一个时间段的内的K线数据

    :param targetList: list  [{'Market':marketName, 'Code': CodeName },]
    :param kFreq: str K线的频率
    :param kFreNum: int, K线频数
    :param nCount: int N个数据
    :param endDate: int 结束时间
    :param filledUp: bool 补齐: True, 不补齐: False
    :param fqType: 复权类型: 不复权: NA, 前复权: 'FWard', 后复权: 'BWard'
    :return: info, str,主要包含如下
    ::
        K线数据的mat文件路径
    ..
    """

    func_name = 'atSendCmdGetNKDataMulti'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetNKDataMulti_send(todotdict({
        'KFrequency': kFreq,
        'NCount': nCount,
        'FreNum': kFreNum,
        'EndDate': endDate,
        'FilledUp': filledUp,
        'FQ': fqType}), targets_dot)

    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetRtData(targetList):
    """获取标的当前tick数据

    :param targetList: targetList: list[dict]  [{'Market':marketName, 'Code': CodeName },]
    :return: list of todotdict,获取的tick数据, 包含字段::

        'Market': str,
        'Code': str,
        'Isbegin': float,
        'Time': float,
        'CurrentPrice': float,
        'CurrentQuantity': float,
        'Volume': float,
        'OpenInt': float,
        'BidPrice': list of float,
        'BidVolume': list of float,
        'AskPrice': list of float,
        'AskVolume': list of float
    """

    func_name = 'atSendCmdGetRtData'
    targets_dot = [todotdict(target) for target in targetList]

    atserial.ATraderGetRtData_send(targets_dot)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listRtData


# noinspection PyPep8Naming
def atSendCmdGetCodeList(block, date):
    """发送命令,获取代码表

    :param block: str 板块信息
    :param date: int, 日期 包含 0 或者 int 表示的日期, eg: 20180630
    :return: list of todotdict, 词典字段如示例
    example:

    >>>atSendCmdGetCodeList('Index', 20180626)
    >>>[{'Code': '000001', 'Market': 'szse', 'Weight': 0.79, 'Name': '平安银行', 'BlockName': 'payh'}, ...]
    ..
    """

    func_name = 'atSendCmdGetCodeList'
    atserial.ATraderGetCodeList_send(block, date)
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetCodeListSet(block, begin_date, end_date):
    """发送命令,获取所有曾经出现在指数和行业成分股"""

    func_name = 'atSendCmdGetCodeListSet'
    atserial.ATraderGetCodeListSet_send(block, begin_date, end_date)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listCodelist


# noinspection PyPep8Naming
def atSendCmdConvertTargets(listMC=[], wstrOpFlags='czce'):
    """
    :param listMC: [{'Market': 'xxx', 'Code': 'xxx'}]
    :param wstrOpFlags: 暂时只支持：'czce', 将大商所3位标的转为4位.
    :return: 
    """

    func_name = 'atSendCmdConvertTargets'
    atserial.ATraderConvertTargets_send([todotdict(item) for item in listMC], wstrOpFlags)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listMC


# noinspection PyPep8Naming
def atSendCmdGetCurDate():
    """获取当前日期
    无参数
    :return: double 当前日期
    """
    func_name = 'atSendCmdGetCurDate'
    atserial.ATraderGetCurDate_send()
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetCurTradeDate():
    """获取当前交易日日期
    :return: double 当前交易日日期
    """

    func_name = 'atSendCmdGetCurTradeDate'
    atserial.ATraderGetCurTradeDate_send()
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetTargetIns(Market, Code, BeginDate, EndDate):
    """获取标的交易日的信息
    :param Market: str 市场类型
    ::

        'SZSE’：深圳股票
        'SSE'：上海股票
        'SHFE'：上海期货
        'DCE' ：大连商品
        'CZCE'：郑州商品
        'CFFEX'：中金所
    ..
    :param Code: str 标的代码
    :param BeginDate: double 起始时间
    :param EndDate: double 结束时间
    :return: list(dict) 交易日日期
    """

    func_name = 'atSendCmdGetTargetIns'
    atserial.ATraderGetTargetIns_send(Market, Code, BeginDate, EndDate)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listIns


# noinspection PyPep8Naming
def atSendCmdGetTargetIns_20190830(Market, Code, BeginDate, EndDate):
    """获取标的交易日的信息
    :param Market: str 市场类型
    ::

        'SZSE’：深圳股票
        'SSE'：上海股票
        'SHFE'：上海期货
        'DCE' ：大连商品
        'CZCE'：郑州商品
        'CFFEX'：中金所
    ..
    :param Code: str 标的代码
    :param BeginDate: double 起始时间
    :param EndDate: double 结束时间
    :return: list(dict) 交易日日期
    """

    func_name = 'atSendCmdGetTargetIns_20190830'
    atserial.ATraderGetTargetIns_20190830_send(Market, Code, BeginDate, EndDate)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listIns


# noinspection PyPep8Naming
def atSendCmdGetTradingTime(targetList, kFreq, beginDay, endDay):
    """ 获取标的频率周期的交易时间
    :param targetList: targetList: list[dict]  [{'Market':marketName, 'Code': CodeName },]
    :param kFreq: K线频率
    :param beginDay: 开始时间
    :param endDay: 结束时间
    :return: str, mat 文件路径 或者 at 返回的错误信息
    ::
        保存交易时间的mat文件
    ..
    """

    func_name = 'atSendCmdGetTradingTime'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetTradingTime_send(todotdict({
        'freq': kFreq,
        'beginD': beginDay,
        'endD': endDay}), targets_dot)

    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetTradingDays():
    """获取交易日期
    :return: list of double
    """

    func_name = 'atSendCmdGetTradingDays'
    atserial.ATraderGetTradingDays_send()
    tradingDays = recv_serial(func_name).result

    return tradingDays


# noinspection PyPep8Naming
def atSendCmdGetTradingDaysCondition(market, begin_day, end_day):
    """   获取交易日日期

    :param market: 市场代号
    :param begin_day: 交易日起始时间
    :param end_day: 交易日结束时间
    :return: list 指定范围内的交易日
    """

    func_name = 'atSendCmdGetTradingDaysCondition'
    atserial.ATraderGetTradingDaysByCondition_send(market, begin_day, end_day)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listDays


# noinspection PyPep8Naming
def atSendCmdGetTradeAccountHandle(name):
    """ 获取交易账号的句柄

    :param name: str 账户名称
    :return: int64 账号句柄
    """

    func_name = 'atSendCmdGetTradeAccountHandle'
    atserial.ATraderSTTRadeGetAccountHandle_send(name)
    res = recv_serial(func_name).result

    return res


# noinspection PyPep8Naming
def atSendCmdGetAccountInfo(handleList):
    """ 获取账户信息

    :param handleList: list 账户句柄列表
    :return: list(Dotdict) 账户信息列表, eg::
        [
            {
            'Handle64': 3459830459809,
            'ValidCash':10000000000000.0,
            'MarginFrozen':0.0,
            'OrderFrozen':0.0,
            'PositionProfit':0.0,
            'HandListCap':10000000000000.0
            }
        ]
    """

    func_name = 'atSendCmdGetAccountInfo'
    accounts = []
    for handle in handleList:
        atserial.ATraderSTGetAccountInfo_send(handle)
        AccountInfo = recv_serial(func_name).result
        AccountInfo.Handle64 = handle
        accounts.append(AccountInfo)

    return accounts


# noinspection PyPep8Naming
def atSendCmdGetPreTradeDate():
    """ 获取当前日期迁移交易日的日期
    :return: double 前一交易日的日期
    """

    func_name = 'atSendCmdGetPreTradeDate'
    atserial.ATraderGetPreTradeDate_send()
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetFundamentalSet(targetList, CatName, ItemList, BeginDate, EndDate):
    """  根据标的的资产，表名，字段名，开始结束日期获取数据库中的日期序列数据
    :param targetList: targetList: list[dict]  [{'Market':marketName, 'Code': CodeName },] 标的列表
    :param CatName: str 表名
    :param ItemList: str字段名
    :param BeginDate: int 开始日期
    :param EndDate: int 结束日期
    :return: list(Dotdict) 相关表时间序列信息
    """
    func_name = 'atSendCmdGetFundamentalSet'
    targets_dot = []
    for target in targetList:
        targets_dot.append(todotdict(target))

    atserial.ATraderGetFundamentalSet_send(CatName, targets_dot, ItemList, BeginDate, EndDate)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    mat_data = load_mat(res.wstrFilePath, error='raise')

    return mat_data


# noinspection PyPep8Naming
def atSendCmdGetHistoryInstruments(targets, begin_date, end_date, fq_type='NA'):
    """ 获取日频交易信息
    :param targets: [{'Market':'xxx', 'Code': 'XXX'}]
    :param begin_date: int, 类似：20190429
    :param end_date: int, 类似：20190429
    :param fq_type: str, 支持： NA, FWard, BWard
    :return:
    """

    func_name = 'atSendCmdGetHistoryInstruments'
    targets_dot = [todotdict(target) for target in targets]
    atserial.ATraderGetHistoryInstruments_send(targets_dot, begin_date, end_date, fq_type)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    data = load_mat(res.wstrFilePath)
    return_keys = set([str.lower('%s_%s_%d' % (target['Market'], target['Code'], idx)) for idx, target in enumerate(targets)])
    result = {str.upper('.'.join(key.split('_')[:2])): data[key] for key in return_keys if key in data}

    return result


# noinspection PyPep8Naming
def atSendCmdGetFactor(FactorName, targetList, BeginDate, EndDate, NDaysBefore):
    """获取标的的因子信息
    :param FactorName: str 因子名称
    :param targetList: targetList: list[dict]  [{'Market':marketName, 'Code': CodeName },] 标的列表
    :param BeginDate: int 开始日期
    :param EndDate: int 结束日期
    :param NDaysBefore: int
    :return:
    """

    func_name = 'atSendCmdGetFactor'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetFactor_send(FactorName, targets_dot, BeginDate, EndDate, NDaysBefore)

    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetFactorMultiFilePath(list_factor_name, TargetList, BeginDate, EndDate, DaysBefore=0):
    """ 根据因子列表和标的列表获取对应的因子矩阵

    :param list_factor_name: list of str 因子列表
    :param TargetList: [{'Market':'', 'Code': ''}]
    :param BeginDate: int
    :param EndDate: int
    :param DaysBefore: int
    :return: mat_files: 文件路径0
    """

    func_name = 'atSendCmdGetFactorMultiFilePath'
    atserial.ATraderGetFactorMultiFilePath_send(list_factor_name, [todotdict(target) for target in TargetList], BeginDate, EndDate, DaysBefore)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listPaths


# noinspection PyPep8Naming
def atSendCmdGetHistorySet(Market, Code, CatName, ItemName, BeginDate, EndDate):
    """  根据标的的资产，表名，字段名，开始日期和结束日期获取数据库中的日期序列数据
    :param Market: str 市场类型
    ::

        'SZSE’：深圳股票
        'SSE'：上海股票
        'SHFE'：上海期货
        'DCE' ：大连商品
        'CZCE'：郑州商品
        'CFFEX'：中金所
    ..
    :param Code: str 标的代码
    :param CatName: str 表名
    :param ItemName: 字段名
    :param BeginDate: 开始时间
    :param EndDate: 结束时间
    :return: list(Dotdict) 相关表时间序列信息
    """
    #  marketCode 是list
    func_name = 'atSendCmdGetHistorySet'

    market_code = [todotdict({'Market': Market, 'Code': Code})]
    atserial.ATraderGetHistorySet_send(CatName, ItemName, market_code, BeginDate, EndDate)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    mat_data = load_mat(res.wstrFilePath, error='raise')

    return mat_data


# noinspection PyPep8Naming
def atSendCmdGetMarketSet(wstrCat, listItem, iBeginDate, iEndDate):
    """ 根据表名， 字段名，开始日期和结束日期获取数据库中与整体市场有关的日期序列数据
    :param wstrCat: str 表名
    :param listItem: str 字段名
    :param iBeginDate: int 开始时间
    :param iEndDate: int 结束时间
    :return: list(Dotdict) 相关表时间序列信息
    """

    func_name = 'atSendCmdGetMarketSet'
    atserial.ATraderGetMarketSet_send(wstrCat, listItem, iBeginDate, iEndDate)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    mat_data = load_mat(res.wstrFilePath, error='raise')

    return mat_data


# noinspection PyPep8Naming
def atSendCmdGetOptionData(market, code):
    """ 获取期权的数据

    :param market: 市场类型
    :param code: 标的代码
    :return: Dotdict 期权数据, 包含字段::

        'ImpliedVolativity': float,
        'BidPrice': float,
        'BidVolume': float,
        'AskPrice': float,
        'AskVolume': float,
        'CurrentPrice': float,
        'OpenInterest': float,
        'UnderlyCurrentPrice': float,
        'RemainDays': float,
        'InterestRate': float,
        'StrikePrice': float,
        'Type': float,
    ..
    """

    func_name = 'atSendCmdGetOptionData'
    atserial.ATraderGetOptionData_send(market, code)
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetOptionInfo(market, code):
    """ 获取期权信息
    :param market: str 市场类型
    :param code: str 标的代码
    :return: Dotdict 期权信息
    ::
        TODO 期权接口
    ...
    """

    func_name = 'atSendCmdGetOptionInfo'
    atserial.ATraderGetOptionInfo_send(market, code)
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetOptionPos(market, code):
    """ 获取期权...信息
    :param market: str 市场类型
    :param code: str 标的代码
    :return: Dotdict 期权...信息
    ::
        TODO 期权接口
    ..
    """

    func_name = 'atSendCmdGetOptionPos'
    atserial.ATraderGetOptionPos_send(market, code)
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdGetTDPData(market, code, date, fqType, no_return, check_permission=True):
    func_name = 'atSendCmdGetTDPData'
    atserial.ATraderGetTDPData_send(todotdict({
        'Market': market,
        'Code': code,
        'Date': date,
        'FQ': fqType,
        'NoReturn': no_return,
        'CheckPermission': check_permission}))
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    mat_path = res.wstrFilePath

    return mat_path


# noinspection PyPep8Naming
def atSendCmdGetTDPDataMultiFilePath(targetList, beginDate, endDate, fqType):
    func_name = 'atSendCmdGetTDPDataMultiFilePath'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetTDPDataMultiFilePath_send(targets_dot, beginDate, endDate, fqType)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetTDPDataMulti(targetList, beginDate, endDate, fqType):
    """获取 tick 数据

    :param targetList: list of dict, 标的列表
    :param beginDate: int, 开始日期, 20180709
    :param endDate: int, 结束日期, eg: 20180710
    :param fqType: str, str, 复权类型
    :return: str, 文件路径 或者 错误字符串, 需要检查错误信息
    """

    func_name = 'atSendCmdGetTDPDataMulti'
    targets_dot = [todotdict(target) for target in targetList]
    atserial.ATraderGetTDPDataMulti_send(targets_dot, beginDate, endDate, fqType)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.wstrFilePath


# noinspection PyPep8Naming
# TODO 期权接口
def atSendCmdGetOptionCode(varargin):
    """ 获取期权的...
    :param varargin: list
    :return:
    """

    func_name = 'atSendCmdGetOptionCode'
    if len(varargin) is 8:
        Market = varargin[0]
        Code = varargin[1]
        Price = varargin[2]
        Month = varargin[3]
        Type = varargin[4]
        ValueType = varargin[5]
        Level = varargin[6]
        ContractAdjustmentType = varargin[7]
        atserial.ATraderGetOptionCode_send(todotdict({
            'Market': Market,
            'Code': Code,
            'Price': Price,
            'Month': Month,
            'Type': Type,
            'ValueType': ValueType,
            'Level': Level,
            'BDate': '',
            'EDate': '',
            'ContractAdjustmentType': ContractAdjustmentType}))
    elif len(varargin) is 5:
        Market = varargin[0]
        Code = varargin[1]
        BDate = varargin[2]
        EDdate = varargin[3]
        ContractAdjustmentType = varargin[4]
        atserial.ATraderGetOptionCode_send(todotdict({
            'Market': Market,
            'Code': Code,
            'Price': 0,
            'Month': 0,
            'Type': '',
            'ValueType': '',
            'Level': 0,
            'BDate': BDate,
            'EData': EDdate,
            'ContractAdjustmentType': ContractAdjustmentType}))
    else:
        raise ValueError(text.ERROR_PARAM_MISMATCH_5_8)

    res = recv_serial(func_name).result
    return res


# noinspection PyPep8Naming
def atSendCmdGetStopOrderInfo(account_handle, stop_order_id_s):
    """ 获取止损止盈单的信息
    """

    func_name = 'atSendCmdGetStopOrderInfo'
    atserial.ATraderGetStopOrderInfo3_1_4_send(account_handle, stop_order_id_s)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listStopOrderInfo


# noinspection PyPep8Naming
def atSendCmdSTTradeStopOrder(params):
    """  发送策略测试的止损止盈单
    :param params: dict 订单信息，包含字段::

        StrategyName: str 策略名
        Handle: double 账户句柄
        Market: str 市场类型
        Code: str 标的代码
        Contracts: double 合约数量
        StopGap: double 开始跟踪止盈的价格
        OrderAct: str 买入: 'buy' 卖出: 'sell'
        OrderCtg: str 下单价格类型 市价: 'market'  限价: 'limit'
        TargetPrice: double 基准价格
        targetOrderID: double 止盈止损针对的单号
        StopBy: str 止盈类型 按照价格点数止盈: 'Point' 按照价格变动百分比: 'Percent'
        StopType: str 下单类型
        TrailingStopGap: double 回测条件
        TrailingStopBy: str 回测类型 按照价格点数止盈: 'Point' 按照价格变动百分比: 'Percent'
        OrderTag: str 订单标记

    :return: dict, 包含字段::
        result: bool, 订单状态
        ClientID: int, 订单 ID
        errCode: int, 错误代码
        errInfo: str, 错误信息

    """

    func_name = 'atSendCmdSTTradeStopOrder'
    atserial.ATraderSTTradeStopOrder_send(todotdict(params))
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.ClientID


# noinspection PyPep8Naming
def atSendCmdSTTradeOperation(params):
    """  发送交易单请求
    :param params: dict , 包含字段::

        StrategyName: str 策略名称
        Handle: double 账户句柄
        Market: str 市场类型
        Code: str 标的代码
        Contracts: double 合约数量
        Price: double 基准价格(市价单的时候为0.0)
        OrderAct: str 买入: 'buy': 1  卖出: 'sell': 0
        OrderCtg: str 下单价格类型 市价: 'market': 1  限价: 'limit': 0
        OffsetFlag: 平仓 close: 0 开仓 open: 1
        OrderTag: str 订单标记

    :return: dotdict, 包含字段::
        'result': bool,
        'ClientID': int,
        'errCode': str,
        'errInfo': str
    """

    func_name = 'atSendCmdSTTradeOperation'
    atserial.ATraderSTTradeOperation_send(todotdict(params))
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.ClientID


# noinspection PyPep8Naming
def atSendCmdSTOrderInfo(handles: 'list', order_ids: 'list'):
    """获取账户对应订单信息"""

    func_name = 'atSendCmdSTOrderInfo'
    atserial.ATraderGetOrderInfo_send(handles, order_ids)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listOrders


# noinspection PyPep8Naming
def atSendCmdSTUnFinishedOrderInfo(handles: 'list', order_dates):
    func_name = 'atSendCmdSTUnFinishedOrderInfo'
    atserial.ATraderGetUnFinishedOrderInfo_send(handles, order_dates)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listOrders


# noinspection PyPep8Naming
def atSendCmdSTGetOrderInfoByDate(handles: 'list', order_dates):
    func_name = 'atSendCmdSTDailyOrderInfo'
    atserial.ATraderGetOrderInfoByDate_send(handles, order_dates)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listOrders


# noinspection PyPep8Naming
def atSendCmdSTGetLastOrderInfo(handle, targets, order_side, position_effect):
    func_name = 'atSendCmdSTGetLastOrderInfo'
    atserial.ATraderGetLastOrderInfo_send(handle, targets, order_side, position_effect)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listOrders


# noinspection PyPep8Naming
def atSendCmdSTGetExecutionInfo(handles, dates):
    func_name = 'atSendCmdSTGetExecutionInfo'
    atserial.ATraderGetDailyExecution_send(handles, dates)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listExecutions


# noinspection PyPep8Naming
def atSendCmdSTGetLastExecutionInfo(handle, target, side, position_effect):
    func_name = 'atSendCmdSTGetLastExecutionInfo'
    atserial.ATraderGetLastExecution_send(handle, target, side, position_effect)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listExecutions


# noinspection PyPep8Naming
def atSendCmdGetAccountConfig(strategyName, handle):
    """获取配置参数

    :param strategyName: str, 策略名
    :param handle: int, 账户句柄
    :return: list of todotdict, eg: [{'Code': 'a0000', 'Market': 'dce', 'Config': 0.2}]
    """

    func_name = 'atSendCmdGetAccountConfig'
    atserial.ATraderGetAccountConfig_send(strategyName, handle)
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdSetAccountConfigTo(strategyName, handle, target_configs):
    """ 调整账户某个标的的仓位，仅可以在回测中使用

    :param strategyName: str 策略名
    :param handle: double 账号句柄
    :param target_configs: list 调整仓位量, eg: [{'Market':Market, 'Code':Code, 'Config': Config },]
    :return:
    """

    atserial.ATraderSetAccountConfigTo_send(strategyName, handle, [todotdict(item) for item in target_configs])


# noinspection PyPep8Naming
def atSendCmdGetDatePeriodBarTime(allTargetLists, KFrequency, KFreNum, endtm):
    """
    :param allTargetLists: list of dict, 标的列表
    :param KFrequency: str, 频率
    :param KFreNum: int， 频数
    :param endtm: int, 结束日期
    :return: np.ndarray, 时间数据
    :raise AtReturnError, ValueError, DataLoadError
    """

    func_name = 'atSendCmdGetDatePeriodBarTime'
    min_market = [todotdict(val) for val in allTargetLists if val['Market'] not in ['sse', 'szse']]

    for val in allTargetLists:
        if val['Market'] in ['sse', 'szse']:
            min_market.append(todotdict(val))
            break

    atserial.ATraderBarTime_send(endtm, KFrequency, KFreNum, min_market)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    mat_file = res.wstrFileName
    if np.logical_not(endtm) and os.path.exists(mat_file):
        run_ignore_exception(os.remove, mat_file)

    mat_data = load_mat(mat_file, error='raise')
    all_time_bar = mat_data.get('Time')

    return all_time_bar


# noinspection PyPep8Naming
def atSendCmdIsAccountValid(handle):
    """ 判断账户是否有效

    :param handle: double　账户类型
    :return:
    """

    func_name = 'atSendCmdIsAccountValid'
    atserial.ATraderIsAccountValid_send(handle)
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdSubscribeAccount(accountID):
    """ 订阅账户
    :param accountID: double 账户句柄
    :return:
    """
    atserial.ATraderSubscribeAccount_send(accountID)


# noinspection PyPep8Naming
def atSendCmdUnsubscribeAccount(accountIDs):
    """ 解订账户
    :param accountIDs: 账户句柄
    :return:
    """
    atserial.ATraderUnsubscribeAccount_send(accountIDs)


# noinspection PyPep8Naming
def atSendCmdSubscribeFactor(MarketCodes, Factors):
    """ 订阅因子

    :param MarketCodes: list(dict) 市场代码列表
    :param Factors: list(str) 因子名列表
    :return:
    """

    if len(MarketCodes) == 0 or len(Factors) == 0:
        return

    market_code_list = [todotdict({'Idx': idx, 'Market': item['Market'], 'Code': item['Code']}) for idx, item in
                        enumerate(MarketCodes)]
    factor_list = [todotdict({'Idx': idx, 'FactorName': factor}) for idx, factor in enumerate(Factors)]
    atserial.ATraderSubscribeFactor_send(market_code_list, factor_list)


# noinspection PyPep8Naming
def atSendCmdUnsubscribeFactor(marketCode, FactorName):
    """ 解订因子
    :param marketCode: list(dict) 市场代码列表
    :param FactorName: str 因子名
    :return:
    """
    market_code_list = [todotdict({'Idx': idx, 'Market': marketCode[idx]['Market'], 'Code': marketCode[idx]['Code']})
                        for
                        idx in range(len(marketCode))]
    atserial.ATraderUnsubscribeFactor_send(market_code_list, FactorName)


# noinspection PyPep8Naming
def atSendCmdSubscribeIns(marketCode, kFreq):
    """ 订阅标的的K线数据
    :param marketCode: list(dict) 市场代码列表
    :param kFreq: str K线的频率
    :return:
    """
    market_code_list = [todotdict({'Idx': idx, 'Market': marketCode[idx]['Market'], 'Code': marketCode[idx]['Code']}) for idx in range(len(marketCode))]
    atserial.ATraderSubscribeIns_send(market_code_list, kFreq)


# noinspection PyPep8Naming
def atSendCmdUnsubscribeIns(marketCode, kFreq):
    """ 解订标的的K线数据
    :param marketCode: list(dict) 市场代码列表
    :param kFreq: str K线的频率
    :return:
    """
    market_code_list = [todotdict({'Idx': idx, 'Market': marketCode[idx]['Market'], 'Code': marketCode[idx]['Code']})
                        for
                        idx in range(len(marketCode))]
    atserial.ATraderUnsubscribeIns_send(market_code_list, kFreq)


# noinspection PyPep8Naming
def atSendCmdCheckSubscribeNum(Frequency, SubscribeNum):
    func_name = 'atSendCmdCheckSubscribeNum'
    atserial.ATraderCheckSubscribeNum_send(Frequency, SubscribeNum)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdSTGetAccountPosition(Handle, Market, Code, LongShort=None):
    """获取仓位信息

    :param Handle: int64 账户句柄
    :param Market: str, 市场
    :param Code: str, code
    :param LongShort: str or None, str包括: 'Long', 'Short'
    :return: todotdict, 仓位信息::

        todotdict{
        'Frozen':0.0,
        'Direction':'',
        'Position':-1600.0,
        'AvgPrice':3679.0,
        'Symbol':'a1809',
        'Market':'dce'
        }

    .. Note:: ATCore 那边若没有查询到持仓, Market,Code,Direction 均为 '', Position, Frozen, AvgPrice 为 0
    """

    func_name = 'atSendCmdSTGetAccountPosition'
    LongShort = '' if LongShort is None else LongShort
    atserial.ATraderSTGetAccountPosition_send(todotdict({'Handle': Handle,
                                                         'Market': Market,
                                                         'Code': Code,
                                                         'LongShort': LongShort}))
    info = recv_serial(func_name).sPositionData
    return info.Position, info.Frozen, info.AvgPrice


# noinspection PyPep8Naming
def atSendCmdSTTradeGetAccountList():
    """ 获取策略测试的账户列表信息
    :return: list of todotdict, eg: [todotdict{'Name':'', 'Handle':xxx, 'Status':'online'}]
    """

    func_name = 'atSendCmdSTTradeGetAccountList'
    atserial.ATraderSTTradeGetAccountList_send()
    res = recv_serial(func_name)

    return res.result


# noinspection PyPep8Naming
def atSendCmdRiseError(i64TaskId, e):
    """向 ATCore 发送错误消息

    :param i64TaskId: int64, ATCore返回的 taskId
    :param e:  str 错误信息内容
    :return:
    """

    if isnan(i64TaskId):
        return
    atserial.ATraderRiseError_send(i64TaskId, str(e))


# noinspection PyPep8Naming
def atSendCmdPutLog(i64TaskId, log):
    """ 发送日志消息

    :param i64TaskId: int64, ATCore返回的 taskId
    :param log: str 日志内容
    :return: None
    """

    if isnan(i64TaskId):
        return
    atserial.ATraderPutLog_send(i64TaskId, log)
    write_log(log, level='info', console=log)


# noinspection PyPep8Naming
def atSendCmdTest(cmd_name: 'str', params: 'list'):
    """ 发送测试命令，方便调试 ATCore
    """

    func_name = 'atSendCmdTest'
    atserial.ATraderCmdTest_send(cmd_name, params)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listResult


# noinspection PyPep8Naming
def atSendCmdKeepActive():
    """ 发送心跳包
    :return:
    """

    atserial.ATraderKeepActive_send()


# noinspection PyPep8Naming
def atSendCmdRtNotifyReceived():
    """ 发送实时数据接收完毕的反馈包
    :return:
    """

    atserial.ATraderRtNotifyReceived_send()


# noinspection PyPep8Naming
def atSendCmdIsMTFundmental(CatName, ItemName):
    """
    :param CatName: str 表名
    :param ItemName: str 字段名
    :return:
    """

    func_name = 'atSendCmdIsMTFundmental'
    atserial.ATraderIsMTFundmental_send(CatName, ItemName)
    res = recv_serial(func_name)

    return res.IsMTFundmental


# noinspection PyPep8Naming
def atSendCmdCloseOperation(strategy_name, i64Handle):
    """
    :param strategy_name: str 策略名称
    :param i64Handle: int64  账户句柄
    :return:
    """

    atserial.ATraderCloseOperation_send(strategy_name, np.int64(i64Handle))


# noinspection PyPep8Naming
def atSendCmdCancelFrozen(Handle):
    """
    :param Handle: int 账户句柄
    :return:
    """
    atserial.ATraderCancelFrozen_send(Handle)


# noinspection PyPep8Naming
def atSendCmdTransTradeTimeToTradeDate(checkTime):
    """ 将时间转换为 yyyymmdd 形式的double类型
    :param checkTime: double 时间
    :return: double  yyyymmdd 形式的时间表示
    """

    func_name = 'atSendCmdTransTradeTimeToTradeDate'
    daytime_str = mft_to_str_format(checkTime, '%Y%m%dT%H%M%S')
    atserial.ATraderTransTradeTimeToTradeDate_send(daytime_str)
    trade_date = recv_serial(func_name).result

    return trade_date


# noinspection PyPep8Naming
def atSendCmdCancelOrder(strategyName, handle, orderID):
    """ 发送停止订单的请求
    :param strategyName: str 策略名称
    :param handle:  int 账户句柄
    :param orderID: int 订单号
    :return:
    """

    atserial.ATraderCancelOrder_send(strategyName, handle, orderID)


# noinspection PyPep8Naming
def atSendCmdCancelStopOrder(strategyName, handle, orderID):
    """ 发送停止止损单的请求
    :param strategyName: str 策略名称
    :param handle: int 账户句柄
    :param orderID: int 订单号
    :return: bool,
    """

    func_name = 'atSendCmdCancelStopOrder'
    atserial.ATraderCancelStopOrder_send(strategyName, handle, orderID)
    res = recv_serial(func_name)

    return res.bResult


# noinspection PyPep8Naming
def atSendCmdCreateTaskBackTest(HandleList, TargetList, params):
    """ 执行回测
    :param HandleList: list(int) 账户列表
    :param TargetList: list(dict)标的列表
    :param params: str 其他参数
    :return:
    """

    func_name = 'atSendCmdCreateTaskBackTest'
    targets = [todotdict(target) for target in TargetList]

    atserial.ATraderCreateTaskBackTest_send(todotdict(params), HandleList, targets)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return np.int64(res.i64TaskID)


# noinspection PyPep8Naming
def atSendCmdStartTaskBackTest(i64TaskId):
    """ 开始回测任务

    :param i64TaskId: int64, ATCore返回的 taskId
    """

    if isnan(i64TaskId):
        return

    func_name = 'atSendCmdStartTaskBackTest'
    atserial.ATraderStartTaskBackTest_send(i64TaskId)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdStopTaskBackTest(i64TaskId, targetList, positionList, params):
    """ 停止回测
    :param i64TaskId: task id
    :param targetList: list(dict) 标的列表
    :param positionList: 仓位信息
    :param params: dict 其他参数
    :return:
    """
    if isnan(i64TaskId):
        return

    func_name = 'atSendCmdStopTaskBackTest'
    mk = [todotdict({'Idx': idx, 'Market': t['Market'], 'Code': t['Code']}) for idx, t in enumerate(targetList)]
    atserial.ATraderStopTaskBackTest_send(i64TaskId, todotdict(params), mk, list(map(todotdict, positionList)))
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdCreateTaskRealTrade(params: 'dict'):
    """ 开始实盘测试

    :param params: DotDict/dict, 包含参数::

        StraName: str 策略名称
        begin: int, 8位的日期, eg: 20180709
        KFrequency: str, `频率`
        KFreNum: int, `频数`
        TargetList: list(dict) 标的列表
        HandleList: 账户句柄

    """

    func_name = 'atSendCmdCreateTaskRealTrade'
    targets = [todotdict(item) for item in todotdict(params).TargetList]
    atserial.ATraderCreateTaskRealTrade_send(todotdict(params), params['HandleList'], targets)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return np.int64(res.i64TaskID)


# noinspection PyPep8Naming
def atSendCmdStartTaskRealTrade(i64TaskId):
    if isnan(i64TaskId):
        return

    func_name = 'atSendCmdStartTaskRealTrade'
    atserial.ATraderStartTaskRealTrade_send(i64TaskId)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdStopTaskRealTrade(i64TaskID, strategy_name, handles):
    """ 停止实盘测试
    :param i64TaskID: int64: 任务ID
    :param strategy_name:str 策略名称
    :param handles: list(double) 账户句柄列列表
    :return:
    """

    func_name = 'atSendCmdStopTaskRealTrade'
    atserial.ATraderStopTaskRealTrade_send(i64TaskID, strategy_name, handles)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdCreateTaskRunFactor(params: 'dict'):
    """ 开始因子计算模式

    :param params: DotDict/dict, 包含参数::

      StraName: str, 策略名称
      StraPath: str, 策略路径
      IndexName: str, get_code_list 参数
      ToolBoxDesc: str, 描述信息
      BeginDate: int, 开始日期
      EndDate: int, 结束日期
    """

    func_name = 'atSendCmdCreateTaskRunFactor'
    new_params = todotdict({
        'wstrFactorName': params['StraName'],
        'wstrSrcPath': params['StraPath'],
        'wstrIndexPlateName': params['IndexName'],
        'wstrToolBoxDes': params['ToolBoxDesc'],
        'iBegin': params['BeginDate'],
        'iEnd': params['EndDate'],
    })
    atserial.ATraderCreateTaskRunFactor_send(new_params)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return np.int64(res.i64TaskID)


# noinspection PyPep8Naming
def atSendCmdStartTaskRunFactor(i64TaskId):
    if isnan(i64TaskId):
        return

    func_name = 'atSendCmdStartTaskRunFactor'
    atserial.ATraderStartTaskRunFactor_send(i64TaskId)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdStopTaskRunFactor(i64TaskId, record_dir):
    if isnan(i64TaskId):
        return

    func_name = 'atSendCmdStopTaskRunFactor'
    atserial.ATraderStopTaskRunFactor_send(i64TaskId, record_dir)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdGetFutureInfoExculusively(targets):
    """ 获取期货相关信息

    :param targets: 标的索引
    :return:
    """

    func_name = 'atSendCmdGetFutureInfoExculusively'
    atserial.ATraderGetFutureInfoExculusively_send([todotdict(target) for target in targets])
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listFutureInfoExcu


# noinspection PyPep8Naming
def atSendCmdGetFutureInfoExculusively_20190918(targets):
    """ 获取期货相关信息

    :param targets: 标的索引
    :return:
    """

    func_name = 'atSendCmdGetFutureInfoExculusively_20190918'
    atserial.ATraderGetFutureInfoExculusively_20190918_send([todotdict(target) for target in targets])
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listFutureInfoExcu


# noinspection PyPep8Naming
def atSendCmdGetAccountTargetGrossPosition(handles, targets):
    """ 获取仓位相关信息

    :param handles: 账户handle
    :param targets: [{'Market': xx, 'Code': xx}]
    :return:
    """

    func_name = 'atSendCmdGetAccountTargetGrossPosition'
    atserial.ATraderGetAccountTargetGrossPosition_send(handles, [todotdict(target) for target in targets])
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listGrossPosition


# noinspection PyPep8Naming
def atSendCmdGetAccountCash(handles):
    func_name = 'atSendCmdGetAccountCash'
    atserial.ATraderGetAccountCash_send(handles)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.listAccountCash


# noinspection PyPep8Naming
def atSendCmdGetAccountPositionAndCash(handles, targets):
    func_name = 'atSendCmdGetAccountPositionAndCash'
    atserial.ATraderGetAccountPositionAndCashInfo_send(handles, [todotdict(target) for target in targets])
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.listAccountCash, res.listGrossPosition


# noinspection PyPep8Naming
def atSendCmdGetToolBoxRootofCacheDir():
    func_name = 'atSendCmdGetToolBoxRootofCacheDir'
    atserial.ATraderGetToolBoxRootofCacheDir_send()
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.wstrRootCacheDir


# noinspection PyPep8Naming
def atSendCmdGetStockInfoExculusively(targets):
    """ 获取股票相关的信息

    :param targets:  标的索引
    :return:
    """

    func_name = 'atSendCmdGetStockInfoExculusively'
    atserial.ATraderGetStockInfoExculusively_send([todotdict(target) for target in targets])
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listStockInfoExcu


# noinspection PyPep8Naming
def atSendCmdFdmtFieldInfo(fdmt_fields: 'list'):
    func_name = 'atSendCmdFdmtFieldInfo'
    atserial.ATraderFdmtFieldInfo_send(fdmt_fields)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdGetFdmt(lang, func, params_str):
    func_name = 'atSendCmdFdmtFieldInfo'
    atserial.ATraderGetFundamentalSet2_send(lang, func, params_str)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdRiskModelFieldInfo(fdmt_fields: 'list'):
    func_name = 'atSendCmdRiskModelFieldInfo'
    atserial.ATraderRiskModelFieldInfo_send(fdmt_fields)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)


# noinspection PyPep8Naming
def atSendCmdGetRiskModel(lang, func, params_str):
    func_name = 'atSendCmdGetRiskModel'
    atserial.ATraderGetRiskModelSet_send(lang, func, params_str)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.wstrFilePath


# noinspection PyPep8Naming
def atSendCmdGetStrategyID():
    func_name = 'atSendCmdGetStrategyID'
    atserial.ATraderGetStrategyID_send()
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.listStrategyInfo


# noinspection PyPep8Naming
def atSendCmdGetBackTestPerformance(i64TaskID):
    func_name = 'atSendCmdGetBackTestPerformance'
    atserial.ATraderGetBackTestPerformance_send(i64TaskID)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)
    return res.listDetail


# noinspection PyPep8Naming
def atSendCmdSubscribeInstrument(MarketCodes):
    market_code_list = [todotdict({'Idx': idx, 'Market': item['Market'], 'Code': item['Code']}) for idx, item in
                        enumerate(MarketCodes)]
    atserial.ATraderSubscribeInstrument_send(market_code_list)


# noinspection PyPep8Naming
def atSendCmdUnsubscribeInstrument():
    atserial.ATraderUnsubscribeInstrument_send()


# noinspection PyPep8Naming
def atSendCmdGetFutureContracts(i64Date, wstrMarket, wstrVarieties):
    """ 获取期货可交易合约

    :param i64Date: 查询日期
    :param wstrMarket: 目标市场
    :param wstrVarieties: 目标品种
    :return:
    """

    func_name = 'atSendCmdGetFutureContracts'
    atserial.ATraderGetFutureContracts_send(i64Date, wstrMarket, wstrVarieties)
    res = recv_serial(func_name)
    atReturnChecker(func_name, res.result)

    return res.listComp

