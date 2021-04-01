
## MessageID
* **Type** `int64LE`

## UserID
* **Type** `int64LE`

## AccountID
* **Type** `int64LE`

## int64
* **Type** `int64LE`

## double
* **Type** `doubleLE`

## IS_AccountSignalType_s
* **Type** `struct`
* **Struct Inner Layout**
    - **AccountID** `int64LE`
    - **SignalType** `int32LE`
    - **BeginTime** `wchar_t[32]`
    - **EndTime** `wchar_t[32]` | 4 NULL

## IS_CircleAttribution_s
* **Type** `struct`
* **Struct Inner Layout**
    - **CircleID** `int64LE`
    - **ManagerID** `int64LE`
    - **CircleName** `wchar_t[32]`

## IS_CircleMessage_s
* **Type** `struct`
* **Struct Inner Layout**
    - **MesgID** `int64LE`
    - **CircleID** `int64LE`
    - **SenderID** `int64LE`
    - **RecipientID** `int64LE`
    - **MesgType** `int32LE`
    - **ReadFlag** `int32LE`
    - **CreateTime** `wchar_t[32]`
    - **ChangeTime** `wchar_t[32]`

## IS_ProfitRank_s
* **Type** `struct`
* **Struct Inner Layout**
    - **ID** `int64LE`
    - **ProfitP90** `doubleLE`

## IS_TradingPerformance_s
* **Type** `struct`
* **Struct Inner Layout**
    - **ProfitP7** `doubleLE`
    - **ProfitP30** `doubleLE`
    - **Profit6Months** `doubleLE`
    - **ProfitP90** `doubleLE`
    - **WinP90** `doubleLE`
    - **DrawdownP90** `doubleLE`
    - **ProfitP** `doubleLE`
    - **YearProfitP** `doubleLE`
    - **WinP** `doubleLE`
    - **Drawdown** `doubleLE`

## IS_UserRemark_s
* **Type** `struct`
* **Struct Inner Layout**
    - **ObserverID** `int64LE`
    - **ObjectID** `int64LE`
    - **ObjectRemark** `wchar_t[32]`

## IS_AccountFollowConcernDetail_s
* **Type** `struct`
* **Struct Inner Layout**
    - **FolloweeUserID** `int64LE`
    - **FolloweeAccountID** `int64LE`
    - **FollowerUserID** `int64LE`
    - **FollowerAccountID** `int64LE`
    - **BeginTime** `wchar_t[32]`
    - **EndTime** `wchar_t[32]`

## IS_DailyProfitP_s
* **Type** `struct`
* **Struct Inner Layout**
    - **TodayProfitP** `doubleLE`
    - **AccumulatedProfitP** `doubleLE`
    - **ProfitPDay** `wchar_t[32]`

## IS_StrategistBasicInfo_s
* **Type** `struct`
* **Struct Inner Layout**
    - **UserID** `int64LE`
    - **FollowNum** `int64LE`
    - **ProfitP** `doubleLE`
    - **WinP** `doubleLE`
    - **UserRemark** `wchar_t[32]`

## IS_UserCircleRank_s
* **Type** `struct`
* **Struct Inner Layout**
    - **CircleID** `int64LE`
    - **Rank** `int64LE`

## IS_StrategyBasicInfo_s
* **Type** `struct`
* **Struct Inner Layout**
    - **AccountID** `int64LE`
    - **FollowNum** `int64LE`
    - **ProfitP90** `doubleLE`
    - **DrawdownP90** `doubleLE`
    - **WinP** `doubleLE`

## IS_UserUserRelation_s
* **Type** `struct`
* **Struct Inner Layout**
    - **i64AUserID** `int64LE`
    - **i64BUserID** `int64LE`
    - **IS_UserUserRelation_e** `int32LE` | 4 NULL

## IS_UserAccountRelation_s
* **Type** `struct`
* **Struct Inner Layout**
    - **i64UserID** `int64LE`
    - **i64AccountID** `int64LE`
    - **IS_UserAccountRelation_e** `int32LE` | 4 NULL

## IS_AccountCurrentProfit_s
* **Type** `struct`
* **Struct Inner Layout**
    - **AccountID** `int64LE`
    - **CurrentProfit** `doubleLE`
