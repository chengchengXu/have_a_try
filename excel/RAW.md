
## 获取可跟踪用户列表
* **Command** `IS_GetTraceableUser`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回可跟踪用户列表
* **Command** `IS_ReturnTraceableUser`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`UserID[n]`** `UserID[n]` | n个可跟踪用户ID

## 获取可跟踪账户列表
* **Command** `IS_GetTraceableAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`TraceableUserID`** `int64` | 可跟踪用户ID

## 返回可跟踪账户列表
* **Command** `IS_ReturnTraceableAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`TraceableUserID`** `int64` | 可跟踪用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`AccountID[n]`** `AccountID[n]` | n个可跟踪账户ID

## 获取跟踪关注列表
* **Command** `IS_GetFollowConcern`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 被查询对象用户ID

## 返回跟踪关注列表
* **Command** `IS_ReturnFollowConcern`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 被查询对象用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_AccountFollowConcernDetail_s[n]`** `IS_AccountFollowConcernDetail_s[n]` | n个跟踪关注内容

## 获取手动账户
* **Command** `IS_GetManualAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户ID

## 返回手动账户
* **Command** `IS_ReturnManualAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_AccountSignalType_s[n]`** `IS_AccountSignalType_s[n]` | n个账户信号类型

## 获取圈子列表
* **Command** `IS_GetCircleList`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回圈子列表
* **Command** `IS_ReturnCircleList`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_CircleAttribution_s[n]`** `IS_CircleAttribution_s[n]` | n个圈子属性

## 获取圈子成员
* **Command** `IS_GetCircleMember`
* **Parameters**
    - **Header**
        + **`CircleID`** `int64` | 圈子ID

## 返回圈子成员
* **Command** `IS_ReturnCircleMember`
* **Parameters**
    - **Header**
        + **`CircleID`** `int64` | 圈子ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`UserID[n]`** `UserID[n]` | n个用户ID

## 获取圈子消息
* **Command** `IS_GetCircleMessage`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回圈子消息
* **Command** `IS_ReturnCircleMessage`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_CircleMessage_s[n]`** `IS_CircleMessage_s[n]` | n个圈子消息

## 获取圈主排名
* **Command** `IS_GetCircleMasterRank`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回圈主排名
* **Command** `IS_ReturnCircleMasterRank`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_ProfitRank_s[n]`** `IS_ProfitRank_s[n]` | n个收益排名

## 获取圈子成员排名
* **Command** `IS_GetCircleMemberRank`
* **Parameters**
    - **Header**
        + **`CircleID`** `int64` | 圈子ID

## 返回圈子成员排名
* **Command** `IS_ReturnCircleMemberRank`
* **Parameters**
    - **Header**
        + **`CircleID`** `int64` | 圈子ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_ProfitRank_s[n]`** `IS_ProfitRank_s[n]` | n个收益排名

## 获取圈子平均收益率排名
* **Command** `IS_GetCircleAverageRank`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回圈子平均收益率排名
* **Command** `IS_ReturnCircleAverageRank`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_ProfitRank_s[n]`** `IS_ProfitRank_s[n]` | n个收益排名

## 获取用户交易业绩
* **Command** `IS_GetUserTradingPerformance`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回用户交易业绩
* **Command** `IS_ReturnUserTradingPerformance`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果 | 默认true
    - **Buffer**
        + **`IS_TradingPerformance_s`** `IS_TradingPerformance_s` | 交易业绩

## 获取账户交易业绩
* **Command** `IS_GetAccountTradingPerformance`
* **Parameters**
    - **Header**
        + **`AccountID`** `int64` | 账户ID

## 返回账户交易业绩
* **Command** `IS_ReturnAccountTradingPerformance`
* **Parameters**
    - **Header**
        + **`AccountID`** `int64` | 账户ID
        + **`result`** `string` | 操作结果 | 默认true
    - **Buffer**
        + **`IS_TradingPerformance_s`** `IS_TradingPerformance_s` | 交易业绩

## 获取交易散点图
* **Command** `IS_GetTradingScatterplot`
* **Parameters**
    - **Header**
        + **`AccountID`** `int64` | 账户ID

## 返回交易散点图
* **Command** `IS_ReturnTradingScatterplot`
* **Parameters**
    - **Header**
        + **`AccountID`** `int64` | 账户ID
        + **`result`** `string` | 操作结果 | 默认true
    - **Buffer**
        + **`Trading[n]`** `double[n]` | n个交易点

## 获取用户备注
* **Command** `IS_GetUserRemark`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回用户备注
* **Command** `IS_ReturnUserRemark`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_UserRemark_s[n]`** `IS_UserRemark_s[n]` | n个用户备注信息

