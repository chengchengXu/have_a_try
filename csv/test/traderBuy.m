% orderID = traderBuy(Handle, Market, Code, Contracts, Price, PriceType, OrderTag)
% 买入开仓下单; 若初始有空头持仓, 则先平仓, 再买入开仓
%
% 输入参数
% Handle: 账户标识, double 值
% Market: 市场类型, char 数组
%  'SZSE': 深圳股票
%  'SSE': 上海股票
%  'SHFE': 上海期货
%  'DCE': 大连商品
%  'CZCE': 郑州商品
%  'CFFEX': 中金所
% Code: 品种代码, char 数组, 如 'IF0000'
% Contracts: 下单数量, double 值
% Price: 下单价格, double 值; 市价单用 0
% PriceType: 下单价格类型, char 数组
%  'market': 市价
%  'limit': 限价
% OrderTag: 订单标记, char 数组
%
% 输出参数
% orderID: 订单号, double 值; 失败返回 0
%
% 功能描述
% 若计划买开 5 手
% 1. 无持仓, 直接买开 5 手多单, 最后持仓 5 手多单
% 2. 原有 3 手空单, 则先平 3 手空单, 再买开 5 手多单, 最后持仓 5 手多单
% 3. 原有 2 手多单, 直接买开 5 手多单, 最后持仓 2 + 5 = 7 手多单
%
% 示例
% HandleList(1) = {'FutureSimAcc'}; HandleList(2) = {'StockSimAcc'};
% handleList = traderGetHandleList();
% Handle = handleList(1);
% 用 FutureSimAcc 账户市价买入 10 手股指期货主力, 并将此买入操作标记为 'buy'
% 若初始有空头持仓, 则会先将空头持仓全部平仓, 再买入 10 手
% orderID = traderBuy(Handle, 'CFFEX', 'IF0000', 10, 0, 'market', 'buy');
