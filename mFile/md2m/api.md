### traderGetCodeList

- 函数说明:获得指数（包含权重和成分股）、行业板块（没有权重，只有成分股），包括成分股及权重等信息

- 语法:

	`traderGetCodeList(block,varargin)`

- 输入参数:

|字段名	|类型	|说明|
|:-:|:-:|:-:|
|block	|char	|板块或指数的名称，其中'index'——返回所有指数；'plate_industry'——返回全部行业;'SecA'——全A;'sse_a'——上海A股;'szse_a'——深圳A股		
|varargin	|整形	|输入的时间日期，缺失时为当前时间点


- 输出参数:

IDPWeightArray	struct结构体，包含以下字段

|字段	|类型	|说明|
|:-:|:-:|:-:|
|Market|char|指数所属交易所代码，行业为空
|Code|char|指数的代码or行业首字母简称
|Name|char|行业或指数的详细名称
|BlockName|double|行业或指数简称
|Weight|double|权重


- 示例:

1.获取所有指数的情况
2.获取所有行业的情况

    a=traderGetCodeList('index');
	b=traderGetCodeList('plate_industry');


返回：

    a = 
    
      1×722 struct array with fields:
    Market
    Code
    Name
    BlockName
    Weight
    
    b = 
    
      1×503 struct array with fields:
    Market
    Code
    Name
    BlockName
    Weight



### traderGetCurrentBarV2



- 函数说明:（在策略结构中）根据策略刷新获得当前bar的信息


- 语法

    `traderGetCurrentBarV2()  `
    

- 输入参数:

	无

- 输出参数:

	返回两个变量，每个变量的含义如下

|变量名	|类型|	说明|
| :-: | :-: |:-:|
|barNumber|整数|当前Bar的序列号，若刷新频率为日频，则返回的顺序是当前时间到开始日期的交易日序列；若非日频，则返回当天开盘至今的序列号|
|barTime|double|Bar时间点，以Datenums形式存储|


- 例子:

策略主函数

	function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得当前刷新时间点Bar的位置和Bar的时间
            [barNumber, barTime]= traderGetCurrentBarV2()    
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');


返回:

    barNumber =
     1
    barTime =   
       7.3706e+05
      
    barNumber =  
     2
    barTime =
       7.3706e+05
    

### traderGetCurrentTickV2


- 函数说明：（在策略结构中）根据标的资产查询当前刷新时刻的Tick数据


- 语法:

    `traderGetCurrentTickV2(TargetIdx)`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|TargetIdx| 整数|标的资产索引


- 输出结构：

多变量，其中每个变量的意义如下：

|变量名|类型|说明|
| - | :-: | :-: |
|TickNumber|N*1 double型数组|当前tick在当天的序数|
|Time|N*1 double型数组|时间列表以Matlab datanum形式存储|
|Price|N*1 double型数组	|当前tick的成交价|
|volume|N*1 double型数组	|当天至当前tick的累计成交量（忽略集合竞价部分）|
|volumetick|	N*1 double型数组 |	当前tick成交量|
|openinterest|	N*1 double型数组|当前tick的持仓量|
|bidprice	|N*5 double型数组|当前tick的前五档委托买价（买一到买五）|
|bidvolume|	N*5 double型数组	|当前tick的前五档委托买量（买一到买五）|
|askprice|	N*5 double型数组	|当前tick的前五档委托卖价（卖一到卖五）|
|askvolume|	N*5 double型数组	|当前tick的委托卖量（卖一到卖五）|

- 例子：

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
        % 三个参数的形式固定 
	    global idexD;
	    if bInit % 判定是否策略开启启动
		    % 行情注册，1分钟的频率  
		    idexD=traderRegKData('tick',1);   
        else
            % 获得当前刷新时间点的tick数据情况
            [TickNumber, Time, Price, Volume, VolumeTick, OpenInterest, BidPrice, BidVolume, AskPrice, AskVolume] = traderGetCurrentTickV2(1)
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'sse';
    TargetList(1).Code = '600000'; % 浦发银行
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用FutureBackReplay这个回测账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照1day的频率运行回测，1day会刷新一次策略
    % 回测时间从20180101开始到20180401结束
    % 价格使用前复权价格
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'tick',1,20180102,20180103,'FWard'); 

返回：

    TickNumber =    
        1   
    Time =    
       7.3706e+05
    Price =   
       12.6200
    Volume =    
    	3046
    VolumeTick =    
    	2147
    OpenInterest =   
     	0  
    BidPrice = 
       12.6100
       12.6000
       12.5900
       12.5800
       12.5700 
    BidVolume =
       54283
     	100
       40200
       41100
       20700 
    AskPrice =   
       12.6200
       12.6300
       12.6400
       12.6500
       12.6600
    AskVolume =
       17800
       47868
       11400
       89000
       25700
	  


### traderGetFactor



- 函数说明:根据标的资产，因子名称，返回因子的数值矩阵



- 语法:

    `traderGetFactor(FactorName, TargetList, BeginDate, EndDate)`; 


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|FactorName|char|BP因子名称，只支持单个因子名
|TargetList|结构体|包含两个字段，Market，Code
|BeginDate|整型|开始日期|
|EndDate|整型|结束日期|




- 输出结构：

返回3个变量，每个变量的意义如下：


|字段名	|类型|	说明|
| - | :-: |:-:|
| Date| cell|交易日历序列
|TargetList| 结构体|标的资产列表
|Data| float|因子矩阵，行为日期，列为对应的标的




- 例子：

使用两个标的，获取其PE这个因子的数值

	TargetList(1).Market = 'sse';
    TargetList(1).Code = '600000'; % 浦发银行
    TargetList(2).Market = 'sse';
    TargetList(2).Code = '601699'; % 潞安环能
    [Date, targetList, Data] = traderGetFactor('PE', TargetList, 20170101,20170201)


返回：

    Date =
      736698
      736699
      736700
      736701
      736704
      736705
      736706
      736707
      736708
      736711
      736712
      736713
      736714
      736715
      736718
      736719
      736720
      736721

    targetList = 
      1×2 struct array with fields:
    Market
    Code


    Data =
       1.0e+05 *
  
    7.36700 00010 0111
    7.36700 00010 0113
    7.36700 00010 0116
    7.36700 00010 0115
    7.36700 00010 0115
    7.36700 00010 0118
    7.36710 00010 0120
    7.36710 00010 0117
    7.36710 00010 0116
    7.36710 00010 0119
    7.36710 00010 0118
    7.36710 00010 0121
    7.36710 00010 0121
    7.36710 00010 0121
    7.36720 00010 0123
    7.36720 00010 0126
    7.36720 00010 0125
    7.36720 00010 0129
    
### traderGetFundamentalSet



- 函数说明:根据标的资产，表名，字段名，开始日期和结束日期来获取数据库中的日期序列数据



- 语法:

    `traderGetFundamentalSet(TargetList,CatName,ItemName,BeginDate,EndDate)`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|TargetList|结构体|包含Market和Code字段
|CatName| char|表名，具体情况数据介绍
|ItemName|char|字段名，请看数据介绍
|BeginDate|  整型, 如 20140608 |开始日期
|EndDate|整型, 如 20140609, 为 0 时取到当天|结束日期


- 输出结构：

struct结构体，每个字段数据的长度与数据库中日期有关，其中每个字段的意义如下：

|字段名|类型|说明|
| - | :-: | :-: |
|Market| char 数组|市场类型
|Code| char 数组|品种代码
|Date|double|时间以Matlab datenum日期数字形式存储|
|对应查询的字段名|any|根据数据库的内容返回



- 例子：

获取潞安环能（601699）和东阿阿胶（000423）从20160101到20180101日，在表FS_DER中的{'WorkCapital','NWorkCapital','IC','TRe'}字段，分别对应为{营运资本，净营运资本，投入资本，留存收益}

    targetlist(1).Market='sse';
	targetlist(2).Market='szse';
	targetlist(1).Code='601699';% 潞安环能
	targetlist(2).Code='000423';% 东阿阿胶

	% 营运资本，净营运资本，投入资本，留存收益
	result=traderGetFundamentalSet(targetlist,'FS_DER',{'WorkCapital','NWorkCapital','IC','TRe'},20160101,20180101)



返回：



	result = 

  	16×1 struct array with fields:

    Market
    Code
    EndDate
    WorkCapital
    NWorkCapital
    IC
    TRe



注意：

1.行业可以作为标的进行查询，具体的行业代码见traderGetCodeList('plate_industry')
2.支持一次查询多个标的


### traderGetHistorySet



- 函数说明:根据标的资产，表名，字段名，开始日期和结束日期来获取数据库中的日期序列数据



