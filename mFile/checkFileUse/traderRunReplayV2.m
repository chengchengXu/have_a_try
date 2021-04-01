% traderRunReplayV2(StrategyName, TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, RepalyDate, FQ, AlgoTradeFun, varAlgoFunParameter)
% 实现策略的回放
%
% 输入参数
% StrategyName: 策略名称, char 数组
% TradeFun: 策略函数, function_handle 型, 格式: @函数名称
% varFunParameter: 策略函数中用到的参数, cell 数组, 如 {'参数一', '参数二', '参数三'}
% AccountList: 账户名称, cell 数组
% TargetList: 策略标的列表, struct 数组
%  Market: 市场类型, char 数组
%  Code: 品种代码, char 数组, 如 '000002'
% KFrequency: 策略刷新频率类型, char 数组
%  'tick': tick 频
%  'min': 分钟频
%  'day': 日频
% KFreNum: 刷新频率数值, double 型
% BeginDate: 策略开始的日期, double 型, 如 20140608
% RepalyDate: 策略回放的日期, double 型, 如 20140610, 要求 BeginDate <= RepalyDate
% FQ: 复权类型, char 数组
%  'NA': 不复权
%  'FWard': 向前复权
%  'BWard': 向后复权
% AlgoTradeFun: 算法交易函数, function_handle 型, 格式: @算法交易函数
% varAlgoFunParameter: 算法交易函数中用到的参数, cell 数组
%
% 示例
% 对策略 Strategy 回放, 回放日期为 2015 年 5 月 25 日, 策略开始时间为 2015 年 5 月 20 日
% AccountList(1) = {'FutureBackReplay'};
% TargetList(1).Market = 'CFFEX'; TargetList(1).Code = 'IF0000';
% TargetList(2).Market = 'CFFEX'; TargetList(2).Code = 'IH0000';
% traderRunReplayV2('Strategy', @Strategy, {len1, len2, stopTar, profitTar, pct, shareNum}, AccountList, targetList, 'min', 1, 20150520, 20150525, 'FWard');
%
% 对策略 Strategy 回放, 回放日期为 2015 年 5 月 25 日, 策略开始时间为 2015 年 5 月 20 日
% AccountList(1) = {'StockBackReplay'};
% TargetList(1).Market = 'SZSE'; TargetList(1).Code = '000002';
% TargetList(2).Market = 'SZSE'; TargetList(2).Code = '000001';
% traderRunReplayV2('Strategy', @Strategy, {len1, len2, stopTar, profitTar, pct, shareNum}, AccountList, targetList, 'min', 1, 20150520, 20150525, 'FWard');