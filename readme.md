## 无人售货机订单导入
### 项目说明
对接无人售货机系统goBox,python 代码是后端同事完成的。
### 1.数据模型

#### 1.set\_of_book

字段名|类型|描述
----|---|----
id|int|唯一标识
set\_of_book|string|账套号
app_key|string|密钥
user_name|string|用户名
access_token|string|令牌
token\_created_at|datetime|令牌获取时间
expired_at|datetime|过期时间
token|string|本地令牌
updated_at|datetime|更新时间
updated_user|string|更新用户


#### 2.device

字段名|类型|描述
----|----|----
id|int|唯一标识
set\_of_book|string|账套号
name|string|货柜名称
dev_id|int|设备id
store_id|int|仓库id
bank_id|int|收款账户id
member_id|int|会员id
employee_id|int|员工id
bill_type|int|发票类型
created_at|datetime|创建时间
created_user|string|创建用户
updated_at|datetime|更新时间
updated_user|string|更新用户


#### 3.orders

字段名|类型|描述
----|----|----
id|int|唯一标识
set\_of_book|string|账套号
trans_id|string|交易id
status|int|交易状态
e_id|string|用户id
dev_id|int|设备id
create_time|datetime|订单创建时间
update_time|datetime|订单状态最终更新时间
total_amount|float|订单总金额
products|json|商品明细
created_at|datetime|下载时间
created_user|string|下载用户
is_imported|boolean|是否已导入
imported_at|datetime|导入时间
imported_user|string|导入用户
retail_id|int|零售单id
retail_code|string|零售单code


### 2.接口

#### 2.1 /api/create_order post  接收订单消息(第三方使用)

	* 传递参数
	
		* headers
			
			* Token 令牌(由c8这边提供给第三方)
		
		* body
	
			* trans_id 交易id
			* status 交易状态
			* e_id 用户id
			* dev_id 设备id
			* create_time 订单创建时间
			* update_time 订单状态最终更新时间
			* products 商品列表 list
	
				* barcode 商品barcode
				* name 商品名称
				* num 商品数量
				* amount 交易金额
				* cost 商品成本
		
	* 返回信息
	
		* 成功时: {"status": 1}
		* 失败时: {"status": 0, "errmsg": 错误信息}

#### 2.2 /api/access_token  get 获取token,调用其他接口时需要在headers中传递该token

	* 传递参数 params
	
		* url c8地址
		* set_of_book 账套号
		* user_name 用户名称
	* headers
	
		* Token c8的令牌
	
	* 返回数据
	
		* 成功时:{"state": 1, "token": 令牌}
		* 出错时:{"state": 0, "errmsg": 错误信息}

#### 2.3 /api/set\_of_books 获取账套设置

	* 传递参数

		* set_of_book 账套号

	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1, "id": 账套id, "set_of_book": 账套号,"app_key": 密钥, "user_name": 用户名, 
		"access_token": 令牌, "token_created_at": 令牌获取时间, "expired_at": 令牌过期时间, "token": 本地令牌,
		"updated_at": 更新时间, "updated_user": 更新用户}
		* 出错时:{"state": 0, "errmsg": 错误信息}


#### 2.4 /api/set\_of_books/[id] put 更新账套设置

	* 传递参数 data

		* app_key 密钥
		* user_name 用户名
		
	* headers
	
		* Token 独立的token
	
	* 返回数据
	
		* 成功时:{"state": 1, "id": 账套id, "set_of_book": 账套号,"app_key": 密钥, "user_name": 用户名, 
		"access_token": 令牌, "token_created_at": 令牌获取时间, "expired_at": 令牌过期时间, "token": 本地令牌,
		"updated_at": 更新时间, "updated_user": 更新用户}
		* 出错时:{"state": 0, "errmsg": 错误信息}