- 语法:

  `traderGetHistorySet(Market,Code,CatName,ItemName,BeginDate,EndDate)`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|Market| char 数组|市场类型
|Code| char 数组|品种代码,
|CatName| char|表名，具体情况数据介绍
|ItemName|char|字段名，请看数据介绍
|BeginDate|  整型, 如 20140608 |开始日期
|EndDate|整型, 如 20140609, 为 0 时取到当天|结束日期


- 输出结构：

struct结构体，每个字段的长度与数据库中日期有关，其中每个字段的意义如下：

|字段名|类型|说明|
| - | :-: | :-: |
|Date|double|时间以Matlab日期数字形式存储|
|对应查询的字段名|any|根据数据库的内容返回



- 例子：

获取601699从20180401到20180501日，在表MKT_EQU_FLOW_ORDER中的{'InflowS','InflowM','InflowL','InflowXL'}字段，分别对应为{资金流入(小单)，资金流入(中单)，资金流入(大单)，资金流入(超大单)}

    data=traderGetHistorySet('sse','601699','MKT_EQU_FLOW_ORDER',{'InflowS','InflowM','InflowL','InflowXL'},20180401,20180501)



返回：



    data = 

  18×1 struct array with fields:

    TradeDate
    InflowS
    InflowM
    InflowL
    InflowXL
	


注意：

1.行业可以作为标的进行查询，具体的行业代码见traderGetCodeList('plate_industry')
2.不支持一次查询多个标的


### traderGetKData



- 函数说明:根据标的资产，频率，开始日期和结束日期获取bar行情信息



- 语法:

    `traderGetKData(Market, Code, KFrequency, KFreNum, BeginDate, EndDate, Filledup, FQ);`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|Market| char 数组|市场类型
|Code| char 数组|品种代码,
|KFrequency| char数组|K 线的时间级别, 如 'day', 'min'
|KFreNum|整数|K 线的频率
|BeginDate|  整型, 如 20140608 |开始日期
|EndDate|整型, 如 20140609, 为 0 时取到当天|结束日期,
|FilledUp| logical|补齐类型, True补齐，False不补齐
|FQ| char 数组|复权类型,    'NA': 不复权；'FWard': 向前复权；'BWard': 向后复权



- 输出结构：

多变量，其中每个变量的意义如下：

|变量名|类型|说明|
| - | :-: | :-: |
|Time|N*1 double型数组|bar的时间以Matlab日期数字形式存储|
|Open|N*1 double型数组	|bar的开盘价|
|High|N*1 double型数组	|bar的最高价|
|Low|	N*1 double型数组 |bar的最低价|
|Close|	N*1 double型数组|bar的收盘价|
|volume|	N*1 double型数组|bar的成交量|
|turnover	|N*1 double型数组|bar的成交金额|
|openinterest|	N*1 double型数组	|bar的持仓量|



- 例子：

获取000004从20170101到20170331日线Bar数据，用8个不同的变量返回其结果


    [Time, Open, High, Low, Close, Volume, TurnOver, OpenInterest] = traderGetKData('SZSE', '000004', 'day', 1, 20170101, 20170331, false, 'FWard');





### traderGetLatestQuotationV2



- 函数说明：（在策略结构中）获取多组标的资产的最新报价情况（只适用于tick刷新）



- 语法:

  ` traderGetLatestQuotationV2(TargetListIdx);`



- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|TargetListIdx|列表或者cell，整数|标的资产索引号|






- 输出结构：


|字段名	|类型|	说明|
| - | :-: |:-:|
|Market|char|标的资产所属交易所代码
|Code|char|标的资产的证券代码
|Time|double|最新报价的时间戳，datenums形式
|CurrentPrice|double|当前价
|CurrentVolume|double|当前成交量

- 例子：

主策略函数

        function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    global BuyOrderID
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获取第一个和第三个标的的最新的报价情况
            LatestQuotation = traderGetLatestQuotationV2([1,3]);
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    TargetList(2).Market = 'SHFE'; 
    TargetList(2).Code = 'AG0000'; % 白银主力
    TargetList(3).Market = 'SHFE'; 
    TargetList(3).Code = 'AL0000'; % 铝主力
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180101,20180102,'FWard');



### traderGetMainContract


- 函数说明：根据交易日历返回主力合约的物理合约


- 语法:

    `traderGetMainContract(Market, Code, BeginDate, EndDate);`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|Market| char 数组|市场类型
|Code| char 数组|品种代码,
|BeginDate| 整形|开始日期
|EndDate| 整形|结束日期

- 输出结构：

N*2 cell：

|字段名|类型|说明|
| - | :-: | :-: |
|Code|N*1 char数组|物理主力合约代码|
|Date|N*1 double数组	|具体交易日历|


- 例子：

获取沪深300主连合约在20180101至20180201的物理主力合约

    data = traderGetMainContract('cffex', 'if0000', 20180101, 20180201);

返回：

    data =
    
      23×2 cell array

    'IF1801'    [20180102]
    'IF1801'    [20180103]
    'IF1801'    [20180104]
    'IF1801'    [20180105]
    'IF1801'    [20180108]
    'IF1801'    [20180109]
    'IF1801'    [20180110]
    'IF1801'    [20180111]
    'IF1801'    [20180112]
    'IF1801'    [20180115]
    'IF1801'    [20180116]
    'IF1801'    [20180117]
    'IF1803'    [20180118]
    'IF1803'    [20180119]
    'IF1803'    [20180122]
    'IF1803'    [20180123]
    'IF1803'    [20180124]
    'IF1803'    [20180125]
    'IF1803'    [20180126]
    'IF1803'    [20180129]
    'IF1803'    [20180130]
    'IF1803'    [20180131]
    'IF1803'    [20180201]
	
### traderGetMarketSet



- 函数说明:根据表名，字段名，开始日期和结束日期，获取数据库中与整体市场有关的日期序列数据



- 语法:

   `traderGetMarketSet(CatName,ItemName,BeginDate,EndDate)`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|CatName| char|表名，具体情况数据介绍
|ItemName|char|字段名，请看数据介绍
|BeginDate|  整型, 如 20140608 |开始日期
|EndDate|整型, 如 20140609, 为 0 时取到当天|结束日期


- 输出结构：

struct结构体，每个cell的长度与数据库中日期有关，其中每个字段的意义如下：

|字段名|类型|说明|
| - | :-: | :-: |
|Date|cell|时间以Matlab日期数字形式存储|
|对应查询的字段名|cell|根据数据库的内容返回



- 例子：

获取从20180401到20180501日，在表MKT_EQUD_STATS中的{'StatsTypeClass','MarketValue','NegMarketValue','TurnoverVol','TurnoverValue'}字段，分别对应为{统计角度，市值,流通市值,成交量,成交金额}，代表整个市场的状况

        data=traderGetMarketSet('MKT_EQUD_STATS',{'StatsTypeClass','MarketValue','NegMarketValue','TurnoverVol','TurnoverValue'},20180401,20180501)



返回：

	data = 

  	90×1 struct array with fields:

    TradeDate
    StatsTypeClass
    MarketValue
    NegMarketValue
    TurnoverVol
    TurnoverValue
	 

### traderGetRegFactor



- 函数说明:（在策略结构中）根据已注册的BP因子获取BP因子数据（数据滑窗）



- 语法:

    `traderGetRegFactor(Idx, length); `


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|idx| float矩阵|注册BP因子返回的矩阵变量
|length| 数值类型|例120, 表示返回从当前开始往前的120个数据序列




- 输出结构：

（M*N+1）*length的矩阵，最新的数据在最后一列，其中每行的含义如下：
M为标的数量
N为因子数量

|字段名	|类型|	说明|
| - | :-: |:-:|
|time|float|当前策略时刻，datenum形式
|第一个标的第一个因子| float|返回的因子数值
|第一个标的第二个因子| float|返回的因子数值
|第二个标的第一个因子| float|返回的因子数值
|第二个标的第二个因子| float|返回的因子数值




- 例子：

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
        % 三个参数的形式固定 
	    global idexD;
        global factor1;
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('day',1);
            % BP因子注册，使用PE和MA10两个因子
            factor1=traderRegFactor('PE','MA10');
        else
            % 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
            factordata=traderGetRegFactor(factor1, 2)
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'sse';
    TargetList(1).Code = '600000'; % 浦发银行
    TargetList(2).Market = 'sse';
    TargetList(2).Code = '601699'; % 潞安环能
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用FutureBackReplay这个回测账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照1day的频率运行回测，1day会刷新一次策略
    % 回测时间从20180101开始到20180401结束
    % 价格使用前复权价格
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'day',1,20180101,20180401,'FWard'); 



### traderGetRegKData



- 函数说明:（在策略结构中）根据已注册的数据序列获取K线数据（数据滑窗）



