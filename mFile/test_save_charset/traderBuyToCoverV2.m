% ### traderBuyToCoverV2
% 
% 
% - 函数说明:（在策略结构中）空单的平仓下单，即买入平仓下单。
% 
% 
% - 语法:
% 
% 	`traderBuyToCoverV2(HandleIdx,TargetIdx,Contracts,Price,PriceType,OrderTag)`
% 
% 
% - 输入参数:
% 
% |字段名	|类型	|说明
% |:-:|:-:|:-:|
% |HandleIdx	|整数|账户句柄索引序列号
% |TargetIdx	|整数|交易标的索引序列号
% |Contracts	|必须为大于零的整数	|下单数量
% |Price	|double	|价格，市价单价格为0
% |PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
% |OrderTag	|char	|订单标记，用户可以自定义
% 
% 
% - 输出参数:
% 
% |字段名	|类型	|说明
% |:-:|:-:|:-:|
% |orderID	|整数	|委托记录号，跟随策略启动进行编号
% 
% 
% - 功能描述:
% 
% 若计划买平5手，
% 
% 1.无持仓，此次买平无效，最后无持仓 
% 
% 2.原有2手多单,此次买平无效,维持买平前的一切状态,最后持仓是:2手多单
% 
% 3.若有7手空单，计划买平5手后，账号最后持仓为:max(7-5,0)=2，即要么还有7-5=2手空单，要么无持仓
% 
% 
% ----------
% 
% - 例子:
% 
% 主策略函数
% 
%     function matlab_example_test(bInit,bDayBegin,cellPar)%
% 	    global idexD;
% 	    % 三个参数的形式固定  
% 	    if bInit % 判定是否策略开启启动  
% 		    % 行情注册，15分钟的K线和5分钟的K线  
% 		    idexD=traderRegKData('min',15);
%         else
%             % 获得第一个账户，索引号为1的标的资产的持仓
%             [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
%             % 若没有持仓
%             if Position==0
%                 % 用'FutureBackReplay'账户，以市价卖出1手rb主连合约，并把这个订单标记为‘sell’
%                 orderID = traderShortSellV2(1, 1, 1, 0, 'market', 'sell');
%             else
%                 % 用'FutureBackReplay'账户，以市价买入平仓1手rb主连合约，并把这个订单标记为‘buy’
%                 SellOrderID=traderBuyToCoverV2(1, 1, 1, 0, 'market', 'buy');
%             end        
% 	    end
%     end
% 
% 执行脚本：
% 
%     clear all;
%     clc;
%     % 设定回测账户
%     AccountList(1) = {'FutureBackReplay'};
%     % 设定
%     TargetList(1).Market = 'SHFE';
%     TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
%     % 设定初始资金和费率，滑点等  
%     traderSetBacktest(1000000, 0.000026,0.02,0);
%     % 按照15分钟的频率运行回测  
%     traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
% 
% - 注意：
% 
% 1.PriceType指定为‘market’的话，price使用0
% 2.OrderID用于止盈止损的订单跟踪，从0开始编号，每次策略重启后会重新编号
% 
% 
% block    char 板块或指数的名称，其中'index'——返回所有指数；'plate_industry'——返回全部行业