## 获取账户信号类型
* **Command** `IS_GetAccountSignalType`
* **Parameters**
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户ID

## 返回账户信号类型
* **Command** `IS_ReturnAccountSignalType`
* **Parameters**
    - **Header**
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_AccountSignalType_s[n]`** `IS_AccountSignalType_s[n]` | n个账户信号类型

## 获取可用于跟踪账户
* **Command** `IS_GetFreeFollowAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户ID

## 返回可用于跟踪账户
* **Command** `IS_ReturnFreeFollowAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_AccountSignalType_s[n]`** `IS_AccountSignalType_s[n]` | n个账户信号类型

## 获取可用于交易账户
* **Command** `IS_GetFreeTradeAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户ID

## 返回可用于交易账户
* **Command** `IS_ReturnFreeTradeAccount`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_AccountSignalType_s[n]`** `IS_AccountSignalType_s[n]` | n个账户信号类型

## 获取用户日收益率
* **Command** `IS_GetUserDailyProfitP`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回用户日收益率
* **Command** `IS_ReturnUserDailyProfitP`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_DailyProfitP_s[n]`** `IS_DailyProfitP_s[n]` | n个日收益率类型

## 获取策略师基础信息
* **Command** `IS_GetStrategistBasicInfo`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`UserID[n]`** `int64[n]` | n个策略师ID

## 返回策略师基础信息
* **Command** `IS_ReturnStrategistBasicInfo`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_StrategistBasicInfo_s[n]`** `IS_StrategistBasicInfo_s[n]` | n个策略师基础信息类型

## 获取用户所在圈子排名
* **Command** `IS_GetUserCircleRank`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户DI

## 返回用户所在圈子排名
* **Command** `IS_ReturnUserCircleRank`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
        + **`ProfitP90`** `double` | 用户90天收益率
    - **Buffer**
        + **`IS_UserCircleRank_s[n]`** `IS_UserCircleRank_s[n]` | n个用户所在圈子排名类型

## 获取策略基础信息
* **Command** `IS_GetStrategyBasicInfo`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户(策略)ID

## 返回策略基础信息
* **Command** `IS_ReturnStrategyBasicInfo`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_StrategyBasicInfo_s[n]`** `IS_StrategyBasicInfo_s[n]` | n个策略基础信息类型

## 获取用户间关系
* **Command** `IS_GetUserUserRelation`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`UserID[n]`** `UserID[n]` | n个用户ID

## 返回用户间关系
* **Command** `IS_ReturnUserUserRelation`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_UserUserRelation_s[n]`** `IS_UserUserRelation_s[n]` | n个用户间关系类型

## 获取用户账户关系
* **Command** `IS_GetUserAccountRelation`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户ID

## 返回用户账户关系
* **Command** `IS_ReturnUserAccountRelation`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_UserAccountRelation_s[n]`** `IS_UserAccountRelation_s[n]` | n个用户账户关系类型

## 获取用户账户当前权益
* **Command** `IS_GetAccountCurrentProfit`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`AccountID[n]`** `int64[n]` | n个账户ID

## 返回用户账户当前权益
* **Command** `IS_ReturnAccountCurrentProfit`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_AccountCurrentProfit_s[n]`** `IS_AccountCurrentProfit_s[n]` | n个账户当前权益类型

## 获取未读消息数
* **Command** `IS_GetNotReadMessageNumber`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID

## 返回未读消息数
* **Command** `IS_ReturnNotReadMessageNumber`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果
        + **`NotReadMessage`** `int64` | 未读消息数

## 设置阅读消息
* **Command** `IS_ReadCircleMessage`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
    - **Buffer**
        + **`MessageID[n]`** `MessageID[n]` | n个圈子消息类型

## 阅读消息结果
* **Command** `IS_ReadCircleMessage`
* **Parameters**
    - **Header**
        + **`UserID`** `int64` | 用户ID
        + **`result`** `string` | 操作结果

## 获取账户日收益率
* **Command** `IS_GetAccountDailyProfitP`
* **Parameters**
    - **Header**
        + **`AccountID`** `int64` | 账户ID

## 返回账户日收益率
* **Command** `IS_ReturnAccountDailyProfitP`
* **Parameters**
    - **Header**
        + **`AccountID`** `int64` | 账户ID
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_DailyProfitP_s[n]`** `IS_DailyProfitP_s[n]` | n个日收益率类型

## 获取推荐圈子
* **Command** `IS_GetRecommendedCircle`

## 返回推荐圈子
* **Command** `IS_ReturnRecommendedCircle`
* **Parameters**
    - **Header**
        + **`result`** `string` | 操作结果
    - **Buffer**
        + **`IS_CircleAttribution_s[n]`** `IS_CircleAttribution_s[n]` | n个圈子属性