- 语法:

    `traderGetRegKData(KIdx, length, fillup); `

- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|Kidx| double矩阵|注册数据返回的矩阵变量，记录注册频率信息
|length| 数值类型|例120, 表示返回从当前开始往前的120个数据序列
|fillup| boolen|true：补齐；false：不补齐

- 输出结构：

（8 x N）x length的矩阵，N为标的数，当存在多标的时，每个标的展示以行的方式扩展矩阵，最新的数据在最后一列，其中每行的含义如下：

|字段|类型|说明|
| - | :-: | :-: |
|Time|1*length double型数组|bar的时间以Matlab datenum日期数字形式存储|
|Open|1*length doublet型数组	|bar的开盘价|
|High|1*length double型数组	|bar的最高价|
|Low|	1*length double型数组 |bar的最低价|
|Close|	1*length double型数组|bar的收盘价|
|volume|	1*length double型数组|bar的成交量|
|turnover	|1*length double型数组|bar的成交金额|
|openinterest|	1*length double型数组	|bar的持仓量（股票为0）|

- 例子：

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    global factor1;  
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，1day级别的K线  
		    idexD=traderRegKData('day',1);
	    else
			% 构建数据滑窗，获取当前时刻过去5天不补齐的数据情况
	    	data=traderGetRegKData(idexD,5,false)
	    end
    end

执行脚本

    % 设定回测账户，
    AccountList(1) = {'StockBackReplay'};
    % 设定标的资产,以万科A作为标的资产
    TargetList.Market='szse';
    TargetList.Code='000002';  
    % 按照1day的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'day',1,20170301,20170625,'FWard');


其中data在策略回测中返回的情况是：
最右的一列为当前时刻的bar信息


    data =
    
       1.0e+08 *

       NaN       NaN       NaN       NaN    0.0074
       NaN       NaN       NaN       NaN    0.0000
       NaN       NaN       NaN       NaN    0.0000
       NaN       NaN       NaN       NaN    0.0000
       NaN       NaN       NaN       NaN    0.0000
       NaN       NaN       NaN       NaN    0.0025
       NaN       NaN       NaN       NaN    5.1417
       NaN       NaN       NaN       NaN         0


### traderGetRegTimeLine

- 函数说明：（在策略结构中）获取策略运行的时间节点（刷新的时间轴）

- 语法:

`    traderGetRegTimeLine();`

- 输入参数：

	无

- 输出结构：

|字段名	|类型|	说明|
| - | :-: |:-:|
|TL|double|整个策略刷新时间的时间轴，datenums格式

- 例子：

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 注册之后，可以获取整个策略刷新的时间轴
            TL=traderGetRegTimeLine()           
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

返回：

    TL =
    
       1.0e+05 *
    
      Columns 1 through 19
    
    7.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.3706
    
      Columns 20 through 38
    
    7.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.3706
    
      Columns 39 through 52
    
    7.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.37067.3706
	


### traderGetTargetInfo



- 函数说明:查询标的基本信息。


- 语法:

	`traderGetTargetInfo(Market, Code)`


- 输入参数:

|字段名	|类型	|说明|
|:-:|:-:|:-:|
|Market	|char	|市场代码|
|Code	|char	|交易品种代码|


- 输出参数:

struct结构体，其中每个字段的意义如下：

|Keys	|类型|说明|
|:-:|:-:|:-:|
|Market	|char	|市场|
|Code	|char	|标的代码|
|Name	|char	|标的名称|
|Type	|double	|标的类型 1 股票, 2 期货, 3 期权
|Multiple	|double|	合约乘数|
|MinMove	|double|	最小变动单位|
|TradingFeeOpen	|double	|开仓手续费率|
|TradingFeeClose|	double|	平仓手续费率|
|TradingFeeCloseToday	|double	|当日平仓手续费|
|LongMargin	|double	|多方保证金率|
|ShortMargin	|double	|空方保证金率|
|LastTradingDate	|double	|最后交易日|
|以下为期权专用|
|TargetMarket	|char|	对标标的市场|
|TargetCode	|char	|对标标的代码|
|OptionType	|char	|期权类型(暂未提供)|
|CallOrPut	|double	|认购认沽|
|ListDate	|double	|首个交易日|
|EndDate	|double	|最后交易日|
|ExerciseDate	|double|	期权行权日|
|DeliveryDate	|double	|行权交割日|
|CMUnit	|double	|合约单位|
|ExercisePrice	|double	|期权行权价|
|MarginUnit	|double	|单位保证金|

示例:

获取橡胶主力连续合约的信息
	
	Data=traderGetTargetInfo('SHFE', 'ru0000')

返回

	Data = 
    
      struct with fields:
    
    Market: 'shfe'
    Code: 'ru0000'
    Name: '天胶1809'
    Type: 2
    Multiple: 10
    MinMove: 5
    TradingFeeOpen: 5.4050e-05
    TradingFeeClose: 5.4050e-05
    TradingFeeCloseToday: 5.4050e-05
    LongMargin: 0.1900
    ShortMargin: 0.1900
    TargetMarket: ''
    TargetCode: ''
    OptionType: ''
    CallOrPut: ''
    ListDate: 20170918
    LastTradingDate: 20180917
    EndDate: 4.3432e-311
    ExerciseDate: 4.3437e-311
    DeliveryDate: 1.5915e-314
    CMUnit: 2.9644e-323
    ExercisePrice: 0
    MarginUnit: 1.5535e-315
	
### traderGetTargetInfoV2



- 函数说明:（在策略结构中）获取标的基本信息。


- 语法:

	`traderGetTargetInfoV2(TargetIdxA)`


- 输入参数:

|字段名	|类型	|说明|
|:-:|:-:|:-:|
|TargetIdxA	|列表，cell或者整数	|标的索引号序列|


- 输出参数:

struct结构体，每个字段的意义如下：

|Keys	|类型	|说明|
|:-:|:-:|:-:|
|Market	|char	|市场|
|Code	|char	|合约代码|
|Name	|char	|标的名称|
|Type	|double	|标的类型 1 股票, 2 期货, 3 期权
|Multiple	|double|	合约乘数|
|MinMove	|double|	最小变动单位|
|TradingFeeOpen	|double	|开仓手续费率|
|TradingFeeClose|	double|	平仓手续费率|
|TradingFeeCloseToday	|double	|当日平仓手续费|
|LongMargin	|double	|多方保证金率|
|ShortMargin	|double	|空方保证金率|
|LastTradingDate	|double	|最后交易日|
|以下为期权专用|
|TargetMarket	|char|	对标标的市场|
|TargetCode	|char	|对标标的代码|
|OptionType	|char	|期权类型(暂未提供)|
|CallOrPut	|double	|认购认沽|
|ListDate	|double	|首个交易日|
|EndDate	|double	|最后交易日|
|ExerciseDate	|double|	期权行权日|
|DeliveryDate	|double	|行权交割日|
|CMUnit	|double	|合约单位|
|ExercisePrice	|double	|期权行权价|
|MarginUnit	|double	|单位保证金|

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得索引号为1的标的资产的基本信息
            Data=traderGetTargetInfoV2(1)
	    end
    end 

执行脚本：

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

返回：

    Data = 
    
      struct with fields:
    
                  Market: 'shfe'
                    Code: 'rb0000'
                    Name: '螺钢1810'
                    Type: 2
                Multiple: 10
                 MinMove: 1
          TradingFeeOpen: 2.6000e-05
         TradingFeeClose: 2.6000e-05
    TradingFeeCloseToday: 2.6000e-05
              LongMargin: 0.1600
             ShortMargin: 0.1600
            TargetMarket: ''
              TargetCode: ''
              OptionType: ''
               CallOrPut: ''
                ListDate: 20171017
         LastTradingDate: 20181015
                 EndDate: 2.3693e-308
            ExerciseDate: 1.4182e-317
            DeliveryDate: 9.8813e-324
                  CMUnit: 2.9644e-323
           ExercisePrice: 6.3660e-314
              MarginUnit: 1.5535e-315
			  


### traderGetTargetList
- 函数说明:（策略结构中）获取标的资产列表。

- 语法:

	`traderGetTargetList()`
	
- 输出参数:
struct结构体，每个字段的意义如下：

|字段|类型	|说明|
|:-:|:-:|:-:|
|Market	|char	|市场|
|Code	|char	|标的代码|

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得索引号为1的标的资产的基本信息
            Data=traderGetTargetList()
	    end
    end

执行脚本:

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

返回：
    
    Data = 
    
      struct with fields:

    	Market: 'SHFE'
      	Code: 'RB0000'
		


### traderGetTickData


- 函数说明：根据标的资产，日期查询当天的所有Tick数据（可以查询当天tick数据）


