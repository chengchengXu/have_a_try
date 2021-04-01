# coding: utf-8

import json
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


class TradeAPIServer(HttpBaseCmd):
    _endpoint = "TradeAPIServer"

    def __init(self, uri, **kwargs):
        super().__init__(url=f"http://{TradeAPIServer._endpoint}{uri}", **kwargs)


class GetStopOrderInfo(TradeAPIServer):
    """ 获取止损止盈单的信息
    """

    uri = r'ATraderGetStopOrderInfo'

    def __init__(self):
        super().__init__(uri=GetStopOrderInfo.uri, mode="post")

    @staticmethod
    def send(account_handle, stop_order_id_s, **kwargs):
        if not hasattr(GetStopOrderInfo, 'cmd'):
            GetStopOrderInfo.cmd = GetStopOrderInfo()
        return super(GetStopOrderInfo, GetStopOrderInfo.cmd).send(account_handle=account_handle, stop_order_id_s=stop_order_id_s, **kwargs)


class STTradeStopOrder(TradeAPIServer):
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

    uri = r'ATraderSTTradeStopOrder'

    def __init__(self):
        super().__init__(uri=STTradeStopOrder.uri, mode="post", pack=STTradeStopOrder.pack)

    @staticmethod
    def send(params, **kwargs):
        if not hasattr(STTradeStopOrder, 'cmd'):
            STTradeStopOrder.cmd = STTradeStopOrder()
        return super(STTradeStopOrder, STTradeStopOrder.cmd).send(params=params, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderSTTradeStopOrder_send(todotdict(params))
        """
        return json.dumps(kwargs)


class STTradeOperation(TradeAPIServer):
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

    uri = r'ATraderSTTradeOperation'

    def __init__(self):
        super().__init__(uri=STTradeOperation.uri, mode="post", pack=STTradeOperation.pack)

    @staticmethod
    def send(params, **kwargs):
        if not hasattr(STTradeOperation, 'cmd'):
            STTradeOperation.cmd = STTradeOperation()
        return super(STTradeOperation, STTradeOperation.cmd).send(params=params, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderSTTradeOperation_send(todotdict(params))
        """
        return json.dumps(kwargs)


class IsAccountValid(TradeAPIServer):
    """ 判断账户是否有效

    :param handle: double　账户类型
    :return:
    """

    uri = r'ATraderIsAccountValid'

    def __init__(self):
        super().__init__(uri=IsAccountValid.uri, mode="post")

    @staticmethod
    def send(handle, **kwargs):
        if not hasattr(IsAccountValid, 'cmd'):
            IsAccountValid.cmd = IsAccountValid()
        return super(IsAccountValid, IsAccountValid.cmd).send(handle=handle, **kwargs)


class STGetAccountPosition(TradeAPIServer):
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

    uri = r'ATraderSTGetAccountPosition'

    def __init__(self):
        super().__init__(uri=STGetAccountPosition.uri, mode="post", pack=STGetAccountPosition.pack, unpack=STGetAccountPosition.unpack)

    @staticmethod
    def send(Handle, Market, Code, LongShort=None, **kwargs):
        if not hasattr(STGetAccountPosition, 'cmd'):
            STGetAccountPosition.cmd = STGetAccountPosition()
        return super(STGetAccountPosition, STGetAccountPosition.cmd).send(Handle=Handle, Market=Market, Code=Code, LongShort=LongShort, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderSTGetAccountPosition_send(todotdict({'Handle': Handle,'Market': Market,'Code': Code,'LongShort': LongShort}))

        LongShort = '' if LongShort is None else LongShort
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        info = recv_serial(func_name).sPositionData

        Some return
        """
        return json.loads(kwargs)


class STTradeGetAccountList(TradeAPIServer):
    """ 获取策略测试的账户列表信息
    :return: list of todotdict, eg: [todotdict{'Name':'', 'Handle':xxx, 'Status':'online'}]
    """

    uri = r'ATraderSTTradeGetAccountList'

    def __init__(self):
        super().__init__(uri=STTradeGetAccountList.uri, mode="post")

    @staticmethod
    def send(**kwargs):
        if not hasattr(STTradeGetAccountList, 'cmd'):
            STTradeGetAccountList.cmd = STTradeGetAccountList()
        return super(STTradeGetAccountList, STTradeGetAccountList.cmd).send(**kwargs)


class CloseOperation(TradeAPIServer):
    """
    :param strategy_name: str 策略名称
    :param i64Handle: int64  账户句柄
    :return:
    """

    uri = r'ATraderCloseOperation'

    def __init__(self):
        super().__init__(uri=CloseOperation.uri, mode="post", pack=CloseOperation.pack, unpack=CloseOperation.unpack)

    @staticmethod
    def send(strategy_name, i64Handle, **kwargs):
        if not hasattr(CloseOperation, 'cmd'):
            CloseOperation.cmd = CloseOperation()
        return super(CloseOperation, CloseOperation.cmd).send(strategy_name=strategy_name, i64Handle=i64Handle, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderCloseOperation_send(strategy_name, np.int64(i64Handle))
        """
        return json.dumps(kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        Nothing return
        """
        return json.loads(kwargs)


class CancelFrozen(TradeAPIServer):
    """
    :param Handle: int 账户句柄
    :return:
    """

    uri = r'ATraderCancelFrozen'

    def __init__(self):
        super().__init__(uri=CancelFrozen.uri, mode="post", unpack=CancelFrozen.unpack)

    @staticmethod
    def send(Handle, **kwargs):
        if not hasattr(CancelFrozen, 'cmd'):
            CancelFrozen.cmd = CancelFrozen()
        return super(CancelFrozen, CancelFrozen.cmd).send(Handle=Handle, **kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        Nothing return
        """
        return json.loads(kwargs)


class CancelOrder(TradeAPIServer):
    """ 发送停止订单的请求
    :param strategyName: str 策略名称
    :param handle:  int 账户句柄
    :param orderID: int 订单号
    :return:
    """

    uri = r'ATraderCancelOrder'

    def __init__(self):
        super().__init__(uri=CancelOrder.uri, mode="post", unpack=CancelOrder.unpack)

    @staticmethod
    def send(strategyName, handle, orderID, **kwargs):
        if not hasattr(CancelOrder, 'cmd'):
            CancelOrder.cmd = CancelOrder()
        return super(CancelOrder, CancelOrder.cmd).send(strategyName=strategyName, handle=handle, orderID=orderID, **kwargs)

    @staticmethod
    def unpack(kwargs):
        """
        Nothing return
        """
        return json.loads(kwargs)


class CancelStopOrder(TradeAPIServer):
    """ 发送停止止损单的请求
    :param strategyName: str 策略名称
    :param handle: int 账户句柄
    :param orderID: int 订单号
    :return: bool,
    """

    uri = r'ATraderCancelStopOrder'

    def __init__(self):
        super().__init__(uri=CancelStopOrder.uri, mode="post")

    @staticmethod
    def send(strategyName, handle, orderID, **kwargs):
        if not hasattr(CancelStopOrder, 'cmd'):
            CancelStopOrder.cmd = CancelStopOrder()
        return super(CancelStopOrder, CancelStopOrder.cmd).send(strategyName=strategyName, handle=handle, orderID=orderID, **kwargs)


class GetAccountTargetGrossPosition(TradeAPIServer):
    """ 获取仓位相关信息

    :param handles: 账户handle
    :param targets: [{'Market': xx, 'Code': xx}]
    :return:
    """

    uri = r'ATraderGetAccountTargetGrossPosition'

    def __init__(self):
        super().__init__(uri=GetAccountTargetGrossPosition.uri, mode="post", pack=GetAccountTargetGrossPosition.pack)

    @staticmethod
    def send(handles, targets, **kwargs):
        if not hasattr(GetAccountTargetGrossPosition, 'cmd'):
            GetAccountTargetGrossPosition.cmd = GetAccountTargetGrossPosition()
        return super(GetAccountTargetGrossPosition, GetAccountTargetGrossPosition.cmd).send(handles=handles, targets=targets, **kwargs)

    @staticmethod
    def pack(kwargs):
        """
        atserial.ATraderGetAccountTargetGrossPosition_send(handles, [todotdict(target) for target in targets])
        """
        return json.dumps(kwargs)


class GetAccountCash(TradeAPIServer):
    uri = r'ATraderGetAccountCash'

    def __init__(self):
        super().__init__(uri=GetAccountCash.uri, mode="post")

    @staticmethod
    def send(handles, **kwargs):
        if not hasattr(GetAccountCash, 'cmd'):
            GetAccountCash.cmd = GetAccountCash()
        return super(GetAccountCash, GetAccountCash.cmd).send(handles=handles, **kwargs)


