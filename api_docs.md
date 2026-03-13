# Backend API 文档

本文档详细描述了 ADP Backend 的所有 API 接口，包括接口地址、请求方法、参数说明和代码定义位置。

## 目录

1. [系统接口](#1-系统接口)
2. [用户认证接口](#2-用户认证接口)
3. [智能体(Agent)接口](#3-智能体agent接口)
4. [聊天(Chat)接口](#4-聊天chat接口)
5. [收藏夹(Collection)接口](#5-收藏夹collection接口)
6. [知识库(Knowledge Base)接口](#6-知识库knowledge-base接口)
7. [文档(Document)接口](#7-文档document接口)
8. [数据集(Dataset)接口](#8-数据集dataset接口)
9. [任务(Task)接口](#9-任务task接口)
10. [流水线(Pipeline)接口](#10-流水线pipeline接口)
11. [模板(Template)接口](#11-模板template接口)
12. [组织(Organization)接口](#12-组织organization接口)
13. [系统配置(System Config)接口](#13-系统配置system-config接口)
14. [OpenAPI 接口](#14-openapi-接口)
15. [管理员接口](#15-管理员接口)
16. [会话(Conversation)接口](#16-会话conversation接口)
17. [第三方接口](#17-第三方接口)
18. [LLM 聊天接口](#18-llm-聊天接口)
19. [训练(Train)接口](#19-训练train-接口)
20. [HF 数据集接口 (LocalFS)](#20-hf-数据集接口-localfs)

---

## 1. 系统接口

### 1.1 健康检查
- **URL**: `/health/`
- **方法**: GET
- **描述**: 服务健康检查接口
- **响应**: HTTP 200
- **代码位置**: [`core/urls.py:24`](core/urls.py#L24)

### 1.2 API 文档
- **Swagger UI**: `/api/docs/` 或 `/api/docs`
- **ReDoc**: `/api/redoc/` 或 `/api/redoc`
- **OpenAPI Schema**: `/api/schema/` 或 `/api/schema`
- **代码位置**: [`core/urls.py:32-37`](core/urls.py#L32)

---

## 2. 用户认证接口

基础路径: `/api/v1/`

### 2.1 用户登录
- **URL**: `/api/v1/login`
- **方法**: POST
- **描述**: 邮箱密码登录
- **请求参数**:
  - `email`: 邮箱地址
  - `password`: 密码
- **代码位置**: [`user/urls.py:17`](user/urls.py#L17), [`user/auth_service.py`](user/auth_service.py)

### 2.2 手机号登录
- **URL**: `/api/v1/login/phone`
- **方法**: POST
- **描述**: 手机号短信验证码登录
- **请求参数**:
  - `phone`: 手机号
  - `code`: 短信验证码
- **代码位置**: [`user/urls.py:27`](user/urls.py#L27)

### 2.3 发送登录短信验证码
- **URL**: `/api/v1/login/sms/code`
- **方法**: POST
- **描述**: 发送登录用短信验证码
- **请求参数**:
  - `phone`: 手机号
- **代码位置**: [`user/urls.py:28`](user/urls.py#L28)

### 2.4 用户注册
- **URL**: `/api/v1/register`
- **方法**: POST
- **描述**: 邮箱注册
- **请求参数**:
  - `email`: 邮箱地址
  - `password`: 密码
  - `code`: 邮箱验证码
- **代码位置**: [`user/urls.py:20`](user/urls.py#L20)

### 2.5 手机号注册
- **URL**: `/api/v1/register/sms`
- **方法**: POST
- **描述**: 手机号短信注册
- **请求参数**:
  - `phone`: 手机号
  - `code`: 短信验证码
- **代码位置**: [`user/urls.py:29`](user/urls.py#L29)

### 2.6 发送邮箱验证码
- **URL**: `/api/v1/email/code`
- **方法**: POST
- **描述**: 发送邮箱验证码
- **请求参数**:
  - `email`: 邮箱地址
- **代码位置**: [`user/urls.py:21`](user/urls.py#L21)

### 2.7 发送短信验证码
- **URL**: `/api/v1/sms/code`
- **方法**: POST
- **描述**: 发送短信验证码
- **请求参数**:
  - `phone`: 手机号
- **代码位置**: [`user/urls.py:30`](user/urls.py#L30)

### 2.8 发送重置密码邮箱验证码
- **URL**: `/api/v1/password/reset/code`
- **方法**: POST
- **描述**: 发送重置密码用的邮箱验证码
- **代码位置**: [`user/urls.py:22`](user/urls.py#L22)

### 2.9 发送重置密码短信验证码
- **URL**: `/api/v1/password/reset/code/sms`
- **方法**: POST
- **描述**: 发送重置密码用的短信验证码
- **请求参数**:
  - `phone`: 手机号
- **代码位置**: [`user/urls.py:31`](user/urls.py#L31)

### 2.10 重置密码（邮箱）
- **URL**: `/api/v1/password/reset`
- **方法**: POST
- **描述**: 通过邮箱验证码重置密码
- **请求参数**:
  - `email`: 邮箱地址
  - `code`: 验证码
  - `new_password`: 新密码
- **代码位置**: [`user/urls.py:23`](user/urls.py#L23)

### 2.11 重置密码（短信）
- **URL**: `/api/v1/password/reset/sms`
- **方法**: POST
- **描述**: 通过短信验证码重置密码
- **请求参数**:
  - `phone`: 手机号
  - `code`: 验证码
  - `new_password`: 新密码
- **代码位置**: [`user/urls.py:32`](user/urls.py#L32)

### 2.12 Token 刷新
- **URL**: `/api/v1/refresh`
- **方法**: POST
- **描述**: 刷新访问令牌
- **代码位置**: [`user/urls.py:18`](user/urls.py#L18)

### 2.13 用户登出
- **URL**: `/api/v1/logout`
- **方法**: POST
- **描述**: 用户登出
- **代码位置**: [`user/urls.py:19`](user/urls.py#L19)

### 2.14 获取用户信息
- **URL**: `/api/v1/users/info`
- **方法**: GET
- **描述**: 获取当前登录用户信息
- **代码位置**: [`user/urls.py:15`](user/urls.py#L15), [`user/views.py:99`](user/views.py#L99)

### 2.15 同步用户信息
- **URL**: `/api/v1/users/sync`
- **方法**: PUT
- **描述**: 同步/更新用户信息
- **代码位置**: [`user/urls.py:14`](user/urls.py#L14), [`user/views.py:88`](user/views.py#L88)

### 2.16 微信二维码登录

#### 生成二维码
- **URL**: `/api/v1/wechat/qr/generate`
- **方法**: GET
- **描述**: 生成微信登录二维码
- **代码位置**: [`user/urls.py:35`](user/urls.py#L35)

#### 检查二维码状态
- **URL**: `/api/v1/wechat/qr/status`
- **方法**: GET
- **描述**: 检查微信登录二维码扫描状态
- **代码位置**: [`user/urls.py:36`](user/urls.py#L36)

#### 微信回调
- **URL**: `/api/v1/wechat/callback`
- **方法**: GET
- **描述**: 微信 OAuth 回调接口
- **代码位置**: [`user/urls.py:37`](user/urls.py#L37)

### 2.17 GitHub OAuth 登录

#### 生成登录链接
- **URL**: `/api/v1/github/auth/generate`
- **方法**: GET
- **描述**: 生成 GitHub 授权登录链接
- **代码位置**: [`user/urls.py:40`](user/urls.py#L40)

#### 检查登录状态
- **URL**: `/api/v1/github/auth/status`
- **方法**: GET
- **描述**: 检查 GitHub 登录状态
- **代码位置**: [`user/urls.py:41`](user/urls.py#L41)

#### GitHub 回调
- **URL**: `/api/v1/github/callback`
- **方法**: GET
- **描述**: GitHub OAuth 回调接口
- **代码位置**: [`user/urls.py:42`](user/urls.py#L42)

### 2.18 邀请码管理

#### 获取邀请码列表
- **URL**: `/api/v1/invite-codes`
- **方法**: GET
- **描述**: 获取所有邀请码列表（管理员权限）
- **代码位置**: [`user/urls.py:45`](user/urls.py#L45), [`user/views.py:129`](user/views.py#L129)

#### 创建邀请码
- **URL**: `/api/v1/invite-codes`
- **方法**: POST
- **描述**: 创建新的邀请码（管理员权限）
- **请求参数**:
  - `code`: 邀请码
  - `description`: 描述（可选）
  - `max_uses`: 最大使用次数（默认 1）
  - `expires_at`: 过期时间（可选）
- **代码位置**: [`user/urls.py:45`](user/urls.py#L45), [`user/views.py:153`](user/views.py#L153)

#### 更新邀请码
- **URL**: `/api/v1/invite-codes/<int:invite_code_id>`
- **方法**: PUT
- **描述**: 更新邀请码信息（管理员权限）
- **代码位置**: [`user/urls.py:46`](user/urls.py#L46), [`user/views.py:208`](user/views.py#L208)

#### 删除邀请码
- **URL**: `/api/v1/invite-codes/<int:invite_code_id>`
- **方法**: DELETE
- **描述**: 删除邀请码（管理员权限）
- **代码位置**: [`user/urls.py:46`](user/urls.py#L46), [`user/views.py:247`](user/views.py#L247)

### 2.19 发送反馈
- **URL**: `/api/v1/feedback`
- **方法**: POST
- **描述**: 发送用户反馈
- **代码位置**: [`user/urls.py:24`](user/urls.py#L24)

---

## 3. 智能体(Agent)接口

基础路径: `/api/v1/`
- **URL 配置**: [`agent/urls.py`](agent/urls.py)
- **视图代码**: [`agent/views.py`](agent/views.py)

### 3.1 智能体列表/详情
- **URL**: `/api/v1/agents`
- **URL**: `/api/v1/agents/<str:agent_id>`
- **方法**: GET
- **描述**: 获取智能体列表或指定智能体详情
- **查询参数**:
  - `page`: 页码（可选）
  - `page_size`: 每页数量（可选）
  - `list_type`: 列表类型（可选）
  - `keyword`: 搜索关键词（可选）
  - `source`: 来源，如 share（可选）
- **代码位置**: [`agent/urls.py:15-16`](agent/urls.py#L15), [`agent/views.py:154`](agent/views.py#L154)

### 3.2 创建智能体
- **URL**: `/api/v1/agents`
- **方法**: POST
- **描述**: 创建新的智能体
- **请求参数**:
  - `title`: 标题
  - `description`: 描述（可选）
  - `collection_and_kbs`: 知识库集合（可选）
  - `tools`: 工具列表（可选）
  - `type`: 类型（可选）
- **代码位置**: [`agent/urls.py:15`](agent/urls.py#L15), [`agent/views.py:191`](agent/views.py#L191)

### 3.3 更新智能体
- **URL**: `/api/v1/agents/<str:agent_id>`
- **方法**: PUT
- **描述**: 更新指定智能体信息
- **代码位置**: [`agent/urls.py:16`](agent/urls.py#L16), [`agent/views.py:213`](agent/views.py#L213)

### 3.4 删除智能体
- **URL**: `/api/v1/agents/<str:agent_id>`
- **方法**: DELETE
- **描述**: 删除指定智能体
- **代码位置**: [`agent/urls.py:16`](agent/urls.py#L16), [`agent/views.py:236`](agent/views.py#L236)

### 3.5 订阅/取消订阅智能体
- **URL**: `/api/v1/agents/<str:agent_id>/subscribe/<int:action>`
- **方法**: POST
- **描述**: 订阅或取消订阅智能体
- **参数**:
  - `action`: 1 表示订阅，0 表示取消订阅
- **代码位置**: [`agent/urls.py:17`](agent/urls.py#L17), [`agent/views.py:360`](agent/views.py#L360)

### 3.6 智能体工具管理

#### 创建工具
- **URL**: `/api/v1/agents/tools`
- **方法**: POST
- **描述**: 为智能体创建新工具
- **请求参数**:
  - `agent_id`: 智能体ID（可选）
  - `name`: 工具名称
  - `url`: 工具URL
  - `openapi_json_path`: OpenAPI JSON 路径
  - `endpoints`: 端点列表
- **代码位置**: [`agent/urls.py:7`](agent/urls.py#L7), [`agent/views.py:262`](agent/views.py#L262)

#### 更新工具
- **URL**: `/api/v1/agents/tools/<str:tools_id>`
- **方法**: PUT
- **描述**: 更新智能体工具
- **代码位置**: [`agent/urls.py:8`](agent/urls.py#L8), [`agent/views.py:286`](agent/views.py#L286)

#### 删除工具
- **URL**: `/api/v1/agents/tools/<str:tools_id>`
- **方法**: DELETE
- **描述**: 删除智能体工具
- **代码位置**: [`agent/urls.py:8`](agent/urls.py#L8), [`agent/views.py:326`](agent/views.py#L326)

### 3.7 获取收藏夹和知识库
- **URL**: `/api/v1/agents/collection-and-kbs`
- **方法**: GET
- **描述**: 获取用户的收藏夹和知识库列表
- **代码位置**: [`agent/urls.py:9`](agent/urls.py#L9), [`agent/views.py:382`](agent/views.py#L382)

### 3.8 获取收藏夹和知识库文档
- **URL**: `/api/v1/agents/collection-and-kbs/documents`
- **方法**: POST
- **描述**: 获取收藏夹和知识库的文档列表
- **代码位置**: [`agent/urls.py:10`](agent/urls.py#L10), [`agent/views.py:401`](agent/views.py#L401)

### 3.9 智能体分享提示
- **URL**: `/api/v1/agents/share/tips`
- **URL**: `/api/v1/agents/share/tips/<str:status>`
- **方法**: POST
- **描述**: 设置智能体分享提示状态
- **代码位置**: [`agent/urls.py:12-13`](agent/urls.py#L12), [`agent/views.py:414`](agent/views.py#L414)

---

## 4. 聊天(Chat)接口

基础路径: `/api/v1/`
- **URL 配置**: [`chat/urls.py`](chat/urls.py)
- **视图代码**: [`chat/views.py`](chat/views.py)

### 4.1 发送聊天消息
- **URL**: `/api/v1/chat`
- **方法**: POST
- **描述**: 向智能体发送消息并获取流式响应
- **请求参数**:
  - `agent_id`: 智能体ID（可选）
  - `conversation_id`: 会话ID（可选）
  - `question`: 问题内容
  - `collection_and_kbs`: 知识库范围（可选）
- **响应**: text/event-stream 流式响应
- **代码位置**: [`chat/urls.py:8`](chat/urls.py#L8), [`chat/views.py:74`](chat/views.py#L74)

### 4.2 会话管理

#### 获取会话列表
- **URL**: `/api/v1/chat/conversations`
- **方法**: GET
- **描述**: 获取用户的会话列表
- **查询参数**:
  - `type`: 类型，如 list
  - `page_size`: 每页数量
  - `page_num`: 页码
- **代码位置**: [`chat/urls.py:10`](chat/urls.py#L10), [`chat/views.py:105`](chat/views.py#L105)

#### 获取会话菜单
- **URL**: `/api/v1/chat/conversations/menu`
- **方法**: GET
- **描述**: 获取会话菜单列表
- **查询参数**:
  - `list_type`: 列表类型
- **代码位置**: [`chat/urls.py:11`](chat/urls.py#L11), [`chat/views.py:174`](chat/views.py#L174)

#### 获取会话详情
- **URL**: `/api/v1/chat/conversations/<str:conversation_id>`
- **方法**: GET
- **描述**: 获取指定会话详情
- **代码位置**: [`chat/urls.py:13`](chat/urls.py#L13), [`chat/views.py:107`](chat/views.py#L107)

#### 创建会话
- **URL**: `/api/v1/chat/conversations`
- **方法**: POST
- **描述**: 创建新会话
- **请求参数**:
  - `agent_id`: 智能体ID（可选）
  - `share_id`: 分享ID（可选）
  - `title`: 会话标题（可选）
- **代码位置**: [`chat/urls.py:10`](chat/urls.py#L10), [`chat/views.py:140`](chat/views.py#L140)

#### 更新会话
- **URL**: `/api/v1/chat/conversations/<str:conversation_id>`
- **方法**: PUT
- **描述**: 更新会话信息
- **代码位置**: [`chat/urls.py:13`](chat/urls.py#L13), [`chat/views.py:127`](chat/views.py#L127)

#### 删除会话
- **URL**: `/api/v1/chat/conversations/<str:conversation_id>`
- **方法**: DELETE
- **描述**: 删除指定会话
- **代码位置**: [`chat/urls.py:13`](chat/urls.py#L13), [`chat/views.py:166`](chat/views.py#L166)

### 4.3 获取会话问题列表
- **URL**: `/api/v1/chat/conversations/<str:conversation_id>/questions`
- **方法**: GET
- **描述**: 获取会话中的问题列表
- **查询参数**:
  - `page_num`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`chat/urls.py:14`](chat/urls.py#L14), [`chat/views.py:188`](chat/views.py#L188)

### 4.4 更新问题答案
- **URL**: `/api/v1/chat/questions/answer`
- **方法**: PUT
- **描述**: 更新问题的答案
- **代码位置**: [`chat/urls.py:16`](chat/urls.py#L16), [`chat/views.py:205`](chat/views.py#L205)

### 4.5 会话分享

#### 创建分享
- **URL**: `/api/v1/chat/share`
- **方法**: POST
- **描述**: 创建会话分享
- **请求参数**:
  - `conversation_id`: 会话ID
  - `question_ids`: 问题ID列表（可选）
- **代码位置**: [`chat/urls.py:18`](chat/urls.py#L18), [`chat/views.py:250`](chat/views.py#L250)

#### 获取分享详情
- **URL**: `/api/v1/chat/share/<str:share_id>`
- **方法**: GET
- **描述**: 获取分享详情
- **代码位置**: [`chat/urls.py:19`](chat/urls.py#L19), [`chat/views.py:252`](chat/views.py#L252)

### 4.6 获取文档总数
- **URL**: `/api/v1/chat/documents/total`
- **方法**: POST
- **描述**: 获取聊天相关文档总数
- **代码位置**: [`chat/urls.py:21`](chat/urls.py#L21), [`chat/views.py:226`](chat/views.py#L226)

### 4.7 获取可引用智能体
- **URL**: `/api/v1/chat/agents/referable`
- **方法**: GET
- **描述**: 获取可引用的智能体列表
- **代码位置**: [`chat/urls.py:22`](chat/urls.py#L22), [`chat/views.py:241`](chat/views.py#L241)

---

## 5. 收藏夹(Collection)接口

基础路径: `/api/v1/`
- **URL 配置**: [`collection/urls.py`](collection/urls.py)
- **视图代码**: [`collection/views.py`](collection/views.py)

### 5.1 获取收藏夹列表/详情
- **URL**: `/api/v1/collections`
- **URL**: `/api/v1/collections/<str:collection_id>`
- **方法**: GET
- **描述**: 获取收藏夹列表或指定收藏夹详情
- **查询参数**:
  - `list_type`: 列表类型（可选）
  - `page_size`: 每页数量（可选）
  - `page_num`: 页码（可选）
- **代码位置**: [`collection/urls.py:8`](collection/urls.py#L8), [`collection/views.py:139`](collection/views.py#L139)

### 5.2 创建收藏夹
- **URL**: `/api/v1/collections`
- **方法**: POST
- **描述**: 创建新收藏夹
- **请求参数**:
  - `knowledge_bases`: 知识库列表，包含 id 和 kb_id
- **代码位置**: [`collection/urls.py:8`](collection/urls.py#L8), [`collection/views.py:164`](collection/views.py#L164)

### 5.3 更新收藏夹
- **URL**: `/api/v1/collections/<str:collection_id>`
- **方法**: PUT
- **描述**: 更新收藏夹信息
- **代码位置**: [`collection/urls.py:12`](collection/urls.py#L12), [`collection/views.py:186`](collection/views.py#L186)

### 5.4 删除收藏夹
- **URL**: `/api/v1/collections/<str:collection_id>`
- **方法**: DELETE
- **描述**: 删除指定收藏夹
- **代码位置**: [`collection/urls.py:12`](collection/urls.py#L12), [`collection/views.py:202`](collection/views.py#L202)

### 5.5 收藏夹文档管理

#### 获取收藏夹文档
- **URL**: `/api/v1/collections/documents`
- **URL**: `/api/v1/collections/<str:collection_id>/documents`
- **方法**: GET
- **描述**: 获取收藏夹中的文档列表
- **代码位置**: [`collection/urls.py:9`](collection/urls.py#L9), [`collection/views.py:254`](collection/views.py#L254)

#### 添加文档到收藏夹
- **URL**: `/api/v1/collections/<str:collection_id>/documents`
- **方法**: PUT
- **描述**: 添加文档到收藏夹
- **代码位置**: [`collection/urls.py:11`](collection/urls.py#L11), [`collection/views.py:272`](collection/views.py#L272)

#### 从收藏夹删除文档
- **URL**: `/api/v1/collections/<str:collection_id>/documents`
- **方法**: DELETE
- **描述**: 从收藏夹删除文档
- **代码位置**: [`collection/urls.py:11`](collection/urls.py#L11), [`collection/views.py:286`](collection/views.py#L286)

### 5.6 获取公开智能体
- **URL**: `/api/v1/collections/pub-agents`
- **URL**: `/api/v1/collections/<str:collection_id>/pub-agents`
- **方法**: GET
- **描述**: 获取与收藏夹相关的公开智能体
- **代码位置**: [`collection/urls.py:10`](collection/urls.py#L10), [`collection/views.py:301`](collection/views.py#L301)

---

## 6. 知识库(Knowledge Base)接口

基础路径: `/api/v1/`
- **URL 配置**: [`knowledgebase/urls.py`](knowledgebase/urls.py)
- **视图代码**: [`knowledgebase/views.py`](knowledgebase/views.py)

### 6.1 获取知识库列表/详情
- **URL**: `/api/v1/knowledge-base`
- **URL**: `/api/v1/knowledge-base/<str:kb_id>`
- **方法**: GET
- **描述**: 获取知识库列表或指定知识库详情
- **查询参数**:
  - `page`: 页码（可选）
  - `page_size`: 每页数量（可选）
  - `list_type`: 列表类型（可选）
  - `group_id`: 分组ID（可选）
- **代码位置**: [`knowledgebase/urls.py:7`](knowledgebase/urls.py#L7), [`knowledgebase/views.py:151`](knowledgebase/views.py#L151)

### 6.2 创建知识库
- **URL**: `/api/v1/knowledge-base`
- **方法**: POST
- **描述**: 创建新知识库
- **请求参数**:
  - `title`: 标题
  - `description`: 描述（可选）
  - `type`: 类型
- **代码位置**: [`knowledgebase/urls.py:7`](knowledgebase/urls.py#L7), [`knowledgebase/views.py:191`](knowledgebase/views.py#L191)

### 6.3 更新知识库
- **URL**: `/api/v1/knowledge-base/<str:kb_id>`
- **方法**: PUT
- **描述**: 更新知识库信息
- **代码位置**: [`knowledgebase/urls.py:13`](knowledgebase/urls.py#L13), [`knowledgebase/views.py:215`](knowledgebase/views.py#L215)

### 6.4 删除知识库
- **URL**: `/api/v1/knowledge-base/<str:kb_id>`
- **方法**: DELETE
- **描述**: 删除指定知识库
- **代码位置**: [`knowledgebase/urls.py:13`](knowledgebase/urls.py#L13), [`knowledgebase/views.py:239`](knowledgebase/views.py#L239)

### 6.5 搜索知识库
- **URL**: `/api/v1/knowledge-base/search`
- **方法**: POST
- **描述**: 在知识库中搜索内容
- **请求参数**:
  - `kb_ids`: 知识库ID列表（可选）
  - `keyword`: 搜索关键词
  - `group_id`: 分组ID（可选）
  - `page_size`: 每页数量（可选）
  - `page_num`: 页码（可选）
- **代码位置**: [`knowledgebase/urls.py:8`](knowledgebase/urls.py#L8), [`knowledgebase/views.py:263`](knowledgebase/views.py#L263)

### 6.6 移动知识库文档
- **URL**: `/api/v1/knowledge-base/move`
- **方法**: POST
- **描述**: 将文档从一个知识库移动到另一个
- **请求参数**:
  - `docs`: 文档列表
  - `new_kb_id`: 目标知识库ID
- **代码位置**: [`knowledgebase/urls.py:12`](knowledgebase/urls.py#L12), [`knowledgebase/views.py:298`](knowledgebase/views.py#L298)

### 6.7 刷新知识库文档
- **URL**: `/api/v1/knowledge-base/refresh`
- **方法**: POST
- **描述**: 刷新知识库文档
- **请求参数**:
  - `kb_id`: 知识库ID
  - `doc_ids`: 文档ID列表（可选）
- **代码位置**: [`knowledgebase/urls.py:9`](knowledgebase/urls.py#L9), [`knowledgebase/views.py:367`](knowledgebase/views.py#L367)

### 6.8 知识库文档管理

#### 获取文档列表
- **URL**: `/api/v1/knowledge-base/<str:kb_id>/documents`
- **方法**: GET
- **描述**: 获取知识库中的文档列表
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`knowledgebase/urls.py:14`](knowledgebase/urls.py#L14), [`knowledgebase/views.py:330`](knowledgebase/views.py#L330)

#### 删除文档
- **URL**: `/api/v1/knowledge-base/<str:kb_id>/documents`
- **方法**: DELETE
- **描述**: 删除知识库中的文档
- **代码位置**: [`knowledgebase/urls.py:14`](knowledgebase/urls.py#L14), [`knowledgebase/views.py:344`](knowledgebase/views.py#L344)

### 6.9 知识库文件管理

#### 获取文件列表
- **URL**: `/api/v1/knowledge-base/<str:kb_id>/files`
- **方法**: GET
- **描述**: 获取知识库中的文件列表
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`knowledgebase/urls.py:15`](knowledgebase/urls.py#L15), [`knowledgebase/views.py:390`](knowledgebase/views.py#L390)

#### 上传文件
- **URL**: `/api/v1/knowledge-base/<str:kb_id>/files`
- **方法**: POST
- **描述**: 上传文件到知识库
- **代码位置**: [`knowledgebase/urls.py:15`](knowledgebase/urls.py#L15), [`knowledgebase/views.py:417`](knowledgebase/views.py#L417)

#### 删除文件
- **URL**: `/api/v1/knowledge-base/<str:kb_id>/files`
- **方法**: DELETE
- **描述**: 删除知识库中的文件
- **代码位置**: [`knowledgebase/urls.py:15`](knowledgebase/urls.py#L15), [`knowledgebase/views.py:443`](knowledgebase/views.py#L443)

### 6.10 搜索历史

#### 获取搜索历史
- **URL**: `/api/v1/knowledge-base/search/history`
- **方法**: GET
- **描述**: 获取知识库搜索历史
- **代码位置**: [`knowledgebase/urls.py:10`](knowledgebase/urls.py#L10), [`knowledgebase/views.py:471`](knowledgebase/views.py#L471)

#### 删除搜索历史
- **URL**: `/api/v1/knowledge-base/search/history/<int:index>`
- **方法**: DELETE
- **描述**: 删除指定索引的搜索历史
- **代码位置**: [`knowledgebase/urls.py:11`](knowledgebase/urls.py#L11), [`knowledgebase/views.py:479`](knowledgebase/views.py#L479)

---

## 7. 文档(Document)接口

基础路径: `/api/v1/`
- **URL 配置**: [`document/urls.py`](document/urls.py)

### 7.1 文档管理

#### 获取文档列表
- **URL**: `/api/v1/documents`
- **方法**: GET
- **描述**: 获取文档列表
- **代码位置**: [`document/urls.py:6`](document/urls.py#L6)

#### 获取文档详情
- **URL**: `/api/v1/documents/<str:kb_type>/<str:kb_id>/<int:doc_id>`
- **方法**: GET
- **描述**: 获取指定文档详情
- **代码位置**: [`document/urls.py:7`](document/urls.py#L7)

#### 删除文档
- **URL**: `/api/v1/documents/<str:kb_type>/<str:kb_id>/<int:doc_id>`
- **方法**: DELETE
- **描述**: 删除指定文档
- **代码位置**: [`document/urls.py:7`](document/urls.py#L7)

### 7.2 文档搜索
- **URL**: `/api/v1/documents/search`
- **方法**: GET/POST
- **描述**: 搜索文档
- **代码位置**: [`document/urls.py:8`](document/urls.py#L8)

### 7.3 获取公开智能体
- **URL**: `/api/v1/documents/pub-agents`
- **方法**: GET
- **描述**: 获取与文档相关的公开智能体
- **代码位置**: [`document/urls.py:9`](document/urls.py#L9)

### 7.4 生成预签名URL
- **URL**: `/api/v1/documents/presigned-url`
- **方法**: POST
- **描述**: 生成文档预签名URL
- **代码位置**: [`document/urls.py:10`](document/urls.py#L10)

### 7.5 获取文档URL
- **URL**: `/api/v1/documents/<str:kb_type>/<str:kb_id>/<int:doc_id>/url`
- **方法**: GET
- **描述**: 获取文档访问URL
- **代码位置**: [`document/urls.py:11`](document/urls.py#L11)

### 7.6 获取引用格式
- **URL**: `/api/v1/documents/<str:kb_type>/<str:kb_id>/<int:doc_id>/references/formats`
- **方法**: GET
- **描述**: 获取文档引用格式
- **代码位置**: [`document/urls.py:12`](document/urls.py#L12)

### 7.7 文档片段(Chunk)管理

#### 获取片段列表
- **URL**: `/api/v1/chunks`
- **方法**: GET
- **描述**: 获取文档片段列表
- **代码位置**: [`document/urls.py:15`](document/urls.py#L15)

#### 批量操作片段
- **URL**: `/api/v1/chunks/batch`
- **方法**: POST/PUT/DELETE
- **描述**: 批量操作文档片段
- **代码位置**: [`document/urls.py:16`](document/urls.py#L16)

#### 获取片段详情
- **URL**: `/api/v1/chunks/<str:kb_id>/<int:doc_id>/<int:chunk_id>`
- **方法**: GET
- **描述**: 获取指定文档片段详情
- **代码位置**: [`document/urls.py:17`](document/urls.py#L17)

#### 删除片段
- **URL**: `/api/v1/chunks/<str:kb_id>/<int:doc_id>/<int:chunk_id>`
- **方法**: DELETE
- **描述**: 删除指定文档片段
- **代码位置**: [`document/urls.py:17`](document/urls.py#L17)

#### 搜索片段
- **URL**: `/api/v1/chunks/search`
- **方法**: GET/POST
- **描述**: 搜索文档片段
- **代码位置**: [`document/urls.py:18`](document/urls.py#L18)

---

## 8. 数据集(Dataset)接口

基础路径: `/api/v2/` 和 `/api/v1/`

### 8.1 V2 版本接口
- **URL 配置**: [`apps/dataset/urls.py`](apps/dataset/urls.py)
- **ViewSet 代码**: [`apps/dataset/viewset/`](apps/dataset/viewset/)

#### 数据集管理（ViewSet）
- **URL**: `/api/v2/dataset/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 数据集CRUD操作
- **代码位置**: [`apps/dataset/urls.py:10`](apps/dataset/urls.py#L10), [`apps/dataset/viewset/Dataset.py`](apps/dataset/viewset/Dataset.py)

#### 文件管理（ViewSet）
- **URL**: `/api/v2/files/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 数据集文件CRUD操作
- **代码位置**: [`apps/dataset/urls.py:11`](apps/dataset/urls.py#L11), [`apps/dataset/viewset/DatasetFile.py`](apps/dataset/viewset/DatasetFile.py)

#### 对象存储管理（ViewSet）
- **URL**: `/api/v2/object_storage/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 对象存储配置CRUD操作
- **代码位置**: [`apps/dataset/urls.py:9`](apps/dataset/urls.py#L9), [`apps/dataset/viewset/ObjectStorage.py`](apps/dataset/viewset/ObjectStorage.py)

### 8.2 V1 版本接口
- **URL 配置**: [`apps/dataset/urls_v1.py`](apps/dataset/urls_v1.py)
- **视图代码**: [`apps/dataset/views/views_v1.py`](apps/dataset/views/views_v1.py)

#### 获取数据集列表/详情
- **URL**: `/api/v1/dataset`
- **URL**: `/api/v1/dataset/<str:dataset_id>`
- **方法**: GET
- **描述**: 获取数据集列表或详情
- **代码位置**: [`apps/dataset/urls_v1.py:8-9`](apps/dataset/urls_v1.py#L8)

#### 创建数据集
- **URL**: `/api/v1/dataset`
- **方法**: POST
- **描述**: 创建新数据集
- **代码位置**: [`apps/dataset/urls_v1.py:8`](apps/dataset/urls_v1.py#L8)

#### 更新数据集
- **URL**: `/api/v1/dataset/<str:dataset_id>`
- **方法**: PUT
- **描述**: 更新数据集信息
- **代码位置**: [`apps/dataset/urls_v1.py:9`](apps/dataset/urls_v1.py#L9)

#### 删除数据集
- **URL**: `/api/v1/dataset/<str:dataset_id>`
- **方法**: DELETE
- **描述**: 删除数据集
- **代码位置**: [`apps/dataset/urls_v1.py:9`](apps/dataset/urls_v1.py#L9)

#### 搜索历史
- **URL**: `/api/v1/dataset/search/history`
- **方法**: GET
- **描述**: 获取搜索历史
- **代码位置**: [`apps/dataset/urls_v1.py:11`](apps/dataset/urls_v1.py#L11)

#### 删除搜索历史
- **URL**: `/api/v1/dataset/search/history/<int:index>`
- **方法**: DELETE
- **描述**: 删除指定搜索历史
- **代码位置**: [`apps/dataset/urls_v1.py:12`](apps/dataset/urls_v1.py#L12)

#### 移动数据集文件
- **URL**: `/api/v1/dataset/move`
- **方法**: POST
- **描述**: 移动数据集文件
- **代码位置**: [`apps/dataset/urls_v1.py:13`](apps/dataset/urls_v1.py#L13)

#### 获取数据集文件
- **URL**: `/api/v1/dataset/<str:dataset_id>/files`
- **方法**: GET
- **描述**: 获取数据集文件列表
- **代码位置**: [`apps/dataset/urls_v1.py:15`](apps/dataset/urls_v1.py#L15)

#### 获取文件详情
- **URL**: `/api/v1/dataset/<str:dataset_id>/files/<str:file_id>`
- **方法**: GET
- **描述**: 获取文件详情
- **代码位置**: [`apps/dataset/urls_v1.py:16`](apps/dataset/urls_v1.py#L16)

#### 生成预签名URL
- **URL**: `/api/v1/presigned-url`
- **URL**: `/api/v1/dataset/file/url`
- **方法**: POST
- **描述**: 生成文件预签名URL
- **代码位置**: [`apps/dataset/urls_v1.py:17-18`](apps/dataset/urls_v1.py)

#### 第三方数据集列表
- **URL**: `/api/v1/third-party/list`
- **方法**: GET
- **描述**: 获取第三方数据集列表
- **代码位置**: [`apps/dataset/urls_v1.py:21`](apps/dataset/urls_v1.py)

#### 第三方数据集详情
- **URL**: `/api/v1/third-party/detail/<str:dataset_name>`
- **方法**: GET
- **描述**: 获取第三方数据集详情
- **代码位置**: [`apps/dataset/urls_v1.py:22`](apps/dataset/urls_v1.py)

#### 第三方数据集文件
- **URL**: `/api/v1/third-party/files/<str:dataset_name>`
- **方法**: GET
- **描述**: 获取第三方数据集文件列表
- **代码位置**: [`apps/dataset/urls_v1.py:23`](apps/dataset/urls_v1.py)

---

## 9. 任务(Task)接口

基础路径: `/api/v1/`
- **URL 配置**: [`task/urls.py`](task/urls.py)
- **视图代码**: [`task/views/__init__.py`](task/views/__init__.py)

### 9.1 任务管理

#### 获取任务列表/详情
- **URL**: `/api/v1/task`
- **URL**: `/api/v1/task/<str:id>`
- **方法**: GET
- **描述**: 获取任务列表或详情
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `status`: 状态筛选
  - `keyword`: 关键词搜索
- **代码位置**: [`task/urls.py:11`](task/urls.py#L11), [`task/views/__init__.py:75`](task/views/__init__.py#L75)

#### 创建任务
- **URL**: `/api/v1/task`
- **方法**: POST
- **描述**: 创建新任务
- **请求参数**:
  - `name`: 任务名称
  - `description`: 描述（可选）
  - `template_id`: 模板ID（可选）
  - `dataset_id`: 数据集ID（可选）
- **代码位置**: [`task/urls.py:11`](task/urls.py#L11), [`task/views/__init__.py:98`](task/views/__init__.py#L98)

#### 更新任务
- **URL**: `/api/v1/task/<str:id>`
- **方法**: PUT
- **描述**: 更新任务信息
- **代码位置**: [`task/urls.py:31`](task/urls.py#L31), [`task/views/__init__.py:121`](task/views/__init__.py#L121)

#### 删除任务
- **URL**: `/api/v1/task/<str:id>`
- **方法**: DELETE
- **描述**: 删除任务（软删除）
- **代码位置**: [`task/urls.py:31`](task/urls.py#L31), [`task/views/__init__.py:142`](task/views/__init__.py#L142)

### 9.2 从模板创建任务
- **URL**: `/api/v1/task/create-from-template`
- **方法**: POST
- **描述**: 从模板创建并启动任务
- **请求参数**:
  - `template_id`: 模板ID
  - `name`: 任务名称
  - `description`: 描述
  - `dataset_id`: 数据集ID（可选）
- **代码位置**: [`task/urls.py:13`](task/urls.py#L13), [`task/views/__init__.py:221`](task/views/__init__.py#L221)

### 9.3 异步从模板创建任务
- **URL**: `/api/v1/task/create-from-template-async`
- **方法**: POST
- **描述**: 异步从模板创建任务，立即返回任务ID
- **代码位置**: [`task/urls.py:14`](task/urls.py#L14), [`task/views/__init__.py:273`](task/views/__init__.py#L273)

### 9.4 生成 Pipeline URL
- **URL**: `/api/v1/task/generate-pipeline-url`
- **方法**: POST
- **描述**: 生成 Pipeline URL
- **代码位置**: [`task/urls.py:15`](task/urls.py#L15), [`task/views/__init__.py:190`](task/views/__init__.py#L190)

### 9.5 任务状态查询
- **URL**: `/api/v1/task/<str:task_id>/status`
- **方法**: GET
- **描述**: 查询任务状态
- **代码位置**: [`task/urls.py:18`](task/urls.py#L18), [`task/views/__init__.py:345`](task/views/__init__.py#L345)

### 9.6 任务操作
- **操作视图代码**: [`task/views/views_task_operation.py`](task/views/views_task_operation.py)

#### 启动任务
- **URL**: `/api/v1/task/<str:task_id>/start`
- **方法**: POST
- **描述**: 启动任务
- **代码位置**: [`task/urls.py:20`](task/urls.py#L20), [`task/views/views_task_operation.py:8`](task/views/views_task_operation.py#L8)

#### 停止任务
- **URL**: `/api/v1/task/<str:task_id>/stop`
- **方法**: POST
- **描述**: 停止任务
- **代码位置**: [`task/urls.py:21`](task/urls.py#L21), [`task/views/views_task_operation.py:9`](task/views/views_task_operation.py#L9)

#### 恢复任务
- **URL**: `/api/v1/task/<str:task_id>/resume`
- **方法**: POST
- **描述**: 恢复任务
- **代码位置**: [`task/urls.py:22`](task/urls.py#L22), [`task/views/views_task_operation.py:10`](task/views/views_task_operation.py#L10)

#### 重启任务
- **URL**: `/api/v1/task/<str:task_id>/restart`
- **方法**: POST
- **描述**: 重启任务
- **代码位置**: [`task/urls.py:24`](task/urls.py#L24), [`task/views/views_task_operation.py:11`](task/views/views_task_operation.py#L11)

### 9.7 设置任务优先级
- **URL**: `/api/v1/task/<str:task_id>/priority`
- **方法**: POST
- **描述**: 设置任务优先级
- **请求参数**:
  - `priority`: 优先级值（1-100，数字越小优先级越高）
- **代码位置**: [`task/urls.py:26`](task/urls.py#L26), [`task/views/__init__.py:449`](task/views/__init__.py#L449)

### 9.8 任务实时监听
- **实时视图代码**: [`task/views/views_task_realtime.py`](task/views/views_task_realtime.py)

#### 监听新消息
- **URL**: `/api/v1/task/<str:task_id>/newly`
- **方法**: GET
- **描述**: 监听任务新消息
- **代码位置**: [`task/urls.py:28`](task/urls.py#L28), [`task/views/views_task_realtime.py:11`](task/views/views_task_realtime.py#L11)

#### Debug 模式监听
- **URL**: `/api/v1/task/<str:task_id>/newly/debug`
- **方法**: GET
- **描述**: Debug 模式监听任务消息
- **代码位置**: [`task/urls.py:29`](task/urls.py#L29), [`task/views/views_task_realtime.py:12`](task/views/views_task_realtime.py#L12)

### 9.9 搜索历史

#### 获取搜索历史
- **URL**: `/api/v1/task/search/history`
- **方法**: GET
- **描述**: 获取任务搜索历史
- **代码位置**: [`task/urls.py:16-17`](task/urls.py#L16), [`task/views/__init__.py:51`](task/views/__init__.py#L51)

#### 删除搜索历史
- **URL**: `/api/v1/task/search/history/<int:index>`
- **方法**: DELETE
- **描述**: 删除指定搜索历史
- **代码位置**: [`task/urls.py:17`](task/urls.py#L17), [`task/views/__init__.py:62`](task/views/__init__.py#L62)

### 9.10 流水线结果查询
- **URL**: `/api/v1/pipelines/results/query`
- **方法**: POST
- **描述**: 查询流水线结果
- **代码位置**: [`task/urls.py:32`](task/urls.py#L32), [`task/views/__init__.py:36`](task/views/__init__.py#L36)

### 9.11 父子流水线子任务
- **URL**: `/api/v1/pipelines/<str:parent_pipeline_id>/subtasks/<str:pipeline_id>`
- **方法**: GET
- **描述**: 获取子任务详情
- **代码位置**: [`task/urls.py:33`](task/urls.py#L33), [`task/views/views_pipelines.py`](task/views/views_pipelines.py)

### 9.12 下载流水线结果
- **URL**: `/api/v1/pipelines/<str:parent_pipeline_id>/subtasks/<str:pipeline_id>/result/download`
- **方法**: GET
- **描述**: 下载流水线结果
- **代码位置**: [`task/urls.py:34`](task/urls.py#L34), [`task/views/views_pipelines.py`](task/views/views_pipelines.py)

### 9.13 流水线评估
- **URL**: `/api/v1/pipelines/evaluate`
- **方法**: POST
- **描述**: 流水线多维度打分
- **请求参数**:
  - `scene`: 评估场景
  - `parent_pipeline_id`: 父流水线ID（可选）
  - `pipeline_id`: 流水线ID（可选）
  - `stage`: 阶段（可选）
  - `input_key`: 输入键（可选）
  - `custom_dimensions`: 自定义维度（可选）
  - `samples`: 样本数据（可选）
- **代码位置**: [`task/urls.py:39`](task/urls.py#L39), [`task/views/__init__.py:651`](task/views/__init__.py#L651)

### 9.14 回调接口

#### 更新数据回调
- **URL**: `/api/v1/private/task/update_data_callback`
- **方法**: GET
- **描述**: 后置任务系统数据更新回调
- **代码位置**: [`task/urls.py:37`](task/urls.py#L37), [`task/views/__init__.py:530`](task/views/__init__.py#L530)

#### 更新周期状态回调
- **URL**: `/api/v1/private/task/update_cycle_status_callback`
- **方法**: POST
- **描述**: 后置任务系统周期状态回调
- **代码位置**: [`task/urls.py:38`](task/urls.py#L38), [`task/views/__init__.py:577`](task/views/__init__.py#L577)

---

## 10. 流水线(Pipeline)接口

基础路径: `/api/v2/`
- **URL 配置**: [`apps/pipelines/urls.py`](apps/pipelines/urls.py)

### 10.1 任务记录统计（ViewSet）
- **URL**: `/api/v2/task_record_stat/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 任务记录统计CRUD操作
- **代码位置**: [`apps/pipelines/urls.py:14`](apps/pipelines/urls.py#L14), [`apps/pipelines/viewset/TaskRecordStat.py`](apps/pipelines/viewset/TaskRecordStat.py)

### 10.2 操作符管理（ViewSet）
- **URL**: `/api/v2/operators/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 流水线操作符CRUD操作
- **代码位置**: [`apps/pipelines/urls.py:15`](apps/pipelines/urls.py#L15), [`apps/pipelines/viewset/Operators.py`](apps/pipelines/viewset/Operators.py)

### 10.3 会话管理（ViewSet）
- **URL**: `/api/v2/conversation/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 流水线会话CRUD操作
- **代码位置**: [`apps/pipelines/urls.py:16`](apps/pipelines/urls.py#L16), [`apps/pipelines/viewset/Conversation.py`](apps/pipelines/viewset/Conversation.py)

### 10.4 创建并启动任务
- **URL**: `/api/v2/task/create_and_play`
- **方法**: POST
- **描述**: 创建并立即启动任务
- **代码位置**: [`apps/pipelines/urls.py:21`](apps/pipelines/urls.py#L21)

### 10.5 获取记录详情（简化）
- **URL**: `/api/v2/task/record_detail_simple`
- **方法**: GET
- **描述**: 获取简化的任务记录详情
- **代码位置**: [`apps/pipelines/urls.py:22`](apps/pipelines/urls.py#L22)

### 10.6 Prefect 回调
- **URL**: `/api/v2/task/prefect_callback`
- **URL**: `/api/v2/prefect/callback`
- **方法**: POST
- **描述**: Prefect 任务系统回调
- **代码位置**: [`apps/pipelines/urls.py:24-25`](apps/pipelines/urls.py#L24)

### 10.7 任务记录重试
- **URL**: `/api/v2/task/record/<str:rid>/retry`
- **方法**: POST
- **描述**: 重试任务记录
- **代码位置**: [`apps/pipelines/urls.py:27`](apps/pipelines/urls.py#L27)

### 10.8 任务记录播放
- **URL**: `/api/v2/task/record/<str:rid>/play`
- **方法**: POST
- **描述**: 播放/执行任务记录
- **代码位置**: [`apps/pipelines/urls.py:28`](apps/pipelines/urls.py#L28)

### 10.9 查询流水线结果
- **URL**: `/api/v2/pipelines/results/query`
- **方法**: POST
- **描述**: 查询流水线执行结果
- **代码位置**: [`apps/pipelines/urls.py:30`](apps/pipelines/urls.py#L30)

---

## 11. 模板(Template)接口

基础路径: `/api/v1/`
- **URL 配置**: [`template/urls.py`](template/urls.py)
- **视图代码**: [`template/views.py`](template/views.py)

### 11.1 获取模板列表/详情
- **URL**: `/api/v1/templates`
- **URL**: `/api/v1/templates/<int:config_id>`
- **方法**: GET
- **描述**: 获取模板列表或详情
- **查询参数**:
  - `keyword`: 关键词搜索
  - `page`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`template/urls.py:7-8`](template/urls.py#L7), [`template/views.py:105`](template/views.py#L105)

### 11.2 创建模板
- **URL**: `/api/v1/templates`
- **方法**: POST
- **描述**: 创建新模板
- **请求参数**:
  - `name`: 模板名称
  - `description`: 描述
  - `pipeline_config_a`: Pipeline配置A
  - `pipeline_config_v`: Pipeline配置V
- **代码位置**: [`template/urls.py:7`](template/urls.py#L7), [`template/views.py:122`](template/views.py#L122)

### 11.3 更新模板
- **URL**: `/api/v1/templates/<int:config_id>`
- **方法**: PUT
- **描述**: 更新模板信息
- **代码位置**: [`template/urls.py:8`](template/urls.py#L8), [`template/views.py:137`](template/views.py#L137)

### 11.4 删除模板
- **URL**: `/api/v1/templates/<int:config_id>`
- **方法**: DELETE
- **描述**: 删除模板
- **代码位置**: [`template/urls.py:8`](template/urls.py#L8), [`template/views.py:152`](template/views.py#L152)

### 11.5 搜索历史

#### 获取搜索历史
- **URL**: `/api/v1/templates/search/history`
- **方法**: GET
- **描述**: 获取模板搜索历史
- **代码位置**: [`template/views.py:32`](template/views.py#L32)

#### 删除搜索历史
- **URL**: `/api/v1/templates/search/history/<int:index>`
- **方法**: DELETE
- **描述**: 删除指定搜索历史
- **代码位置**: [`template/views.py:43`](template/views.py#L43)

---

## 12. 组织(Organization)接口

基础路径: `/api/v1/`
- **URL 配置**: [`organization/urls.py`](organization/urls.py)
- **视图代码**: [`organization/views.py`](organization/views.py)

### 12.1 创建组织
- **URL**: `/api/v1/organization/create`
- **方法**: POST
- **描述**: 创建新组织
- **请求参数**:
  - `title`: 组织名称
  - `contact_info`: 联系信息（可选）
- **代码位置**: [`organization/urls.py:6`](organization/urls.py#L6), [`organization/views.py:52`](organization/views.py#L52)

### 12.2 获取组织列表
- **URL**: `/api/v1/organization/list`
- **方法**: GET
- **描述**: 获取组织列表
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `search`: 搜索关键词
  - `created_by`: 创建者筛选
- **代码位置**: [`organization/urls.py:7`](organization/urls.py#L7), [`organization/views.py:220`](organization/views.py#L220)

### 12.3 获取我的组织
- **URL**: `/api/v1/organization/my`
- **方法**: GET
- **描述**: 获取当前用户创建的组织
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`organization/urls.py:8`](organization/urls.py#L8), [`organization/views.py:266`](organization/views.py#L266)

### 12.4 获取组织详情
- **URL**: `/api/v1/organization/<str:org_id>`
- **方法**: GET
- **描述**: 获取指定组织详情
- **代码位置**: [`organization/urls.py:9`](organization/urls.py#L9), [`organization/views.py:92`](organization/views.py#L92)

### 12.5 更新组织
- **URL**: `/api/v1/organization/<str:org_id>/update`
- **方法**: PUT
- **描述**: 更新组织信息
- **代码位置**: [`organization/urls.py:10`](organization/urls.py#L10), [`organization/views.py:121`](organization/views.py#L121)

### 12.6 删除组织
- **URL**: `/api/v1/organization/<str:org_id>/delete`
- **方法**: DELETE
- **描述**: 删除组织
- **代码位置**: [`organization/urls.py:11`](organization/urls.py#L11), [`organization/views.py:175`](organization/views.py#L175)

### 12.7 重新生成组织令牌
- **URL**: `/api/v1/organization/<str:org_id>/regenerate-token`
- **方法**: POST
- **描述**: 重新生成组织访问令牌
- **代码位置**: [`organization/urls.py:12`](organization/urls.py#L12), [`organization/views.py:309`](organization/views.py#L309)

### 12.8 组织成员管理

#### 获取成员列表
- **URL**: `/api/v1/organization/<str:org_id>/members`
- **方法**: GET
- **描述**: 获取组织成员列表
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`organization/urls.py:15`](organization/urls.py#L15), [`organization/views.py:458`](organization/views.py#L458)

#### 添加成员
- **URL**: `/api/v1/organization/<str:org_id>/members/add`
- **方法**: POST
- **描述**: 添加成员到组织
- **请求参数**:
  - `user_id`: 用户ID
- **代码位置**: [`organization/urls.py:16`](organization/urls.py#L16), [`organization/views.py:356`](organization/views.py#L356)

#### 移除成员
- **URL**: `/api/v1/organization/<str:org_id>/members/remove`
- **方法**: DELETE
- **描述**: 从组织移除成员
- **请求参数**:
  - `user_id`: 用户ID
- **代码位置**: [`organization/urls.py:17`](organization/urls.py#L17), [`organization/views.py:408`](organization/views.py#L408)

---

## 13. 系统配置(System Config)接口

### 13.1 V1 版本接口

基础路径: `/api/v1/`
- **URL 配置**: [`systemconfig/urls.py`](systemconfig/urls.py)
- **视图代码**: [`systemconfig/views.py`](systemconfig/views.py)

#### 获取系统配置
- **URL**: `/api/v1/system-config`
- **URL**: `/api/v1/system-config/<str:config_id>`
- **方法**: GET
- **描述**: 获取系统配置列表或详情
- **代码位置**: [`systemconfig/urls.py:8-10`](systemconfig/urls.py#L8)

#### 创建系统配置
- **URL**: `/api/v1/system-config`
- **方法**: POST
- **描述**: 创建系统配置
- **代码位置**: [`systemconfig/urls.py:9`](systemconfig/urls.py#L9)

#### 更新系统配置
- **URL**: `/api/v1/system-config/<str:config_id>`
- **方法**: PUT
- **描述**: 更新系统配置
- **代码位置**: [`systemconfig/urls.py:10`](systemconfig/urls.py#L10)

#### 搜索系统配置
- **URL**: `/api/v1/system-config/search`
- **方法**: GET
- **描述**: 搜索系统配置
- **代码位置**: [`systemconfig/urls.py:8`](systemconfig/urls.py#L8)

### 13.2 V2 版本接口（ViewSet）

基础路径: `/api/v2/`
- **URL 配置**: [`apps/system/urls.py`](apps/system/urls.py)
- **ViewSet 代码**: [`apps/system/viewset/`](apps/system/viewset/)

#### 系统配置管理
- **URL**: `/api/v2/system-config/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 系统配置CRUD操作
- **代码位置**: [`apps/system/urls.py:8`](apps/system/urls.py#L8), [`apps/system/viewset/SystemConfigViewSet.py`](apps/system/viewset/SystemConfigViewSet.py)

#### 外部服务管理
- **URL**: `/api/v2/external-service/`
- **方法**: GET, POST, PUT, DELETE
- **描述**: 外部服务配置CRUD操作
- **代码位置**: [`apps/system/urls.py:9`](apps/system/urls.py#L9), [`apps/system/viewset/ExternalSystemViewSet.py`](apps/system/viewset/ExternalSystemViewSet.py)

---

## 14. OpenAPI 接口

基础路径: `/api/v1/`
- **URL 配置**: [`openapi/urls.py`](openapi/urls.py)
- **视图代码**: [`openapi/views.py`](openapi/views.py)

### 14.1 API Key 管理

#### 获取 API Key 列表
- **URL**: `/api/v1/openapi/apikey`
- **方法**: GET
- **描述**: 获取用户的 API Key 列表
- **查询参数**:
  - `page_size`: 每页数量
  - `page_num`: 页码
  - `is_all`: 是否获取全部
  - `is_used`: 是否已使用
- **代码位置**: [`openapi/urls.py:8`](openapi/urls.py#L8), [`openapi/views.py:39`](openapi/views.py#L39)

#### 创建 API Key
- **URL**: `/api/v1/openapi/apikey`
- **方法**: POST
- **描述**: 创建新的 API Key
- **限制**: 每个用户最多 100 个 Key
- **代码位置**: [`openapi/urls.py:8`](openapi/urls.py#L8), [`openapi/views.py:49`](openapi/views.py#L49)

#### 更新 API Key
- **URL**: `/api/v1/openapi/apikey/<int:openapi_id>`
- **方法**: PUT
- **描述**: 更新 API Key 信息
- **代码位置**: [`openapi/urls.py:9`](openapi/urls.py#L9), [`openapi/views.py:60`](openapi/views.py#L60)

#### 删除 API Key
- **URL**: `/api/v1/openapi/apikey/<int:openapi_id>`
- **方法**: DELETE
- **描述**: 删除 API Key
- **代码位置**: [`openapi/urls.py:9`](openapi/urls.py#L9), [`openapi/views.py:72`](openapi/views.py#L72)

### 14.2 使用情况统计
- **URL**: `/api/v1/openapi/apikey/usage/chat`
- **方法**: GET
- **描述**: 获取聊天功能使用情况
- **代码位置**: [`openapi/urls.py:11`](openapi/urls.py#L11), [`openapi/views.py:167`](openapi/views.py#L167)

### 14.3 从模板创建 Dataflow 任务
- **URL**: `/api/v1/openapi/v1/dataflow/tasks/create-from-template`
- **方法**: POST
- **描述**: 通过签名从模板创建任务
- **查询参数**:
  - `signature`: Base64 编码的签名数据
- **代码位置**: [`openapi/urls.py:12`](openapi/urls.py#L12), [`openapi/views.py:82`](openapi/views.py#L82)

### 14.4 安全 API Key 管理

基础路径: `/api/v1/openapi/`
- **URL 配置**: [`openapi/urls_secure.py`](openapi/urls_secure.py)
- **视图代码**: [`openapi/views_secure.py`](openapi/views_secure.py)

#### 获取安全 API Key 列表
- **URL**: `/api/v1/openapi/keys/secure`
- **方法**: GET
- **描述**: 获取安全 API Key 列表
- **代码位置**: [`openapi/urls_secure.py:11`](openapi/urls_secure.py)

#### 创建安全 API Key
- **URL**: `/api/v1/openapi/keys/secure`
- **方法**: POST
- **描述**: 创建安全 API Key
- **代码位置**: [`openapi/urls_secure.py:11`](openapi/urls_secure.py)

#### 获取安全 API Key 详情
- **URL**: `/api/v1/openapi/keys/secure/<str:api_key_id>`
- **方法**: GET
- **描述**: 获取指定安全 API Key 详情
- **代码位置**: [`openapi/urls_secure.py:12`](openapi/urls_secure.py#L12)

#### 更新安全 API Key
- **URL**: `/api/v1/openapi/keys/secure/<str:api_key_id>`
- **方法**: PUT
- **描述**: 更新安全 API Key
- **代码位置**: [`openapi/urls_secure.py:13`](openapi/urls_secure.py#L13)

#### 删除安全 API Key
- **URL**: `/api/v1/openapi/keys/secure/<str:api_key_id>`
- **方法**: DELETE
- **描述**: 删除安全 API Key
- **代码位置**: [`openapi/urls_secure.py:14`](openapi/urls_secure.py#L14)

#### 轮换 API Key
- **URL**: `/api/v1/openapi/keys/secure/<str:api_key_id>/rotate`
- **方法**: POST
- **描述**: 轮换 API Key
- **代码位置**: [`openapi/urls_secure.py:17`](openapi/urls_secure.py#L17)

#### 获取使用日志
- **URL**: `/api/v1/openapi/keys/secure/<str:api_key_id>/logs`
- **方法**: GET
- **描述**: 获取 API Key 使用日志
- **代码位置**: [`openapi/urls_secure.py:18`](openapi/urls_secure.py#L18)

#### 获取统计数据
- **URL**: `/api/v1/openapi/keys/secure/stats`
- **方法**: GET
- **描述**: 获取 API Key 使用统计
- **代码位置**: [`openapi/urls_secure.py:21`](openapi/urls_secure.py#L21)

#### 验证 API Key 强度
- **URL**: `/api/v1/openapi/keys/secure/validate`
- **方法**: POST
- **描述**: 验证 API Key 强度
- **代码位置**: [`openapi/urls_secure.py:22`](openapi/urls_secure.py#L22)

#### 批量删除
- **URL**: `/api/v1/openapi/keys/secure/bulk-delete`
- **方法**: POST
- **描述**: 批量删除 API Key
- **代码位置**: [`openapi/urls_secure.py:25`](openapi/urls_secure.py#L25)

---

## 15. 管理员接口

基础路径: `/api/admin/`
- **URL 配置**: [`customadmin/urls.py`](customadmin/urls.py)
- **视图代码**: [`customadmin/views.py`](customadmin/views.py)

### 15.1 智能体管理

#### 获取智能体详情
- **URL**: `/api/admin/agents/<str:agent_id>`
- **方法**: GET
- **描述**: 获取智能体详情（管理员权限）
- **代码位置**: [`customadmin/urls.py:8`](customadmin/urls.py#L8), [`customadmin/views.py:88`](customadmin/views.py#L88)

#### 删除智能体
- **URL**: `/api/admin/agents/<str:agent_id>`
- **方法**: DELETE
- **描述**: 删除任意智能体（管理员权限）
- **代码位置**: [`customadmin/urls.py:8`](customadmin/urls.py#L8), [`customadmin/views.py:96`](customadmin/views.py#L96)

### 15.2 智能体发布管理

#### 获取发布列表
- **URL**: `/api/admin/agents/publish`
- **方法**: GET
- **描述**: 获取已发布智能体列表
- **代码位置**: [`customadmin/urls.py:7`](customadmin/urls.py#L7), [`customadmin/views.py:110`](customadmin/views.py#L110)

#### 发布智能体
- **URL**: `/api/admin/agents/<str:agent_id>/publish`
- **方法**: POST
- **描述**: 发布智能体到公开市场
- **代码位置**: [`customadmin/urls.py:9`](customadmin/urls.py#L9), [`customadmin/views.py:124`](customadmin/views.py#L124)

#### 取消发布
- **URL**: `/api/admin/agents/<str:agent_id>/publish`
- **方法**: DELETE
- **描述**: 取消智能体发布
- **代码位置**: [`customadmin/urls.py:9`](customadmin/urls.py#L9), [`customadmin/views.py:138`](customadmin/views.py#L138)

#### 更新发布顺序
- **URL**: `/api/admin/agents/publish`
- **方法**: PUT
- **描述**: 更新智能体发布排序
- **代码位置**: [`customadmin/urls.py:7`](customadmin/urls.py#L7), [`customadmin/views.py:115`](customadmin/views.py#L115)

### 15.3 知识库管理

#### 获取知识库详情
- **URL**: `/api/admin/kb/<str:kb_id>`
- **方法**: GET
- **描述**: 获取知识库详情（管理员权限）
- **代码位置**: [`customadmin/urls.py:11`](customadmin/urls.py#L11), [`customadmin/views.py:151`](customadmin/views.py#L151)

### 15.4 知识库发布管理

#### 获取发布列表
- **URL**: `/api/admin/kb/publish`
- **方法**: GET
- **描述**: 获取已发布知识库列表
- **代码位置**: [`customadmin/urls.py:10`](customadmin/urls.py#L10), [`customadmin/views.py:172`](customadmin/views.py#L172)

#### 发布知识库
- **URL**: `/api/admin/kb/<str:kb_id>/publish`
- **方法**: POST
- **描述**: 发布知识库到公开市场
- **代码位置**: [`customadmin/urls.py:12`](customadmin/urls.py#L12), [`customadmin/views.py:186`](customadmin/views.py#L186)

#### 取消发布
- **URL**: `/api/admin/kb/<str:kb_id>/publish`
- **方法**: DELETE
- **描述**: 取消知识库发布
- **代码位置**: [`customadmin/urls.py:12`](customadmin/urls.py#L12), [`customadmin/views.py:200`](customadmin/views.py#L200)

#### 更新发布顺序
- **URL**: `/api/admin/kb/publish`
- **方法**: PUT
- **描述**: 更新知识库发布排序
- **代码位置**: [`customadmin/urls.py:10`](customadmin/urls.py#L10), [`customadmin/views.py:177`](customadmin/views.py#L177)

### 15.5 用户权限管理

#### 设置超级用户
- **URL**: `/api/admin/superuser/<str:user_id>`
- **URL**: `/api/admin/superuser/<str:user_id>/<int:is_superuser>`
- **方法**: PUT
- **描述**: 设置/取消超级用户权限
- **代码位置**: [`customadmin/urls.py:14-15`](customadmin/urls.py#L14), [`customadmin/views.py:47`](customadmin/views.py#L47)

#### 设置管理员
- **URL**: `/api/admin/adminuser/<str:user_id>`
- **URL**: `/api/admin/adminuser/<str:user_id>/<int:is_admin>`
- **方法**: PUT
- **描述**: 设置/取消管理员权限
- **代码位置**: [`customadmin/urls.py:17-18`](customadmin/urls.py#L17), [`customadmin/views.py:59`](customadmin/views.py#L59)

#### 设置用户激活状态
- **URL**: `/api/admin/userpermission/<str:user_id>/<int:is_active>`
- **方法**: PUT
- **描述**: 激活/禁用用户账号
- **代码位置**: [`customadmin/urls.py:19`](customadmin/urls.py#L19), [`customadmin/views.py:73`](customadmin/views.py#L73)

### 15.6 用户列表
- **URL**: `/api/admin/users`
- **方法**: GET
- **描述**: 获取用户列表
- **查询参数**:
  - `keyword`: 搜索关键词
  - `page_size`: 每页数量
  - `page_num`: 页码
- **代码位置**: [`customadmin/urls.py:20`](customadmin/urls.py#L20), [`customadmin/views.py:211`](customadmin/views.py#L211)

### 15.7 全局配置
- **URL**: `/api/admin/config`
- **方法**: GET, POST
- **描述**: 获取/设置全局配置
- **代码位置**: [`customadmin/urls.py:22`](customadmin/urls.py#L22), [`customadmin/views.py:228`](customadmin/views.py#L228)

---

## 16. 会话(Conversation)接口

基础路径: `/api/v1/`
- **URL 配置**: [`df_conversation/urls.py`](df_conversation/urls.py)
- **视图代码**: [`df_conversation/views.py`](df_conversation/views.py)

### 16.1 创建会话
- **URL**: `/api/v1/df-conversation/create`
- **方法**: POST
- **描述**: 创建新会话
- **请求参数**:
  - `title`: 会话标题（可选）
  - `dataset_id`: 数据集ID（可选）
- **代码位置**: [`df_conversation/urls.py:21`](df_conversation/urls.py#L21)

### 16.2 获取会话列表
- **URL**: `/api/v1/df-conversation/list`
- **方法**: GET
- **描述**: 获取用户的所有会话
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
- **代码位置**: [`df_conversation/urls.py:24`](df_conversation/urls.py#L24)

### 16.3 获取会话详情/删除会话
- **URL**: `/api/v1/df-conversation/<uuid:conversation_id>`
- **方法**: GET, DELETE
- **描述**: 获取会话详情或删除会话
- **代码位置**: [`df_conversation/urls.py:27`](df_conversation/urls.py#L27)

---

## 17. 第三方接口

基础路径: `/api/v1/`
- **URL 配置**: [`third_party/urls.py`](third_party/urls.py)
- **视图代码**: [`third_party/views_kps.py`](third_party/views_kps.py)

### 17.1 KPS 接口

#### 查询数据集
- **URL**: `/api/v1/third-party/kps/query-dataset`
- **方法**: GET/POST
- **描述**: 查询 KPS 数据集
- **代码位置**: [`third_party/urls.py:28`](third_party/urls.py#L28)

#### 回调接口
- **URL**: `/api/v1/third-party/kps/callback`
- **方法**: POST
- **描述**: KPS 回调处理
- **代码位置**: [`third_party/urls.py:29`](third_party/urls.py#L29)

#### 额外导入
- **URL**: `/api/v1/third-party/kps/import`
- **方法**: POST
- **描述**: KPS 额外数据导入
- **代码位置**: [`third_party/urls.py:30`](third_party/urls.py#L30)

### 17.2 测试接口
- **URL**: `/api/v1/third-party/test`
- **方法**: GET
- **描述**: 第三方测试接口
- **代码位置**: [`third_party/urls.py:31`](third_party/urls.py#L31)

---

## 18. LLM 聊天接口

基础路径: `/llm_chat/`
- **URL 配置**: [`llm_chat/urls.py`](llm_chat/urls.py)
- **视图代码**: [`llm_chat/views.py`](llm_chat/views.py)

### 18.1 聊天完成
- **URL**: `/llm_chat/v1/chat/completions`
- **方法**: POST
- **描述**: LLM 聊天完成接口（代理转发）
- **请求参数**: 兼容 OpenAI API 格式
- **代码位置**: [`llm_chat/urls.py:5`](llm_chat/urls.py#L5)

---

## 【不完善】19. 训练(Train)接口

基础路径: `/api/v1/`
- **URL 配置**: [`train/urls.py`](train/urls.py)
- **视图代码**: [`train/views.py`](train/views.py)

### 19.1 训练服务代理
- **URL**: `/api/v1/train/`
- **URL**: `/api/v1/train/<path:path>`
- **方法**: ALL
- **描述**: 训练服务代理转发
- **代码位置**: [`train/urls.py:7-8`](train/urls.py#L7)

---

## 20. HF 数据集接口 (LocalFS)

基础路径: `/api/hf/`
- **URL 配置**: [`backend/dataset/hf_urls.py`](backend/dataset/hf_urls.py)
- **服务代码**: [`backend/dataset/services.py`](backend/dataset/services.py)
- **视图代码**: [`backend/dataset/hf_views.py`](backend/dataset/hf_views.py)

提供兼容 Hugging Face Hub 和 Datasets Server (Viewer) 的本地文件系统接口。

### 20.1 Hub 接口 (数据集管理)

#### 列出数据集
- **URL**: `/api/hf/api/datasets`
- **方法**: GET
- **描述**: 获取本地所有数据集列表。支持 `search` 和 `limit` 参数。

#### 获取数据集元数据
- **URL**: `/api/hf/api/datasets/<path:repo_id>`
- **方法**: GET/HEAD
- **描述**: 获取指定数据集的详细信息及文件列表（siblings）。同时兼容 `/tree/`, `/paths-info/` 等 Git 探查接口。

#### 下载/预览文件 (Resolve)
- **URL**: `/api/hf/datasets/<path:repo_id>/resolve/<str:revision>/<path:path>`
- **方法**: GET/HEAD
- **描述**: 下载或流式读取数据集中的特定文件。

#### 创建数据集仓库
- **URL**: `/api/hf/api/repos/create`
- **方法**: POST
- **描述**: 在本地创建一个新的数据集目录。
- **请求参数**: `{"name": "namespace/repo_name"}`

#### 删除数据集仓库
- **URL**: `/api/hf/api/datasets/<path:repo_id>`
- **方法**: DELETE
- **描述**: 删除本地数据集目录及其所有内容。

#### 上传文件
- **URL**: `/api/hf/api/datasets/<path:repo_id>/upload/<str:revision>/<path:path>`
- **方法**: POST
- **描述**: 上传并持久化文件到数据集的特定路径。

### 20.2 Viewer 接口 (数据探查)

#### 检查可用性
- **URL**: `/api/hf/is-valid`
- **方法**: GET
- **描述**: 检查数据集是否支持预览和查看。
- **参数**: `dataset=<repo_id>`

#### 获取 Split 列表
- **URL**: `/api/hf/splits`
- **方法**: GET
- **描述**: 列出数据集包含的所有 Split（如 train, test）。
- **参数**: `dataset=<repo_id>`

#### 获取数据行 (Rows)
- **URL**: `/api/hf/rows` 或 `/api/hf/first-rows`
- **方法**: GET
- **描述**: 分页读取数据集内容。支持 JSONL, JSON, CSV, Parquet。
- **参数**:
  - `dataset=<repo_id>`
  - `split=<split_name>` (默认 train)
  - `offset=<int>` (默认 0)
  - `length=<int>` (默认 100)

#### 获取数据集信息 (Info)
- **URL**: `/api/hf/info`
- **方法**: GET
- **描述**: 获取数据集结构信息，包含自动推断的列类型（dtypes）。
- **参数**: `dataset=<repo_id>`

---

## 核心配置

### 主 URL 配置
- **文件位置**: [`core/urls.py`](core/urls.py#L1)
- **描述**: 所有 API 路由的主入口配置

### 主要模块 URL 映射

| 模块 | URL 前缀 | URL 配置文件 |
|------|----------|-------------|
| User | `/api/v1/` | [`user/urls.py`](user/urls.py) |
| Agent | `/api/v1/` | [`agent/urls.py`](agent/urls.py) |
| Chat | `/api/v1/` | [`chat/urls.py`](chat/urls.py) |
| Collection | `/api/v1/` | [`collection/urls.py`](collection/urls.py) |
| Knowledge Base | `/api/v1/` | [`knowledgebase/urls.py`](knowledgebase/urls.py) |
| Document | `/api/v1/` | [`document/urls.py`](document/urls.py) |
| Dataset V1 | `/api/v1/` | [`apps/dataset/urls_v1.py`](apps/dataset/urls_v1.py) |
| Dataset V2 | `/api/v2/` | [`apps/dataset/urls.py`](apps/dataset/urls.py) |
| HF Datasets | `/api/hf/` | [`backend/dataset/hf_urls.py`](backend/dataset/hf_urls.py) |
| Task | `/api/v1/` | [`task/urls.py`](task/urls.py) |
| Pipeline | `/api/v2/` | [`apps/pipelines/urls.py`](apps/pipelines/urls.py) |
| Template | `/api/v1/` | [`template/urls.py`](template/urls.py) |
| Organization | `/api/v1/` | [`organization/urls.py`](organization/urls.py) |
| System Config V1 | `/api/v1/` | [`systemconfig/urls.py`](systemconfig/urls.py) |
| System Config V2 | `/api/v2/` | [`apps/system/urls.py`](apps/system/urls.py) |
| OpenAPI | `/api/v1/` | [`openapi/urls.py`](openapi/urls.py) |
| Custom Admin | `/api/admin/` | [`customadmin/urls.py`](customadmin/urls.py) |
| Conversation | `/api/v1/` | [`df_conversation/urls.py`](df_conversation/urls.py) |
| Third Party | `/api/v1/` | [`third_party/urls.py`](third_party/urls.py) |
| LLM Chat | `/llm_chat/` | [`llm_chat/urls.py`](llm_chat/urls.py) |
| Train | `/api/v1/` | [`train/urls.py`](train/urls.py) |

---

## 认证说明

### JWT Token 认证

大多数 API 接口需要 JWT Token 认证。在请求头中添加：

```
Authorization: Bearer <your_jwt_token>
```

### 权限等级

1. **普通用户**: 只能访问自己的资源
2. **管理员(is_staff)**: 可以访问大部分管理接口
3. **超级用户(is_superuser)**: 拥有所有权限

---

## 响应格式

### 成功响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

### 错误响应

```json
{
  "code": 100001,
  "msg": "错误信息",
  "data": {}
}
```

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 100000 | 通用错误 |
| 100001 | 参数错误/验证失败 |
| 100002 | 资源不存在 |
| 100003 | 无权限 |
| 510888 | 任务操作错误 |
| 150001 | API Key 数量限制 |
| 190001 | 参数错误：资源不存在 |

---

## 分页说明

列表接口默认支持分页，返回格式：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "total_pages": 10
  }
}
```

---

## 流式响应

聊天接口使用 SSE (Server-Sent Events) 流式响应：

```
data: {"content_type": "on_message", "content": "Hello"}

data: {"content_type": "on_message", "content": " World"}

data: {"content_type": "on_complete"}
```

---

*文档生成时间: 2026-03-13*
*版本: v1.2*