- 语法:

    `traderGetTickData(Market, Code, Date, FQ);`


- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|Market| char 数组|市场类型
|Code| char 数组|品种代码,
|Date| 整形|查询日期
|FQ| char 数组|复权类型,    'NA': 不复权；'FWard': 向前复权；'BWard': 向后复权

- 输出结构：

多变量，其中每个变量的意义如下：

|字段名|类型|说明|
| - | :-: | :-: |
|Time|N*1 double型数组|时间列表以Matlab datanum形式存储|
|Price|N*1 double型数组	|tick的成交价|
|volume|N*1 double型数组	|当天的累计成交量|
|volumetick|	N*1 double型数组 |	tick成交量|
|turnover|	N*1 double型数组| 	tick的成交金额,|
|openinterest|	N*1 double型数组|tick的持仓量|
|bidprice	|N*5 double型数组|tick的前五档委托买价（买一到买五）|
|bidvolume|	N*5 double型数组	|tick的前五档委托买量（买一到买五）|
|askprice|	N*5 double型数组	|tick的前五档委托卖价（卖一到卖五）|
|askvolume|	N*5 double型数组	|tick的委托卖量（卖一到卖五）|

- 例子：

获取沪深300主连合约在20150601当天整天的Tick数据情况，以10个变量返回其结果

    [Time, Price, Volume, VolumeTick, TurnOver, OpenInterest, BidPrice, BidVolume, AskPrice, AskVolume] = traderGetTickData('CFFEX', 'IF0000', 20150601, 'NA');





### traderGetTradingDays

- 函数说明:获取指定日期内，所有的交易日，如果endday为0，则返回从开始时间一直到最近一个交易日中间所有的交易日期。

- 语法:

	`traderGetTradingDays(BeginDay, EndDay)`


- 输入参数:

|字段名	|类型	|说明|
|:-:|:-:|:-:|
|BeginDay	|整形	|开始交易日期|
|EndDay	|整形	|结束交易日期|



- 输出参数:


||类型|说明|
|:-:|:-:|:-:|
|Days	|一维矩阵|交易日期序列|


- 例子:

获取20180101至20180201的交易日历

    traderGetTradingDays(20180101,20180201)


返回:

    ans =
    
      Columns 1 through 16

    20180102    20180103    20180104    20180105    20180108    20180109    20180110    20180111    20180112    20180115    20180116    20180117    20180118    20180119    20180122    20180123

      Columns 17 through 23

    20180124    20180125    20180126    20180129    20180130    20180131    20180201
	

### traderGetTradingTime

- 函数说明:根据具体标的的频率周期获取的交易时间。

- 语法:

	`traderGetTradingTime(TargetList,freq,BeginDay,EndDay)`

- 输入参数:

|字段名	|类型|	说明|
|:-:|:-:|:-:|
|TargetList|结构体|标的资产，包含Market和Code两个字段|
|freq|char|返回的时间精细级别'tick','sec','min','day'|
|BeginDay|整型|开始日期|
|EndDay	|整型|	结束日期|


- 输出参数:

|字段名	|类型	|说明|
|:-:|:-:|:-:|
|Time	|一维矩阵	|交易时间，datenum格式，有多个标的时，会取各自时间的并集|
|DayPos	|一维矩阵	|该时间在所属日期bar序列数，有多个标的时，会取各自的并集再排序|


- 例子:

获取3个期货品种在20180507至20180508，以1分钟划分的交易时间点

    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    TargetList(2).Market = 'SHFE'; 
    TargetList(2).Code = 'AG0000'; % 白银主力
    TargetList(3).Market = 'SHFE'; 
    TargetList(3).Code = 'AL0000'; % 铝主力
	[Time, DayPos] = traderGetTradingTime (TargetList, 'min', 20180507, 20180508);

返回
    
	Time =

       1.0e+05 *
    
        7.3718
	    7.3718
	    7.3718
	    7.3718
		  .
		  .

    DayPos =
    
	     1
	     2
	     3
	     4
      	 .
    	 .



### traderRunBacktestV2


- 函数说明:（回测函数入口）实现策略的回测。


- 语法:

    `traderRunBacktestV2(StrategyName,@TradeFun,varFunParameter,AccountList,TargetList,KFrequency,KFreNum,BeginDate,EndDate,FQ)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|StrategyName	|char	|自定义回测策略的名称
|TradeFun	|函数对象	|主策略函数名
|varFunParameter	|cell	|策略函数中用到的参数
|AccountList	|cell	|账户名称，回测模式只允许单账号
|TargetList	|结构体	|策略标的列表 Market : 市场类型，char；Code: 交易品种代码，char
|KFreNum	|整数|频率数值
|KFrequency	|char	|频率周期
|BeginDate	|整型	|开始日期
|EndDate	|整型	|结束日期
|FQ	|char	|复权类型， 'NA'为不复权， 'FWard'向前复权， 'BWard' 向后复权


- 输出：

	无


- 例子:

执行脚本

    clear all;
    clc;
    % 设定需要传进策略的参数
    stoploss =0.9; % 设定止损比例
    m=5; % 设定双均线中的第一根均线周期
    n=10; % 设定双均线中的第二个均线周期
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用FutureBackReplay这个回测账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照15分钟的频率运行回测，每15分钟会刷新一次策略
    % 回测时间从20180102开始到20180103结束
    % 价格使用前复权价格
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {stoploss,m,n},AccountList,TargetList,'min',15,20180102,20180103,'FWard'); 



- 注意：

1.回测的账户只能使用FutureBackReplay或者StockBackReplay，均可以交易所有标的
2.回测不允许使用多账户交易
3.参数不一定都需要在执行脚本中定义，在主策略函数里定义也是可以的



### traderRunRealTradeV2

- 函数说明: 实现策略的实盘交易和模拟交易，只支持单一策略。

- 语法:

	`traderRunRealTradeV2(StrategyName, @TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, FQ)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|StrategyName	|char	|自定义回测策略的名称
|TradeFun	|函数对象	|主策略函数名
|varFunParameter	|cell	|策略函数中用到的参数
|AccountList	|cell	|账户名称，回测模式只允许单账号
|TargetList	|结构体	|策略标的列表 Market : 市场类型，char； Code: 交易品种代码，char
|KFreNum	|整数|频率数值
|KFrequency	|char	|频率周期
|EndDate	|整型	|结束日期
|FQ	|char	|复权类型， 'NA'为不复权， 'FWard'向前复权， 'BWard' 向后复权


- 输出：

	无


- 例子:

执行脚本


    clear all;
    clc;
    % 设定需要传进策略的参数
    stoploss =0.9; % 设定止损比例
    m=5; % 设定双均线中的第一根均线周期
    n=10; % 设定双均线中的第二个均线周期
    % 设定实时交易的账户
    AccountList(1) = {'SimAcc'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用SimAcc这个账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照15分钟的频率运行实时交易
    % 数据会从20180502开始准备
    % 价格使用前复权价格
    traderRunRealTradeV2('matlab_example_test',@matlab_example_test, {stoploss,m,n},AccountList,TargetList,'min',15,20180502,'FWard');
    

- 注意：

1.实盘交易和模拟交易都是使用traderRunRealTradeV2，通过账户名来区分，配置账户在AT客户端上设置
2.BeginDate的作用于设定数据开始位置，构建的数据滑窗时间轴不能早于BeginDate，否则将返回NaN或者“”
3.实时模式下的手续费以及滑点等不能设置，实盘根据经纪商设定，模拟交易根据系统默认设置


### traderDailyCloseTime




- 函数说明: 日内停止刷新时间设置，执行函数后，日内策略不会再被刷新执行


- 语法:

	`traderDailyCloseTime(time)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|time|整型	|平仓时间, 整型, 如: 112500代表11:25:00


- 输出：

	无


- 例子

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
            % 设置在14：55:00时对所有仓位平仓
            traderDailyCloseTime(145500);
        else
            % 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
	    end
    end
	


### traderRegFactor

- 函数说明:（在策略结构中）注册策略要使用的BP因子（目前仅限于股票）


- 语法:

    `traderRegFactor(FactorName1，FactorName2，……)`

- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|FactorName	|char	|因子名称，具体见数据介绍

- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|Idx	|double矩阵	|每一行代表一个标的，列为系统用于构建数据滑窗的数据

- 例子:

主策略函数

	    function matlab_example_test(bInit,bDayBegin,cellPar)%
        % 三个参数的形式固定 
	    global idexD;
        global factor1;

	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('day',1);
            % BP因子注册，使用PE和MA10两个因子
            factor1=traderRegFactor('PE','MA10');
        else
            % 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
            factordata=traderGetRegFactor(factor1, 1)
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'sse';
    TargetList(1).Code = '600000'; % 浦发银行
    TargetList(2).Market = 'sse';
    TargetList(2).Code = '601699'; % 潞安环能
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用FutureBackReplay这个回测账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照1day的频率运行回测，1day会刷新一次策略
    % 回测时间从20180101开始到20180401结束
    % 价格使用前复权价格
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'day',1,20180101,20180401,'FWard'); 

- 注意：

1.一般`traderRegFactor`返回的变量都需要使用在主策略函数里定义为全局变量，不然没办法在后续的函数运行中被调用
2.支持同时注册多个因子
3.因子的数值是数据库里是日数值,默认交易日结束才更新，所以时间在交易时间，只能拿到前一天的因子数值


### traderRegKData

- 函数说明:（在策略结构中）注册策略要使用的行情数据频率

- 语法:

	`traderRegKData(KFrequency, KFreNum)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|KFrequency	|char	|频率周期，支持‘tick’，‘min’，‘day'
|KFreNum	|整数	|频率数值

- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|Idx	|double矩阵	|每一行代表一个标的，列为系统用于构建数据滑窗的数据

- 例子:

主策略函数

	function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
			% 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定需要传进策略的参数
    stoploss =0.9; % 设定止损比例
    m=5; % 设定双均线中的第一根均线周期
    n=10; % 设定双均线中的第二个均线周期
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用FutureBackReplay这个回测账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照15分钟的频率运行回测，每15分钟会刷新一次策略
    % 回测时间从20180102开始到20180103结束
    % 价格使用前复权价格
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {stoploss,m,n},AccountList,TargetList,'min',15,20180102,20180103,'FWard'); 

