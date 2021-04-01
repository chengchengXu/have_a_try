# coding: utf-8
import json
from ..utils.datetimefunc import mft_to_str_format
from ..ufuncs import todotdict


class DataAPIServer(HttpBaseCmd):
    _endpoint = "DataAPIServer"

    def __init(self, uri, **kwargs):
        super().__init__(url=f"http://{DataAPIServer._endpoint}{uri}", **kwargs)


class GetFutureInfo_20190920(DataAPIServer):
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

    uri = r'ATraderGetFutureInfo_20190920'

    def __init__(self):
        super().__init__(uri=GetFutureInfo_20190920.uri, mode="post", pack=GetFutureInfo_20190920.pack)

    @staticmethod
    def send(listMkCode, **kwargs):
        if not hasattr(GetFutureInfo_20190920, 'cmd'):
            GetFutureInfo_20190920.cmd = GetFutureInfo_20190920()
        return super(GetFutureInfo_20190920, GetFutureInfo_20190920.cmd).send(listMkCode=listMkCode, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetFutureInfo_20190920_send([todotdict(item) for item in listMkCode])
        """
        return json.dumps(kwargs)


class GetKData(DataAPIServer):
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

    uri = r'ATraderGetKData'

    def __init__(self):
        super().__init__(uri=GetKData.uri, mode="post", pack=GetKData.pack)

    @staticmethod
    def send(targets, kFreq, kFreNum, beginDate, endDate, filledUp, fqType, noReturn, **kwargs):
        if not hasattr(GetKData, 'cmd'):
            GetKData.cmd = GetKData()
        return super(GetKData, GetKData.cmd).send(targets=targets, kFreq=kFreq, kFreNum=kFreNum, beginDate=beginDate, endDate=endDate, filledUp=filledUp, fqType=fqType, noReturn=noReturn, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetKData_send(todotdict({'MarketCode': [todotdict(target) for target in targets],'KFrequency': kFreq,'KFreNum': kFreNum,'BeginDate': beginDate,'EndDate': endDate,'FilledUp': filledUp,'FQ': fqType,'NoReturn': noReturn}))
        """
        return json.dumps(kwargs)


class GetKDataMulti(DataAPIServer):
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

    uri = r'ATraderGetKDataMulti'

    def __init__(self):
        super().__init__(uri=GetKDataMulti.uri, mode="post", pack=GetKDataMulti.pack)

    @staticmethod
    def send(targetList, kFreq, beginDate, endDate, filledUp, fqType, **kwargs):
        if not hasattr(GetKDataMulti, 'cmd'):
            GetKDataMulti.cmd = GetKDataMulti()
        return super(GetKDataMulti, GetKDataMulti.cmd).send(targetList=targetList, kFreq=kFreq, beginDate=beginDate, endDate=endDate, filledUp=filledUp, fqType=fqType, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetKDataMulti_send(todotdict({'KFrequency': kFreq,'BeginDate': beginDate,'EndDate': endDate,'FilledUp': filledUp,'FQ': fqType,'NoReturn': False}), targets_dot)

        targets_dot = [todotdict(target) for target in targetList]
        """
        return json.dumps(kwargs)


class GetNKDataMulti(DataAPIServer):
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

    uri = r'ATraderGetNKDataMulti'

    def __init__(self):
        super().__init__(uri=GetNKDataMulti.uri, mode="post", pack=GetNKDataMulti.pack)

    @staticmethod
    def send(targetList, kFreq, kFreNum, nCount, endDate, filledUp, fqType, **kwargs):
        if not hasattr(GetNKDataMulti, 'cmd'):
            GetNKDataMulti.cmd = GetNKDataMulti()
        return super(GetNKDataMulti, GetNKDataMulti.cmd).send(targetList=targetList, kFreq=kFreq, kFreNum=kFreNum, nCount=nCount, endDate=endDate, filledUp=filledUp, fqType=fqType, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetNKDataMulti_send(todotdict({'KFrequency': kFreq,'NCount': nCount,'FreNum': kFreNum,'EndDate': endDate,'FilledUp': filledUp,'FQ': fqType}), targets_dot)

        targets_dot = [todotdict(target) for target in targetList]
        """
        return json.dumps(kwargs)


class GetRtData(DataAPIServer):
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

    uri = r'ATraderGetRtData'

    def __init__(self):
        super().__init__(uri=GetRtData.uri, mode="post", pack=GetRtData.pack)

    @staticmethod
    def send(targetList, **kwargs):
        if not hasattr(GetRtData, 'cmd'):
            GetRtData.cmd = GetRtData()
        return super(GetRtData, GetRtData.cmd).send(targetList=targetList, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetRtData_send(targets_dot)

        targets_dot = [todotdict(target) for target in targetList]
        """
        return json.dumps(kwargs)


class GetCodeList(DataAPIServer):
    """发送命令,获取代码表

    :param block: str 板块信息
    :param date: int, 日期 包含 0 或者 int 表示的日期, eg: 20180630
    :return: list of todotdict, 词典字段如示例
    example:

    >>>atSendCmdGetCodeList('Index', 20180626)
    >>>[{'Code': '000001', 'Market': 'szse', 'Weight': 0.79, 'Name': '平安银行', 'BlockName': 'payh'}, ...]
    ..
    """

    uri = r'ATraderGetCodeList'

    def __init__(self):
        super().__init__(uri=GetCodeList.uri, mode="post")

    @staticmethod
    def send(block, date, **kwargs):
        if not hasattr(GetCodeList, 'cmd'):
            GetCodeList.cmd = GetCodeList()
        return super(GetCodeList, GetCodeList.cmd).send(block=block, date=date, **kwargs)


class GetCodeListSet(DataAPIServer):
    """发送命令,获取所有曾经出现在指数和行业成分股"""

    uri = r'ATraderGetCodeListSet'

    def __init__(self):
        super().__init__(uri=GetCodeListSet.uri, mode="post")

    @staticmethod
    def send(block, begin_date, end_date, **kwargs):
        if not hasattr(GetCodeListSet, 'cmd'):
            GetCodeListSet.cmd = GetCodeListSet()
        return super(GetCodeListSet, GetCodeListSet.cmd).send(block=block, begin_date=begin_date, end_date=end_date, **kwargs)


class ConvertTargets(DataAPIServer):
    """
    :param listMC: [{'Market': 'xxx', 'Code': 'xxx'}]
    :param wstrOpFlags: 暂时只支持：'czce', 将大商所3位标的转为4位.
    :return: 
    """

    uri = r'ATraderConvertTargets'

    def __init__(self):
        super().__init__(uri=ConvertTargets.uri, mode="post", pack=ConvertTargets.pack)

    @staticmethod
    def send(listMC=[], wstrOpFlags='czce', **kwargs):
        if not hasattr(ConvertTargets, 'cmd'):
            ConvertTargets.cmd = ConvertTargets()
        return super(ConvertTargets, ConvertTargets.cmd).send(listMC=listMC, wstrOpFlags=wstrOpFlags, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderConvertTargets_send([todotdict(item) for item in listMC], wstrOpFlags)
        """
        return json.dumps(kwargs)


class GetCurDate(DataAPIServer):
    """获取当前日期
    无参数
    :return: double 当前日期
    """

    uri = r'ATraderGetCurDate'

    def __init__(self):
        super().__init__(uri=GetCurDate.uri, mode="post")

    @staticmethod
    def send(**kwargs):
        if not hasattr(GetCurDate, 'cmd'):
            GetCurDate.cmd = GetCurDate()
        return super(GetCurDate, GetCurDate.cmd).send(**kwargs)


class GetCurTradeDate(DataAPIServer):
    """获取当前交易日日期
    :return: double 当前交易日日期
    """

    uri = r'ATraderGetCurTradeDate'

    def __init__(self):
        super().__init__(uri=GetCurTradeDate.uri, mode="post")

    @staticmethod
    def send(**kwargs):
        if not hasattr(GetCurTradeDate, 'cmd'):
            GetCurTradeDate.cmd = GetCurTradeDate()
        return super(GetCurTradeDate, GetCurTradeDate.cmd).send(**kwargs)


class GetTargetIns(DataAPIServer):
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

    uri = r'ATraderGetTargetIns'

    def __init__(self):
        super().__init__(uri=GetTargetIns.uri, mode="post")

    @staticmethod
    def send(Market, Code, BeginDate, EndDate, **kwargs):
        if not hasattr(GetTargetIns, 'cmd'):
            GetTargetIns.cmd = GetTargetIns()
        return super(GetTargetIns, GetTargetIns.cmd).send(Market=Market, Code=Code, BeginDate=BeginDate, EndDate=EndDate, **kwargs)


class GetTargetIns_20190830(DataAPIServer):
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

    uri = r'ATraderGetTargetIns_20190830'

    def __init__(self):
        super().__init__(uri=GetTargetIns_20190830.uri, mode="post")

    @staticmethod
    def send(Market, Code, BeginDate, EndDate, **kwargs):
        if not hasattr(GetTargetIns_20190830, 'cmd'):
            GetTargetIns_20190830.cmd = GetTargetIns_20190830()
        return super(GetTargetIns_20190830, GetTargetIns_20190830.cmd).send(Market=Market, Code=Code, BeginDate=BeginDate, EndDate=EndDate, **kwargs)


class GetTradingTime(DataAPIServer):
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

    uri = r'ATraderGetTradingTime'

    def __init__(self):
        super().__init__(uri=GetTradingTime.uri, mode="post", pack=GetTradingTime.pack)

    @staticmethod
    def send(targetList, kFreq, beginDay, endDay, **kwargs):
        if not hasattr(GetTradingTime, 'cmd'):
            GetTradingTime.cmd = GetTradingTime()
        return super(GetTradingTime, GetTradingTime.cmd).send(targetList=targetList, kFreq=kFreq, beginDay=beginDay, endDay=endDay, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetTradingTime_send(todotdict({'freq': kFreq,'beginD': beginDay,'endD': endDay}), targets_dot)

        targets_dot = [todotdict(target) for target in targetList]
        """
        return json.dumps(kwargs)


class GetTradingDays(DataAPIServer):
    """获取交易日期
    :return: list of double
    """

    uri = r'ATraderGetTradingDays'

    def __init__(self):
        super().__init__(uri=GetTradingDays.uri, mode="post", unpack=GetTradingDays.unpack)

    @staticmethod
    def send(**kwargs):
        if not hasattr(GetTradingDays, 'cmd'):
            GetTradingDays.cmd = GetTradingDays()
        return super(GetTradingDays, GetTradingDays.cmd).send(**kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        tradingDays = recv_serial(func_name).result

        Some return
        """
        return json.loads(kwargs)


class GetPreTradeDate(DataAPIServer):
    """ 获取当前日期迁移交易日的日期
    :return: double 前一交易日的日期
    """

    uri = r'ATraderGetPreTradeDate'

    def __init__(self):
        super().__init__(uri=GetPreTradeDate.uri, mode="post")

    @staticmethod
    def send(**kwargs):
        if not hasattr(GetPreTradeDate, 'cmd'):
            GetPreTradeDate.cmd = GetPreTradeDate()
        return super(GetPreTradeDate, GetPreTradeDate.cmd).send(**kwargs)


class GetFundamentalSet(DataAPIServer):
    """  根据标的的资产，表名，字段名，开始结束日期获取数据库中的日期序列数据
    :param targetList: targetList: list[dict]  [{'Market':marketName, 'Code': CodeName },] 标的列表
    :param CatName: str 表名
    :param ItemList: str字段名
    :param BeginDate: int 开始日期
    :param EndDate: int 结束日期
    :return: list(Dotdict) 相关表时间序列信息
    """

    uri = r'ATraderGetFundamentalSet'

    def __init__(self):
        super().__init__(uri=GetFundamentalSet.uri, mode="post", pack=GetFundamentalSet.pack, unpack=GetFundamentalSet.unpack)

    @staticmethod
    def send(targetList, CatName, ItemList, BeginDate, EndDate, **kwargs):
        if not hasattr(GetFundamentalSet, 'cmd'):
            GetFundamentalSet.cmd = GetFundamentalSet()
        return super(GetFundamentalSet, GetFundamentalSet.cmd).send(targetList=targetList, CatName=CatName, ItemList=ItemList, BeginDate=BeginDate, EndDate=EndDate, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetFundamentalSet_send(CatName, targets_dot, ItemList, BeginDate, EndDate)

        targets_dot = []
        for target in targetList:
            targets_dot.append(todotdict(target))
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        mat_data = load_mat(res.wstrFilePath, error='raise')

        Some return
        """
        return json.loads(kwargs)


class GetHistoryInstruments(DataAPIServer):
    """ 获取日频交易信息
    :param targets: [{'Market':'xxx', 'Code': 'XXX'}]
    :param begin_date: int, 类似：20190429
    :param end_date: int, 类似：20190429
    :param fq_type: str, 支持： NA, FWard, BWard
    :return:
    """

    uri = r'ATraderGetHistoryInstruments'

    def __init__(self):
        super().__init__(uri=GetHistoryInstruments.uri, mode="post", pack=GetHistoryInstruments.pack, unpack=GetHistoryInstruments.unpack)

    @staticmethod
    def send(targets, begin_date, end_date, fq_type='NA', **kwargs):
        if not hasattr(GetHistoryInstruments, 'cmd'):
            GetHistoryInstruments.cmd = GetHistoryInstruments()
        return super(GetHistoryInstruments, GetHistoryInstruments.cmd).send(targets=targets, begin_date=begin_date, end_date=end_date, fq_type=fq_type, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetHistoryInstruments_send(targets_dot, begin_date, end_date, fq_type)

        targets_dot = [todotdict(target) for target in targets]
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        data = load_mat(res.wstrFilePath)
        return_keys = set([str.lower('%s_%s_%d' % (target['Market'], target['Code'], idx)) for idx, target in enumerate(targets)])
        result = {str.upper('.'.join(key.split('_')[:2])): data[key] for key in return_keys if key in data}

        Some return
        """
        return json.loads(kwargs)


class GetFactor(DataAPIServer):
    """获取标的的因子信息
    :param FactorName: str 因子名称
    :param targetList: targetList: list[dict]  [{'Market':marketName, 'Code': CodeName },] 标的列表
    :param BeginDate: int 开始日期
    :param EndDate: int 结束日期
    :param NDaysBefore: int
    :return:
    """

    uri = r'ATraderGetFactor'

    def __init__(self):
        super().__init__(uri=GetFactor.uri, mode="post", pack=GetFactor.pack)

    @staticmethod
    def send(FactorName, targetList, BeginDate, EndDate, NDaysBefore, **kwargs):
        if not hasattr(GetFactor, 'cmd'):
            GetFactor.cmd = GetFactor()
        return super(GetFactor, GetFactor.cmd).send(FactorName=FactorName, targetList=targetList, BeginDate=BeginDate, EndDate=EndDate, NDaysBefore=NDaysBefore, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetFactor_send(FactorName, targets_dot, BeginDate, EndDate, NDaysBefore)

        targets_dot = [todotdict(target) for target in targetList]
        """
        return json.dumps(kwargs)


class GetHistorySet(DataAPIServer):
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

    uri = r'ATraderGetHistorySet'

    def __init__(self):
        super().__init__(uri=GetHistorySet.uri, mode="post", pack=GetHistorySet.pack, unpack=GetHistorySet.unpack)

    @staticmethod
    def send(Market, Code, CatName, ItemName, BeginDate, EndDate, **kwargs):
        if not hasattr(GetHistorySet, 'cmd'):
            GetHistorySet.cmd = GetHistorySet()
        return super(GetHistorySet, GetHistorySet.cmd).send(Market=Market, Code=Code, CatName=CatName, ItemName=ItemName, BeginDate=BeginDate, EndDate=EndDate, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetHistorySet_send(CatName, ItemName, market_code, BeginDate, EndDate)

        #  marketCode 是list
        market_code = [todotdict({'Market': Market, 'Code': Code})]
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        mat_data = load_mat(res.wstrFilePath, error='raise')

        Some return
        """
        return json.loads(kwargs)


class GetMarketSet(DataAPIServer):
    """ 根据表名， 字段名，开始日期和结束日期获取数据库中与整体市场有关的日期序列数据
    :param wstrCat: str 表名
    :param listItem: str 字段名
    :param iBeginDate: int 开始时间
    :param iEndDate: int 结束时间
    :return: list(Dotdict) 相关表时间序列信息
    """

    uri = r'ATraderGetMarketSet'

    def __init__(self):
        super().__init__(uri=GetMarketSet.uri, mode="post", unpack=GetMarketSet.unpack)

    @staticmethod
    def send(wstrCat, listItem, iBeginDate, iEndDate, **kwargs):
        if not hasattr(GetMarketSet, 'cmd'):
            GetMarketSet.cmd = GetMarketSet()
        return super(GetMarketSet, GetMarketSet.cmd).send(wstrCat=wstrCat, listItem=listItem, iBeginDate=iBeginDate, iEndDate=iEndDate, **kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        mat_data = load_mat(res.wstrFilePath, error='raise')

        Some return
        """
        return json.loads(kwargs)


class GetTDPData(DataAPIServer):
    uri = r'ATraderGetTDPData'

    def __init__(self):
        super().__init__(uri=GetTDPData.uri, mode="post", pack=GetTDPData.pack, unpack=GetTDPData.unpack)

    @staticmethod
    def send(market, code, date, fqType, no_return, check_permission=True, **kwargs):
        if not hasattr(GetTDPData, 'cmd'):
            GetTDPData.cmd = GetTDPData()
        return super(GetTDPData, GetTDPData.cmd).send(market=market, code=code, date=date, fqType=fqType, no_return=no_return, check_permission=check_permission, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetTDPData_send(todotdict({'Market': market,'Code': code,'Date': date,'FQ': fqType,'NoReturn': no_return,'CheckPermission': check_permission}))
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        mat_path = res.wstrFilePath

        Some return
        """
        return json.loads(kwargs)


class GetTDPDataMulti(DataAPIServer):
    """获取 tick 数据

    :param targetList: list of dict, 标的列表
    :param beginDate: int, 开始日期, 20180709
    :param endDate: int, 结束日期, eg: 20180710
    :param fqType: str, str, 复权类型
    :return: str, 文件路径 或者 错误字符串, 需要检查错误信息
    """

    uri = r'ATraderGetTDPDataMulti'

    def __init__(self):
        super().__init__(uri=GetTDPDataMulti.uri, mode="post", pack=GetTDPDataMulti.pack)

    @staticmethod
    def send(targetList, beginDate, endDate, fqType, **kwargs):
        if not hasattr(GetTDPDataMulti, 'cmd'):
            GetTDPDataMulti.cmd = GetTDPDataMulti()
        return super(GetTDPDataMulti, GetTDPDataMulti.cmd).send(targetList=targetList, beginDate=beginDate, endDate=endDate, fqType=fqType, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetTDPDataMulti_send(targets_dot, beginDate, endDate, fqType)

        targets_dot = [todotdict(target) for target in targetList]
        """
        return json.dumps(kwargs)


class CheckSubscribeNum(DataAPIServer):
    uri = r'ATraderCheckSubscribeNum'

    def __init__(self):
        super().__init__(uri=CheckSubscribeNum.uri, mode="post", unpack=CheckSubscribeNum.unpack)

    @staticmethod
    def send(Frequency, SubscribeNum, **kwargs):
        if not hasattr(CheckSubscribeNum, 'cmd'):
            CheckSubscribeNum.cmd = CheckSubscribeNum()
        return super(CheckSubscribeNum, CheckSubscribeNum.cmd).send(Frequency=Frequency, SubscribeNum=SubscribeNum, **kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        Nothing return
        """
        return json.loads(kwargs)


class TransTradeTimeToTradeDate(DataAPIServer):
    """ 将时间转换为 yyyymmdd 形式的double类型
    :param checkTime: double 时间
    :return: double  yyyymmdd 形式的时间表示
    """

    uri = r'ATraderTransTradeTimeToTradeDate'

    def __init__(self):
        super().__init__(uri=TransTradeTimeToTradeDate.uri, mode="post", pack=TransTradeTimeToTradeDate.pack, unpack=TransTradeTimeToTradeDate.unpack)

    @staticmethod
    def send(checkTime, **kwargs):
        if not hasattr(TransTradeTimeToTradeDate, 'cmd'):
            TransTradeTimeToTradeDate.cmd = TransTradeTimeToTradeDate()
        return super(TransTradeTimeToTradeDate, TransTradeTimeToTradeDate.cmd).send(checkTime=checkTime, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderTransTradeTimeToTradeDate_send(daytime_str)

        daytime_str = mft_to_str_format(checkTime, '%Y%m%dT%H%M%S')
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        trade_date = recv_serial(func_name).result

        Some return
        """
        return json.loads(kwargs)


class GetFutureInfoExculusively(DataAPIServer):
    """ 获取期货相关信息

    :param targets: 标的索引
    :return:
    """

    uri = r'ATraderGetFutureInfoExculusively'

    def __init__(self):
        super().__init__(uri=GetFutureInfoExculusively.uri, mode="post", pack=GetFutureInfoExculusively.pack)

    @staticmethod
    def send(targets, **kwargs):
        if not hasattr(GetFutureInfoExculusively, 'cmd'):
            GetFutureInfoExculusively.cmd = GetFutureInfoExculusively()
        return super(GetFutureInfoExculusively, GetFutureInfoExculusively.cmd).send(targets=targets, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetFutureInfoExculusively_send([todotdict(target) for target in targets])
        """
        return json.dumps(kwargs)


class GetFutureInfoExculusively_20190918(DataAPIServer):
    """ 获取期货相关信息

    :param targets: 标的索引
    :return:
    """

    uri = r'ATraderGetFutureInfoExculusively_20190918'

    def __init__(self):
        super().__init__(uri=GetFutureInfoExculusively_20190918.uri, mode="post", pack=GetFutureInfoExculusively_20190918.pack)

    @staticmethod
    def send(targets, **kwargs):
        if not hasattr(GetFutureInfoExculusively_20190918, 'cmd'):
            GetFutureInfoExculusively_20190918.cmd = GetFutureInfoExculusively_20190918()
        return super(GetFutureInfoExculusively_20190918, GetFutureInfoExculusively_20190918.cmd).send(targets=targets, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetFutureInfoExculusively_20190918_send([todotdict(target) for target in targets])
        """
        return json.dumps(kwargs)


class GetStockInfoExculusively(DataAPIServer):
    """ 获取股票相关的信息

    :param targets:  标的索引
    :return:
    """

    uri = r'ATraderGetStockInfoExculusively'

    def __init__(self):
        super().__init__(uri=GetStockInfoExculusively.uri, mode="post", pack=GetStockInfoExculusively.pack)

    @staticmethod
    def send(targets, **kwargs):
        if not hasattr(GetStockInfoExculusively, 'cmd'):
            GetStockInfoExculusively.cmd = GetStockInfoExculusively()
        return super(GetStockInfoExculusively, GetStockInfoExculusively.cmd).send(targets=targets, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetStockInfoExculusively_send([todotdict(target) for target in targets])
        """
        return json.dumps(kwargs)


class FdmtFieldInfo(DataAPIServer):
    uri = r'ATraderFdmtFieldInfo'

    def __init__(self):
        super().__init__(uri=FdmtFieldInfo.uri, mode="post", pack=FdmtFieldInfo.pack, unpack=FdmtFieldInfo.unpack)

    @staticmethod
    def send(fdmt_fields: 'list', **kwargs):
        if not hasattr(FdmtFieldInfo, 'cmd'):
            FdmtFieldInfo.cmd = FdmtFieldInfo()
        return super(FdmtFieldInfo, FdmtFieldInfo.cmd).send(fdmt_fields=fdmt_fields, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderFdmtFieldInfo_send(fdmt_fields)
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        Nothing return
        """
        return json.loads(kwargs)


class RiskModelFieldInfo(DataAPIServer):
    uri = r'ATraderRiskModelFieldInfo'

    def __init__(self):
        super().__init__(uri=RiskModelFieldInfo.uri, mode="post", pack=RiskModelFieldInfo.pack, unpack=RiskModelFieldInfo.unpack)

    @staticmethod
    def send(fdmt_fields: 'list', **kwargs):
        if not hasattr(RiskModelFieldInfo, 'cmd'):
            RiskModelFieldInfo.cmd = RiskModelFieldInfo()
        return super(RiskModelFieldInfo, RiskModelFieldInfo.cmd).send(fdmt_fields=fdmt_fields, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderRiskModelFieldInfo_send(fdmt_fields)
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        Nothing return
        """
        return json.loads(kwargs)


class GetFutureContracts(DataAPIServer):
    """ 获取期货可交易合约

    :param i64Date: 查询日期
    :param wstrMarket: 目标市场
    :param wstrVarieties: 目标品种
    :return:
    """

    uri = r'ATraderGetFutureContracts'

    def __init__(self):
        super().__init__(uri=GetFutureContracts.uri, mode="post")

    @staticmethod
    def send(i64Date, wstrMarket, wstrVarieties, **kwargs):
        if not hasattr(GetFutureContracts, 'cmd'):
            GetFutureContracts.cmd = GetFutureContracts()
        return super(GetFutureContracts, GetFutureContracts.cmd).send(i64Date=i64Date, wstrMarket=wstrMarket, wstrVarieties=wstrVarieties, **kwargs)


