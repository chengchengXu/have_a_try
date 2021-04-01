
import pandas as pd
from atrader.tframe.comm.atcmd import *

# get account handle
test_name = 'SimAcc'
h = atSendCmdGetTradeAccountHandle(test_name)

# get account position
a_p = atSendCmdGetAccountTargetGrossPosition([h], '')
t = pd.DataFrame(a_p)
print(t)

a_p_c = atSendCmdGetAccountPositionAndCash([h], '')
t = pd.DataFrame(a_p_c[-1])
print(t)