返回：

    idexD =

     2     1     0

注意：

1.一般`traderRegKData`返回的变量都需要使用在主策略函数里定义为全局变量，不然没办法在后续的函数运行中被调用
2.当存在多个标的，然后`traderGetRegKData`只想拿某个标的时，通过筛选行就可以实现，例如`traderGetRegKData(idexD(1,:), 5, false)`就只拿到第一个标的的数据


### traderSetBacktest

- 函数说明:（回测入口前）设置回测初始信息。

- 语法:

	`traderSetBacktest(InitialCash,Costfee,Rate,SlidePrice,PriceLoc,DealType,LimitType)`

- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|InitialCash	|double	|初始资本
|Costfee	|double	|手续费率（所有品种统一设置）
|Rate	|double	|无风险利率
|SlidePrice	|double	|滑点倍数
|PriceLoc	|char	|市价单成交位置 :0-当前bar收盘价； 1-下一个bar开盘价； 2-下一个bar第二个tick; n-下一个bar第n个tick;  默认为1
|DealType	|char	|市价单成交类型: 0-成交价； 1-对方最优价； 2-己方最优价 默认为0
|LimitType	|char	|限价单成交方式: 0-直接成交； 1-下一个bar内没有该价格时，撤单处理； 默认为0

- 输出：

	无

- 例子
在回测时设置初始资本1000000元、手续费率0.0025、无风险利率0.02、滑价0、默认1下一个bar的开盘价、默认0成交价、默认0直接成交

		traderSetBacktest(1000000,0.0025,0.02,0,1,0,0)
	

### traderSetMarketOrderHoldingType

- 函数说明: （在回测结构中）设置市价单保持状态，只适用于回测


