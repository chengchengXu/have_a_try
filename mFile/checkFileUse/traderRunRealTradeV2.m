% traderRunRealTradeV2(StrategyName, TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, FQ, AlgoTradeFun, varAlgoFunParameter)
% 实现策略的实盘交易
%
% 输入参数
% StrategyName: 策略名称, char 数组
% TradeFun: 策略函数, function_handle 型, 格式: @函数名称
% varFunParameter: 策略函数中用到的参数, cell 数组
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
% FQ: 复权类型, char 数组
%  'NA': 不复权
%  'FWard': 向前复权
%  'BWard': 向后复权
% AlgoTradeFun: 算法交易函数, function_handle 型, 格式: @算法交易函数
% varAlgoFunParameter: 算法交易函数中用到的参数, cell 数组
%
% 示例
% 对策略 Strategy 实时交易, 策略参数为 {len, plus, ShareNum}, 取数据的开始时间为 2015 年 1 月 1 日
% AccountList(1) = 'FutureSimAcc';
% TargetList(1).Market = 'CFFEX'; TargetList(1).Code = 'IF0000';
% TargetList(2).Market = 'CFFEX'; TargetList(2).Code = 'IH0000';
% traderRunRealTradeV2('Strategy', @Strategy, {len, plus, ShareNum}, AccountList, TargetList, 'min', 1, 20150101, 'FQ');