#### 2.5 /api/devices post 创建货柜配置

	* 传递参数 data

		* name 货柜名称
		* dev_id 设备id
		* store_id 仓库id
		* bank_id 收款账户
		* member_id 会员id
		* employee_id 员工id
		* bill_type 发票类型
	
	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1, "id": 货柜id, "set_of_book": 账套号, "name": 货柜名称, "dev_id": 设备id,
		 "store_id": 仓库id, "bank_id": 收款账户id, "member_id": 会员id, "employee_id": 员工id, "bill_type": 
		 发票类型, "created_at": 创建时间, "created_user": 创建用户, "updated_at": 更新时间, "updated_user": 更新用户}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.5 /api/devices get 获取货柜列表

	* 传递参数

		* name 货柜名称(可传)
		* start 分页参数
		* limit 分页参数

	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1, "total": 总数量, "root": [{"id": 货柜id, "set_of_book": 账套号, "name": 货柜名称, "dev_id": 设备id,
		 "store_id": 仓库id, "bank_id": 收款账户id, "member_id": 会员id, "employee_id": 员工id, "bill_type": 
		 发票类型, "created_at": 创建时间, "created_user": 创建用户, "updated_at": 更新时间, "updated_user": 更新用户}]}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.6 /api/devices/[id] get 获取单个货柜信息

	* 传递参数

		* 无

	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1, "id": 货柜id, "set_of_book": 账套号, "name": 货柜名称, "dev_id": 设备id,
		 "store_id": 仓库id, "bank_id": 收款账户id, "member_id": 会员id, "employee_id": 员工id, "bill_type": 
		 发票类型, "created_at": 创建时间, "created_user": 创建用户, "updated_at": 更新时间, "updated_user": 更新用户}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.7 /api/devices/[id] put 更新货柜信息

	* 传递参数 data

		* name 货柜名称
		* dev_id 设备id
		* store_id 仓库id
		* bank_id 收款账户
		* member_id 会员id
		* employee_id 员工id
		* bill_type 发票类型
	
	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1, "id": 货柜id, "set_of_book": 账套号, "name": 货柜名称, "dev_id": 设备id,
		 "store_id": 仓库id, "bank_id": 收款账户id, "member_id": 会员id, "employee_id": 员工id, "bill_type": 
		 发票类型, "created_at": 创建时间, "created_user": 创建用户, "updated_at": 更新时间, "updated_user": 更新用户}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.8 /api/devices/[id] delete 删除货柜信息

	* 传递参数

		* 无

	* headers

		* Token 令牌

	* 返回数据

		* 成功时: {"state": 1}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.9 /api/orders?action=get_orders get 下载订单列表

	* 传递参数

		* start_date 开始时间
		* end_date 结束时间（注: 时间区间最长一周）
		* dev_id 设备id号
		* trans_id 交易id
		* status 交易状态{100:支付成功,101:等待支付,102:等待退款,103:退款成功,104:退款失败,105:交易关闭,107:支付失败,
		109:交易异常,110:重新退款}
		
	* headers

		* Token 令牌

	* 返回数据

		* 成功时: {"state": 1, "page": 下一页页码数, 为None时表示没有下一页}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.10 /api/orders?action=trade_view get 查询订单列表

	* 传递参数

		* dev_id 设备id
		* start_date 开始时间
		* end_date 结束时间
		* status 订单状态
		* is_imported 导入状态(0或1)
		* trans_id 交易编号
		* start 分页参数
		* limit 分页参数

	* headers

		* Token 令牌

	* 返回数据

		* 成功时: {"state": 1, "total":总行数, "root":[{"id": id, "set_of_book": 账套号, "trans_id": 交易id, 
		"status": 订单状态, "e_id": 用户id, "dev_id": 设备id, "create_time": 订单创建时间, "update_time": 订单状态
		最终更新时间, "total_amount": 订单总金额, "products": 商品明细列表, "created_at": 订单下载时间, "created_user":下载用户, "is_imported": 是否已导入, "imported_at": 导入时间, "imported_user": 导入用户, "retail_id": 零售单id,"retail_code": 零售单单号}]}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.11 /api/orders/[id]?action=import get 导入c8

	* 传递参数

		* 无

	* headers

		* Token 令牌

	* 返回数据

		* 成功时: {"state": 1}
		* 出错时: {"state": 0, "errmsg": 错误信息}

#### 2.12 /api/orders/[id]?action=init_order get 状态重置

	* 传递参数

		* 无

	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1}
		* 出错时:{"state": 0, "errmsg": 错误信息}

#### 2.13 /api/orders/[id] delete 删除订单

	* 传递参数

		* 无

	* headers

		* Token 令牌

	* 返回数据

		* 成功时:{"state": 1}
		* 出错时:{"state": 0, "errmsg": 错误信息}