- 语法:

	`traderSetMarketOrderHoldingType(MarketOrderHolding)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|MarketOrderHolding	|logical	|当一下根bar成交量为0时，true,则在成交量等于0时撤单，false则为保持状态


- 输出：

	无


- 例子

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
            % 设置市价单的保持状态(只适用于回测)
            traderSetMarketOrderHoldingType(true);
        else
            % 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
	    end
    end


### traderGetAccountInfoV2

- 函数说明: (策略结构中)通过账户句柄索引序列号获得账户当前资金情况

- 语法:

	`traderGetAccountInfoV2(HandleIdx)`

- 输入参数

|字段名|类型|说明|
|:-:|:-:|:-:|
|HandleIdx|列表，cell或者整数|账户句柄索引序列号|

- 输出参数:

返回多个变量，每个变量的意义如下：

|字段|类型	|说明
|:-:|:-:|:-:|
|ValidCash	|double	|账户当前可用资金
|HandListCap	|double	|账户当前总动态权益
|OrderFrozen	|double	|下单冻结资金总额
|MarginFrozen	|double	|保证金冻结资金总额
|PositionProfit	|double	|持仓盈亏

- 示例:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得索引号为1的标的资产的基本信息
             [ValidCash, HandListCap,OrderFrozen, MarginFrozen,PositionProfit] = traderGetAccountInfoV2(1)
	    end
    end


执行脚本：

	clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

返回：


    ValidCash =
    
     1000000
    
    HandListCap =
    
     1000000
    
    OrderFrozen =
    
     0
    
    MarginFrozen =
    
     0
    
    PositionProfit =
    
     0
	 

### traderGetAccountPositionDirV2

- 函数说明:（策略结构中）获得指定账户，指定标的资产的当前多头或者空头的仓位信息。


- 语法:

	`traderGetAccountPositionDirV2(HandleIdx,TargetIdx,LongShort)`

- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|列表，cell或者整数	|账户句柄索引序列号
|TargetIdx	|列表，cell或者整数	|交易标的索引序列号
|LongShort	|char	|'Long'表示多头 'Short'表示空头


- 输出参数:

返回3个变量，每个变量的意义如下：

|字段|类型	|说明
|:-:|:-:|:-:|
|Position	|double	|当前多头或者空头持仓
|Frozen	|double	|当前多头或者空头冻结持仓
|AvgPrice	|double	|当前多头或者空头平均价格


- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的多头持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionDirV2(1, 1, 'Long')
			% 若多头持仓为0
            if Position==0
                % 下单以市价单买入1手
                orderID = traderBuyV2(1, 1, 1, 0, 'market', 'buy');
            end        
	    end
    end

执行脚本：

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

返回：

    Position =
    
     0
    
    
    Frozen =
    
     0
    
    
    AvgPrice =

     0
	 

### traderGetAccountPositionV2

- 函数说明:(策略结构中)获得标的资产在指定账户里仓位信息。


- 语法:

	`traderGetAccountPositionV2(HandleIdx,TargetIdx)`

- 输入参数

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|列表，cell或者整数	|账户句柄索引序列号
|TargetIdx	|列表，cell或者整数	|交易标的索引序列号


- 输出参数:

3个变量，每个变量的代表意义如下：

|字段|类型	|说明
|:-:|:-:|:-:|
|Position	|double|当前多头或者空头持仓
|Frozen	|double|当前多头或者空头冻结持仓
|AvgPrice	|double	|当前多头或者空头平均价格


- 例子： 

主策略函数

	function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1)
            % 若没有持仓
            if Position==0
                % 下单以市价单买入1手
                orderID = traderBuyV2(1, 1, 1, 0, 'market', 'buy');
            end        
	    end
    end

执行脚本：

	clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

返回：

    Position =
    
     0
    
    Frozen =
    
     0
    
    AvgPrice =
    
     0



### traderBuyToCoverV2


- 函数说明:（在策略结构中）空单的平仓下单，即买入平仓下单。


- 语法:

	`traderBuyToCoverV2(HandleIdx,TargetIdx,Contracts,Price,PriceType,OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Contracts	|必须为大于零的整数	|下单数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义


- 输出参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|orderID	|整数	|委托记录号，跟随策略启动进行编号


- 功能描述:

若计划买平5手，

1.无持仓，此次买平无效，最后无持仓 

2.原有2手多单,此次买平无效,维持买平前的一切状态,最后持仓是:2手多单

3.若有7手空单，计划买平5手后，账号最后持仓为:max(7-5,0)=2，即要么还有7-5=2手空单，要么无持仓


----------

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
            % 若没有持仓
            if Position==0
                % 用'FutureBackReplay'账户，以市价卖出1手rb主连合约，并把这个订单标记为‘sell’
                orderID = traderShortSellV2(1, 1, 1, 0, 'market', 'sell');
            else
                % 用'FutureBackReplay'账户，以市价买入平仓1手rb主连合约，并把这个订单标记为‘buy’
                SellOrderID=traderBuyToCoverV2(1, 1, 1, 0, 'market', 'buy');
            end        
	    end
    end

执行脚本：

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

- 注意：

1.PriceType指定为‘market’的话，price使用0
2.OrderID用于止盈止损的订单跟踪，从0开始编号，每次策略重启后会重新编号


### traderBuyV2


- 函数说明:（在策略结构中）买入开仓下单，若初始有空头持仓，则先平仓，再买入。


- 语法:

	`traderBuyV2(HandleIdx,TargetIdx,Contracts,Price,PriceType,OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Contracts	|必须为大于零的整数	|下单数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|orderID	|整数	|委托记录号，跟随策略启动进行编号


- 功能描述:

若计划买开5手，

1.无持仓，直接买开5手多单，最后持仓是:5手多单
2.原有3手空单，则市价平3手空单，再买开5手多单，最后持仓是:5手多单
3.原有2手多单，再买开5手多单，最后持仓是:2+5=7手多单

----------

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1)
            % 若没有持仓
            if Position==0
                % 用'FutureBackReplay'账户，以市价买入1手rb主连合约，并把这个订单标记为‘buy’
                orderID = traderBuyV2(1, 1, 1, 0, 'market', 'buy');
            end        
	    end
    end

执行脚本：

	clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

- 注意：

1.PriceType指定为‘market’的话，price必须使用0
2.OrderID用于止盈止损的订单跟踪，从1开始编号，每次策略重启后会重新编号
3.委托订单成交的位置会在下一根K线（回测中根据设置），回报会在下一次策略刷新时获取


### traderCancelOrderV2

- 函数说明：（在策略结构中）撤销未成交的限价单



- 语法:

    `traderCancelOrderV2(HandleIdx, OrderID);`

- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|HandleIdx| 整数|账户索引，顺序根据策略入口时指定的AccountList
|OrderID| 整数|委托订单系统生成的OrderID


- 输出结构：

	无

- 例子：

主策略函数

        function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    global BuyOrderID
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获取账户的当前持仓信息
            [Position,Frozen,AveragePrice]=traderGetAccountPositionV2(1,1);
            
            % 若没有持仓则下单
            if Position==0
                % 下单，使用第一个账户，第一个标的资产，下单数量1手，价格为0，市价单，标记这个单为'buy1'  
                BuyOrderID=traderBuyV2(1,1,1,40000,'limit','buy1');
                % 增加止损单
                % 第一个账户，针对BuyOrderID这个订单，止损价差为3个指数点，以市价平仓，并标记这个止损单为‘stop1’
                OrderID=traderStopLossByOrderV2(1,BuyOrderID,3,'point','market','stop1');
            end
            % 判断BuyOrderID这个限价单是否已经成交
            Price=traderOrderFilledPriceV2(1,BuyOrderID);
            if Price==0 % Price==0表示该订单未成交
                % 撤销BuyOrderID这个限价单
                traderCancelOrderV2(1,BuyOrderID);
            end
       
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定标的资产
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180101,20180102,'FWard');
	
### traderCloseAllV2

- 函数说明: （在策略结构中）全平指定账户所有持仓(不包含冻结部分)。


- 语法:

	`traderCloseAllV2(HandleIdx)`

- 输入参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号

- 输入参数:

	无

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
            % 将第一个账户全部平仓
            traderCloseAllV2(1)      
	    end
    end

执行脚本

	clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
	
### traderDirectBuyV2

- 函数说明:（在策略结构中）买入下单，初始持仓无影响。

- 语法:

	`traderDirectBuyV2(HandleIdx, TargetIdx, Contracts, Price, PriceType,OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Contracts	|必须为大于零的整数	|下单数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义

- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|orderID	|整数	|委托记录号，跟随策略启动进行编号


- 功能描述:

若计划买开5手:

1.无持仓，直接买开5手，最后持仓为:5手多单

若账号已有空单:

2.如果空单数量大，例如空单7手，则最后仓位为:7-5=2手空单

3.如果买开数量大，例如空单3手，则最后仓位为:5-3=2手多单

4.已有3手买开，再买开5手，最后持仓是3+5=8手多单

----------

- 例子:

主策略函数：

     function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1)
            % 若没有持仓
            if Position==0
                % 用'FutureBackReplay'账户，以市价买入1手rb主连合约，并把这个订单标记为‘buy’
                orderID = traderDirectBuyV2(1, 1, 1, 0, 'market', 'buy');
            end        
	    end
    end
  
执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
	

### traderDirectSellV2

- 函数说明:（在策略结构中）卖出下单，初始持仓无影响。

- 语法:

	`traderDirectSellV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Contracts	|必须为大于零的整数	|下单数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|orderID	|int	|委托记录号，跟随策略启动进行编号

功能描述:

若计划卖开5手，

1.账号无持仓，直接卖开5手空单
若账号已有多单,
2.如果卖开数量大,例如多单3手，则先平3手多单,再卖开5-3=2手空单.最后持仓是:2手空单
3.如果多单数量大,例如多单8手，则最后仓位为:8-5=3手多单[即多单被平了5手
4.若账号已有2手空单,再卖开5手,最后持仓的数量是:2+5=7手空单

----------

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1)
            % 若没有持仓
            if Position==0
                % 用'FutureBackReplay'账户，以市价买卖出1手rb主连合约，并把这个订单标记为‘sell’
                orderID = traderDirectSellV2(1, 1, 1, 0, 'market', 'sell');
            end        
	    end
    end  

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
	
### traderOrderFilledPriceV2

- 函数说明：（在策略结构中）判断限价单是否已经成交



- 语法:

    `traderOrderFilledPriceV2(HandleIdx, OrderID);`

- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|HandleIdx| 整数|账户索引，顺序根据策略入口时指定的AccountList
|OrderID| 整数|委托订单系统生成的OrderID

- 输出结构：

|字段名	|类型|	说明|
| - | :-: |:-:|
|Price|double|限价单是否成交，若0，则未成交；若成交，则返回值为成交价，部分成交则返回部分成交的均价

- 例子：

主策略函数

        function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    global BuyOrderID
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获取账户的当前持仓信息
            [Position,Frozen,AveragePrice]=traderGetAccountPositionV2(1,1);
            
            % 若没有持仓则下单
            if Position==0
                % 下单，使用第一个账户，第一个标的资产，下单数量1手，价格为0，市价单，标记这个单为'buy1'  
                BuyOrderID=traderBuyV2(1,1,1,40000,'limit','buy1');
                % 增加止损单
                % 第一个账户，针对BuyOrderID这个订单，止损价差为3个指数点，以市价平仓，并标记这个止损单为‘stop1’
                OrderID=traderStopLossByOrderV2(1,BuyOrderID,3,'point','market','stop1');
            end
            % 判断BuyOrderID这个限价单是否已经成交
            Price=traderOrderFilledPriceV2(1,BuyOrderID);
            if Price==0 % Price==0表示该订单未成交
                % 撤销BuyOrderID这个限价单
                traderCancelOrderV2(1,BuyOrderID);
            end
       
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180101,20180102,'FWard');
	

### traderPositionToV2

- 函数说明:指定账户，指定标的资产调仓到指定仓位


- 语法:

	`traderPositionToV2(HandleIdx,TargetIdx,Position,Price,PriceType,OrderTag)`


- 输入参数：

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Position	|double	|目标仓位数量，正负代表多空, 数值代表仓位数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|orderID	|整数	|委托记录号，跟随策略启动进行编号

功能描述:

1.计划调整为指定仓位:5，（多单或者空单）
账号无持仓:则相应开多或者开空5手

2.初始持仓为3手多单:
计划调整为5手空单,平3手多单,开5手空单,最后持仓:5手空单
计划调整为5手多单,最后持仓:5手多单

3.初始持仓为2手空单:
计划调整为5手多单,则平2手空单,再开5手多单,最后持仓:5手多单
计划调整为5手空单,最后持仓:5手空单

----------

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
            % 用'FutureBackReplay'账户，以市价将rb主连合约的仓位调到5手，并把这个订单标记为‘target’
            orderID = traderPositionToV2(1, 1, 5, 0, 'market', 'target');       
	    end
    end

执行脚本：

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
	

### traderSellShortV2

- 函数说明:（在策略结构中）卖出开仓下单，若初始有多头持仓，则先平仓，再卖出。


- 语法:

	`traderSellShortV2(HandleIdx,TargetIdx,Contracts,Price,PriceType,OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Contracts	|必须为大于零的整数	|下单数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|orderID	|整数	|委托记录号，跟随策略启动进行编号

功能描述:

若计划卖开5手，

1.账号无持仓，直接卖开5手空单，最后持仓:5手空单

2.有3手多单,先市价平3手多单,在卖开5手空单,最后持仓:5手空单

3.有2手空单,再卖开5手空单,最后持仓:2+5=7手空单


----------

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
            % 若没有持仓
            if Position==0
                % 用'FutureBackReplay'账户，以市价卖出1手rb主连合约，并把这个订单标记为‘sell’
                orderID = traderSellShortV2(1, 1, 1, 0, 'market', 'sell');
            end        
	    end
    end

执行脚本：

	clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
	
### traderSellV2

- 函数说明:（在策略结构中）多单的平仓下单，即卖出平仓下单。


- 语法:

	`traderSellV2(HandleIdx,TargetIdx,Contracts,Price,PriceType,OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数|账户句柄索引序列号
|TargetIdx	|整数|交易标的索引序列号
|Contracts	|必须为大于零的整数	|下单数量
|Price	|double	|价格，市价单价格为0
|PriceType	|char	|下单价格类型 'market': 市价 'limit': 限价
|OrderTag	|char	|订单标记，用户可以自定义


- 输出参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|orderID	|整数	|委托记录号，跟随策略启动进行编号


- 功能描述:

若计划卖平5手，

1.无持仓，此次卖平无效，最后无持仓 

2.原有2手空单,此次卖平无效,维持卖平前的一切状态,最后持仓是:2手空单

3.若有7手多单，计划卖平5手后，账号最后持仓为:max(7-5,0)=2，即要么还有7-5=2手多单，要么无持仓

----------

- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获得第一个账户，索引号为1的标的资产的持仓
            [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
            % 若没有持仓
            if Position==0
                % 用'FutureBackReplay'账户，以市价卖出1手rb主连合约，并把这个订单标记为‘buy’
                orderID = traderBuyV2(1, 1, 1, 0, 'market', 'buy');
            else
                % 用'FutureBackReplay'账户，以市价卖出平仓1手rb主连合约，并把这个订单标记为‘sell’
                SellOrderID=traderSellV2(1, 1, 1, 0, 'market', 'sell');
            end        
	    end
    end

执行脚本：

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

- 注意：

1.PriceType指定为‘market’的话，price使用0
2.OrderID用于止盈止损的订单跟踪，从0开始编号，每次策略重启后会重新编号


### traderCancelStopOrderV2

- 函数说明：（在策略结构中）根据止盈止损单生成的OrderID撤销未触发的止盈止损单

- 语法:

   ` traderCancelStopOrderV2(HandleIdx, OrderID);`

- 输入参数：

|字段名	|类型|	说明|
| - | :-: |:-:|
|HandleIdx| 整数|账户索引，顺序根据策略入口时指定的AccountList
|OrderID| 整数|需撤销的止盈止损单的订单号

- 输出结构：

无

- 例子：

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    global OrderID; 
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 获取账户的当前持仓信息
            [Position,Frozen,AveragePrice]=traderGetAccountPositionV2(1,1);
            % 若没有持仓则下单
            if Position==0
                % 下单，使用第一个账户，第一个标的资产，下单数量1手，价格为0，市价单，标记这个单为'buy1'  
                BuyOrderID=traderBuyV2(1,1,1,0,'market','buy1');
                % 增加止损单
                % 第一个账户，针对BuyOrderID这个订单，止损价差为3个指数点，以市价平仓，并标记这个止损单为‘stop1’
                OrderID=traderStopLossByOrderV2(1,BuyOrderID,3,'point','market','stop1');
            % 若有持仓则撤销现有的止损单
            else
				% 撤销OrderID这个订单编号的止损单                
                traderCancelStopOrderV2(1,OrderID);
            end  
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180101,20180102,'FWard');
	

### traderStopLossByOrderV2




- 函数说明: （在策略结构中）针对指定订单以固定的点位或者比例止损（以tick数据进行匹配，仅在匹配成功时成交）


- 语法:

	`traderStopLossByOrderV2(HandleIdx, TargetOrderID, StopGap, StopType, OrderCtg, OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数	|账户句柄索引
|TargetOrderID	|整数	|止损指令针对的订单（委托时生成的OrderID）
|StopGap	|double	|止损阈值， 当stopType为'Point'时，其数值代表价格变动的点数， 当stopType为'Percent'时，其数值代表价格变动百分比，如3表示3%
|StopType	|char	|止损类型 'Point'：  按价格点数止损，在订单成交价格的基础上变动指定点数则触发止损条件 'Percent'：按照价格变化的百分比率止损，在订单成交价格的基础上变动指定百分比则触发止损条件
|OrderCtg	|char	|下单价格类型: 'market': 市价成交
|OrderTag	|char	|订单标记


- 输出参数:

|字段名|类型	|说明
|:-:|:-:|:-:|
|StopOrderID	|整数	|订单号


- 例子:

主策略函数


 	function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 买入下单
            orderID=traderBuyV2(1,1,1,0,'market','buy');
            % 根据买入的订单设置止损单
            % 以点数作为止损标准，亏损6个指数点将以市价止损
            StopOrderID=traderStopLossByOrderV2(1, orderID, 6, 'point', 'market', 'stop1');     
	    end
    end  

执行脚本：

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');


- 注意:

1.使用止盈止损时设置的Point或者Percent，计算触发价格会根据该品种的最小变动单位四舍五入取整

2.Point指的是价格点数，并非最小变动单位


### traderStopProfitByOrderV2


- 函数说明: （在策略结构中）针对指定订单以固定的点位或者比例止盈（以tick数据进行匹配，仅在匹配成功时成交）

- 语法:

	`traderStopProfitByOrderV2(HandleIdx,TargetOrderID,StopGap,StopType,OrderCtg,OrderTag)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数	|账户句柄索引
|TargetOrderID	|整数	|止损指令针对的订单（委托时生成的OrderID）
|StopGap	|double	|止盈阈值， 当stopType为'Point'时，其数值代表价格变动的点数， 当stopType为'Percent'时，其数值代表价格变动百分比，如3表示3%
|StopType	|char	|止盈类型 'Point'：  按价格点数止损，在订单成交价格的基础上变动指定点数则触发止盈条件 'Percent'：按照价格变化的百分比率止盈，在订单成交价格的基础上变动指定百分比则触发止盈条件
|OrderCtg	|char	|下单价格类型: 'market': 市价成交
|OrderTag	|char	|订单标记


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|StopOrderID	|整数	|订单号


- 例子:

主策略函数

    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 买入下单
            orderID=traderBuyV2(1,1,1,0,'market','buy');
            % 根据买入的订单设置止损单
            % 以点数作为止盈标准，获利6个指数点将以市价止盈
            StopOrderID=traderStopProfitByOrderV2(1, orderID, 6, 'point', 'market', 'stop1');     
	    end
    end

执行脚本 

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');

- 注意：

1.使用止盈止损时设置的Point或者Percent，计算触发价格会根据该品种的最小变动单位四舍五入取整

2.Point指的是价格点数，并非最小变动单位


### traderStopTrailingByOrderV2


- 函数说明: （在策略结构中）针对指定订单跟踪止盈（以tick数据进行匹配，仅在匹配成功时成交）

- 语法:

	`traderStopTrailingByOrderV2(HandleIdx, TargetOrderID, StopGap, StopType, TrailingGap, TrailingType, OrderCtg, OrderTag)`

- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|HandleIdx	|整数	|账户句柄索引
|TargetOrderID	|整数	|止损指令针对的订单（委托时生成的OrderID）
|StopGap	|double	|止盈阈值， 当stopType为'Point'时，其数值代表价格变动的点数， 当stopType为'Percent'时，其数值代表价格变动百分比，如3表示3%
|StopType	|char	|止盈类型 'Point'：  按价格点数止损，在订单成交价格的基础上变动指定点数则触发止盈条件 'Percent'：按照价格变化的百分比率止盈，在订单成交价格的基础上变动指定百分比则触发止盈条件
|TrailingGap	|double	|跟踪止盈触发的回撤条件 当TrailingType为'Point'时，其数值代表价格变动的点数， 当TrailingType为'Percent'时，其数值代表价格变动百分比，如3表示3%。若价格先触及stopGap,又触及此条件，则进行对应的止盈下单
|TrailingType	|char	|跟踪止盈类型 Point'：  按价格点数止盈，从触发止盈条件时刻开始，回撤达到指定点数则进行止盈操作 'Percent'：按照价格变化的百分比率止盈，从触发止盈条件时刻开始，回撤达到指定百分比则进行止盈操作
|OrderCtg	|char	|下单价格类型: 'market': 市价成交
|OrderTag	|char	|订单标记

- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|ClientOrderID	|int	|订单号

- 例子:

主策略函数

	    function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
        else
            % 买入下单
            orderID=traderBuyV2(1,1,1,0,'market','buy');
            % 当价格亏损 1 %时止损
            StopOrderID=traderStopLossByOrderV2(1, orderID, 1, 'Percent', 'market', 'stoplossB');
            % 当价格上涨20%之后，回撤2%将触发追踪止盈
            TrailingStopOrderID=traderStopTrailingByOrderV2(1, orderID, 20, 'Percent', 2, 'Percent', 'market', 'trailingB');    
	    end
    end

执行脚本

    clear all;
    clc;
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 按照15分钟的频率运行回测  
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');


- 注意：

1.使用止盈止损时设置的Point或者Percent，计算触发价格会根据该品种的最小变动单位四舍五入取整

2.Point指的是价格点数，并非最小变动单位


###traderPutLog


- 函数说明: （在策略结构中）构造 log 信息发送至 AT，不能在注册阶段使用


- 语法:

	`traderPutLog(Log)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|Log	|char	|需要在AT上面输出的文本信息


- 输出参数：

	无

- 例子:

主策略函数

	function matlab_example_test(bInit,bDayBegin,cellPar)%
	    global idexD;
	    % 三个参数的形式固定  
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
            
        else
            % 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
            traderPutLog('Welcome To AT')
	    end
    end

执行脚本：

    clear all;
    clc;
    % 设定需要传进策略的参数
    stoploss =0.9; % 设定止损比例
    m=5; % 设定双均线中的第一根均线周期
    n=10; % 设定双均线中的第二个均线周期
    % 设定回测账户
    AccountList(1) = {'FutureBackReplay'};
    % 设定
    TargetList(1).Market = 'SHFE';
    TargetList(1).Code = 'RB0000'; % 螺纹钢主力连续
    % 设定初始资金和费率，滑点等  
    traderSetBacktest(1000000, 0.000026,0.02,0);
    % 策略名为‘matlab_example_test’，每次刷新会调用matlab_example_test
    % 将{stoploss,m,n}参数传进策略
    % 使用FutureBackReplay这个回测账户
    % 以TargetList这结构体里的内容作为订阅标的
    % 按照15分钟的频率运行回测，每15分钟会刷新一次策略
    % 回测时间从20180102开始到20180103结束
    % 价格使用前复权价格
    traderRunBacktestV2('matlab_example_test',@matlab_example_test, {stoploss,m,n},AccountList,TargetList,'min',15,20180102,20180103,'FWard'); 


### traderRegUserIndi

- 函数说明: （在策略结构中的注册阶段）注册用户自建的外部函数。


- 语法:

	`Idx=traderRegUserIndi(F,cellPar)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|F	|函数对象	|因子计算函数
|cellPar	|cell|F函数入参，传递参数到自建函数中


- 输出参数:

|	|类型	|说明
|:-:|:-:|:-:|
|Idx	|double矩阵|返回因子序列的索引值，系统使用


- 示例:

在注册阶段中使用

    if bInit
	    %% 初始化回测帐户
	    % 数据只有先注册才能使用
	    % 基本数据注册
	    % traderRegKData('day',Freq).Freq为bar的周期。
	    % 自定义函数注册
	    % traderRegUserIndi(@Fun,{para1,para2,...})。
	    % Fun为自定义函数，其固定结构参考后面代码，大括号内为函数输入参数。
	    g_idxKOneMin = traderRegKData('min',1);%交易频率
	    g_idxKFiveMin = traderRegKData('min',Freq);%信号频率
	    g_idxSignal = traderRegUserIndi(@getSignal,{g_idxKFiveMin,nbar,range});
		
### traderGetRegUserIndi


- 函数说明:（在策略结构中）根据已注册的用户自建函数序列获取数据索引序列


- 语法:

	`traderGetRegUserIndi(Idx,len)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|Idx	|double矩阵	|注册数据时返回的索引序列矩阵
|Len	|整数	|获取自建函数返回值序列在当前时刻往前取Len个数据


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|Idx	|Any	|自定义输出值


- 示例:

在策略函数中

    if bInit
	    %% 初始化回测帐户
	    % 数据只有先注册才能使用
	    % 基本数据注册
	    % traderRegKData('day',Freq).Freq为bar的周期。
	    % 自定义函数注册
	    % traderRegUserIndi(@Fun,{para1,para2,...})。
	    % Fun为自定义函数，其固定结构参考后面代码，大括号内为函数输入参数。
	    g_idxKOneMin = traderRegKData('min',1);%交易频率
	    g_idxKFiveMin = traderRegKData('min',Freq);%信号频率
	    g_idxSignal = traderRegUserIndi(@getSignal,{g_idxKFiveMin,nbar,range});
	 
    else
	    %% 交易逻辑
	    %   交易启动、先平后开
	    targetList = traderGetTargetList(); % 获取标的信息。
	    TLen = length(targetList);%标的个数
	    Signal = traderGetRegUserIndi(g_idxSignal,1)
    end 

- 注意

1.自建函数返回的序列和K线的序列在时间上是一致的

###traderSetParalMode

- 函数说明: （在策略结构中的注册阶段）选择是否开启并行模式

- 语法:

	`traderSetParalMode(mode)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|mode	|logical|true代表并行开启，false代表运行关闭（默认为false）


- 输出参数:

无


- 示例:

在注册阶段中使用

    if bInit
    %% 初始化回测帐户
    % 数据只有先注册才能使用
    % 基本数据注册
    % traderRegKData('day',Freq).Freq为bar的周期。
    % 自定义函数注册
    % traderRegUserIndi(@Fun,{para1,para2,...})。
    % Fun为自定义函数，其固定结构参考后面代码，大括号内为函数输入参数。
    % 使用并行模式
    traderSetParalMode(true);
    g_idxKOneMin = traderRegKData('min',1);%交易频率
    g_idxKFiveMin = traderRegKData('min',Freq);%信号频率
    g_idxSignal = traderRegUserIndi(@getSignal,{g_idxKFiveMin,nbar,range});

###traderRegUserData

- 函数说明: （在策略结构中的注册阶段）注册用户自建的外部数据。

- 语法:

	`Idx=traderRegUserData(TimeLine,DataArray)`

- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|TimeLine|cell，或者矩阵	|导入数据的时间轴, 长度与数据序列保持一致
|DataArray	|cell，或者矩阵|导入的数据序列, 长度与时间轴保持一致


- 输出参数:

|字段|类型	|说明
|:-:|:-:|:-:|
|Idx	|double矩阵|返回因子序列的索引值，系统使用


- 示例:

在注册阶段中使用

        % 插入外部数据
        % 插入两个时间点
        T(1) = datenum(2018, 1, 2, 10, 00, 00); 
        T(2) = datenum(2018, 1, 3, 10, 10, 10);
        % 出入两个时间点上的数值
        D(1) = 2.6;
        D(2) = 3.8;
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
            % 注册外部数据
            userD=traderRegUserData(T, D);
			
###traderGetRegUserData

- 函数说明:（在策略结构中）根据已注册的用户的外部序列获取数据索引序列

- 语法:

	`traderGetRegUserData(Idx,len)`


- 输入参数:

|字段名	|类型	|说明
|:-:|:-:|:-:|
|Idx	|double矩阵	|注册数据时返回的索引序列矩阵
|Len	|整数	|获取外部数据序列在当前时刻往前取Len个数据


- 输出参数:

|	|类型	|说明
|:-:|:-:|:-:|
|Idx	|Any	|在traderRegUserData中定义的在当前时间点的数据


- 示例:

在策略函数中

    function matlab_example_test(bInit,bDayBegin,cellPar)%
        % 三个参数的形式固定 
	    global idexD;
        global userD;
        % 插入外部数据
        % 插入两个时间点
        T(1) = datenum(2018, 1, 2, 10, 00, 00); 
        T(2) = datenum(2018, 1, 3, 10, 10, 10);
        % 出入两个时间点上的数值
        D(1) = 2.6;
        D(2) = 3.8;
	    if bInit % 判定是否策略开启启动  
		    % 行情注册，15分钟的K线和5分钟的K线  
		    idexD=traderRegKData('min',15);
            % 注册外部数据
            userD=traderRegUserData(T, D);
        else
            % 获取所有标的在当前时刻往前5根K线的数据（15min频率）
            data=traderGetRegKData(idexD, 5, false);
            datestr(data(1,end))
			% 获取当前时刻往前3个时间点的外部数据序列
            userdata=traderGetRegUserData(userD,3)
	    end
    end

- 注意：

1.外部数据的序列和K线的序列在时间上是一致的
2.若当前刷新的时间点不在外部数据的时间序列上，则返回0


### traderSetParamCheck

- 函数说明: （在策略结构中的注册阶段）选择开启或关闭参数检查功能。


- 语法:

	`traderSetParamCheck(mode)`

- 输入参数:

|字段名|类型|说明
|:-:|:-:|:-:|
|mode|logical|true代表参数检查开启，false代表参数检查关闭（默认为false）

- 输出参数:

	无

- 示例:

在注册阶段中使用

    if bInit
	    % 开启参数检查模式
	    traderSetParalMode(true);


### traderClearCache

- 函数说明: 清除Matlab缓存数据。

- 语法:

	`traderClearCache`

- 输入参数:

	无

- 输出参数:

	无

- 示例:

当需要清除Matlab缓存时，在Command Window中输入

	traderClearCache

