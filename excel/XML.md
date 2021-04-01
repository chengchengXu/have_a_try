
## 添加跟踪关注
* **Command** `IS_AddFollowConcern`
* **Parameters**
 - **`FolloweeUserID`** 领跑用户ID
 - **`FolloweeAccountID`** 领跑账户ID
 - **`FollowerUserID`** 跟跑用户ID

## 删除跟踪关注
* **Command** `IS_DelFollowConcern`
* **Parameters**
 - **`FolloweeUserID`** 领跑用户ID
 - **`FolloweeAccountID`** 领跑账户ID
 - **`FollowerUserID`** 跟跑用户ID

## 开始跟踪
* **Command** `IS_StartFollow`
* **Parameters**
 - **`FolloweeUserID`** 领跑用户ID
 - **`FolloweeAccountID`** 领跑账户ID
 - **`FollowerUserID`** 跟跑用户ID
 - **`FollowerAccountID`** 跟跑账户ID

## 关闭跟踪
* **Command** `IS_StopFollow`
* **Parameters**
 - **`FolloweeUserID`** 领跑用户ID
 - **`FolloweeAccountID`** 领跑账户ID
 - **`FollowerUserID`** 跟跑用户ID
 - **`FollowerAccountID`** 跟跑账户ID

## 添加跟踪时间
* **Command** `IS_AddFollowTime`
* **Parameters**
 - **`FolloweeUserID`** 领跑用户ID
 - **`FolloweeAccountID`** 领跑账户ID
 - **`FollowerUserID`** 跟跑用户ID
 - **`FollowerAccountID`** 跟跑账户ID
 - **`EndTime`** 跟踪结束时间

## 删除跟踪时间
* **Command** `IS_DelFollowTime`
* **Parameters**
 - **`FolloweeUserID`** 领跑用户ID
 - **`FolloweeAccountID`** 领跑账户ID
 - **`FollowerUserID`** 跟跑用户ID
 - **`FollowerAccountID`** 跟跑账户ID

## 开始发布
* **Command** `IS_StartPublish`
* **Parameters**
 - **`UserID`** 发布用户
 - **`AccountID`** 发布账户

## 关闭发布
* **Command** `IS_StopPublish`
* **Parameters**
 - **`UserID`** 发布用户
 - **`AccountID`** 发布账户

## 添加发布时间
* **Command** `IS_AddPublishTime`
* **Parameters**
 - **`UserID`** 发布用户
 - **`AccountID`** 发布账户
 - **`EndTime`** 发布结束时间

## 删除发布时间
* **Command** `IS_DelPublishTime`
* **Parameters**
 - **`UserID`** 发布用户
 - **`AccountID`** 发布账户

## 邀请加入
* **Command** `IS_InviteToIn`
* **Parameters**
 - **`InviterID`** 邀请者ID
 - **`InviteeID`** 被邀请者ID

## 接受邀请(邀请成功)
* **Command** `IS_InviteSucceed`
* **Parameters**
 - **`MessageID`** 消息ID

## 拒绝邀请(邀请失败)
* **Command** `IS_InviteFail`
* **Parameters**
 - **`MessageID`** 消息ID

## 申请加入
* **Command** `IS_RequestToIn`
* **Parameters**
 - **`RequesterID`** 申请者ID
 - **`RequesteeID`** 被申请者ID

## 接受申请(申请成功)
* **Command** `IS_RequestSucceed`
* **Parameters**
 - **`MessageID`** 消息ID

## 拒绝申请(申请失败)
* **Command** `IS_RequestFail`
* **Parameters**
 - **`MessageID`** 消息ID

## 移出圈子用户
* **Command** `IS_RemoveCircleMember`
* **Parameters**
 - **`ManagerID`** 圈主ID
 - **`MemberID`** 成员ID

## 退出圈子
* **Command** `IS_QuitCircle`
* **Parameters**
 - **`ManagerID`** 圈主ID
 - **`MemberID`** 成员ID

## 删除圈子消息
* **Command** `IS_DeleteCircleMessage`
* **Parameters**
 - **`MessageID`** 消息ID

## 设置用户备注
* **Command** `IS_SetUserRemark`
* **Parameters**
 - **`ObserverID`** 观察者ID
 - **`ObjectID`** 对象ID
 - **`ObjectRemark`** 对象备注

## 设置圈子自动通过请求
* **Command** `IS_AutoLetOthersIn`
* **Parameters**
 - **`UserID`** 圈主ID
 - **`AutoLetOthersIn`** 自动开关 | 0关闭，1开启
