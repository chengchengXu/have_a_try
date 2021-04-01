from atrader.calcfactor import *
import atrader.tframe.sysclsbase as cnt
from random import *
from atrader.api.orders import *

def myuniform_rand(context: ContextFactor):
    target_len = len(context.target_list)
    return np.full([target_len, 1], random(), dtype=np.float32)


def init(context: ContextFactor):
    context.n = 0
    reg_factor(['PE'])
    reg_kdata('day', 3)
    context.counter = 1
    reg_userindi(myuniform_rand)
    reg_userdata(['2017-01-11'], ['6'])


def calc_factor(context: ContextFactor):
    RAND = []

    print('show the count %d' % context.n, context.now)
    context.n = context.n + 1

    print(get_auto_value(5))
    # print(context.now)
    kdata = get_reg_kdata(context.reg_kdata[0], [], 10, True, True)
    # print(kdata)
    bp_fator = get_reg_factor(context.reg_factor[0], [], 1, True)
    # print(bp_fator)
    context.now
    try:
        get_order_info()
    except Exception:
        print("get_order_info test ok")
    else:
        print("get_code_info test failed")
    try:
        get_last_order()
    except Exception:
        print("get_last_order test ok")
    else:
        print("get_last_order test failed")
    try:
        get_daily_orders()
    except Exception:
        print("get_daily_orders test ok")
    else:
        print('get_daily_orders test failed')
    try:
        get_stop_info()
    except Exception:
        print('get_stop_info test ok')
    else:
        print('get_stop_info test failed')
    try:
        get_daily_executions()
    except Exception:
        print('get_daily_execution test ok')
    else:
        print('get_daily-execution test failed')
    try:
        order_value(0, 0, 0, 0, 0, 0, 0)
    except Exception:
        print('order_value test ok')
    else:
        print('order_value test failed')
    try:
        order_volume(0,0,0,0,0,0,0)
    except Exception:
        print('order_volume test ok')
    else:
        print('order_volume test failed')
    try:
        order_close_all()
    except Exception:
        print('order_close_all test ok')
    else:
        print('order_close_all test failed')
    try:
        order_cancel_all()
    except Exception:
        print('order_cancel_all test ok')
    else:
        print('order_ cancel_all test failed')
    try:
        order_percent(0, 0, 0, 0, 0, 0, 0)
    except Exception:
        print('order_percent test ok')
    else:
        print('order_percent test failed')
    try:
        order_cancel([])
    except Exception:
        print('order_cancel test ok')
    else:
        print('order_cancel test failed')
    try:
        order_target_percent(0, 0, 0, 0, 0)
    except Exception:
        print('order_target_percent test ok')
    else:
        print('order_target_percent test failed')
    try:
        order_target_value(0, 0, 0, 0, 0)
    except Exception:
        print('order_target_value test ok')
    else:
        print('order_target_value test failed')
    try:
        order_target_volume(0, 0, 0, 0, 0)
    except Exception:
        print('order_target_volume test ok')
    else:
        print('order_target_volume test failed')
    try:
        get_unfinished_orders()
    except Exception:
        print('get_unfinish_order test ok')
    else:
        print('get_unfinish_order test failed')
    try:
        stop_loss_by_order(0, 0, 0, 0)
    except Exception:
        print('stop_loss_by_order test ok')
    else:
        print('stop_loss_by_order test failed')
    try:
        stop_profit_by_order(0, 0, 0, 0, 0)
    except Exception:
        print('stop_profit_by_order test ok')
    else:
        print('stop_profit_by_order test failed')
    try:
        stop_trailing_by_order(0, 0, 0, 0, 0, 0)
    except Exception:
        print('stop_trailing_by_order test ok')
    else:
        print('stop_trailing_by_order test failed')
    try:
        stop_cancel([])
    except Exception:
        print('stop_cancel test ok')
    else:
        print('stop_cancel test failed')

    for i in range(len(context.target_list)):
        RAND.append(gauss(0, 1))
        # RAND.append(np.nan)
    print(get_reg_userdata(context.reg_userdata[0]))
    print(get_reg_userindi(context.reg_userindi[0]))

    return np.array(RAND).reshape(-1, 1)


if __name__ == '__main__':
    # run_factor(factor_name='RAND', file_path='runfactorTest.py', targets='AllSecA', begin_date='2017-01-01', end_date='2017-03-01', fq=1)
    run_factor(factor_name='RAND', file_path='runfactorTest.py', targets='SZ50', begin_date='2018-01-01', end_date='2018-03-01', fq=1)
    # a = cnt.vr.ATFactorResult
    k = 0
