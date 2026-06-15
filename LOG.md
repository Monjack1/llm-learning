

## 2026-06-12 Day 1

学了：
- uv 建项目，理解 pyproject.toml / .venv / .gitignore / .env 各自作用
- 用 .env + python-dotenv + os.getenv 安全管理 API key
- 调通 DeepSeek API，理解 base_url 兼容原理、system/user/assistant 三种角色
- temperature（0 稳定 / 1.5 发散）、max_tokens 是硬截断
- 独立搭出多轮对话脚本：靠每轮把 assistant 回复 append 回 messages 实现"记忆"
- token 统计（response.usage）、Git add/commit/push 全流程

踩的坑：
- 把 cmbUnionPay 那串订单号当成 API key，401 报错，去 API keys 页面重建才对
- content 拼成 cotent，模型收不到内容
- clear 逻辑漏了 continue
- git commit 没带 -m 掉进 Vim（Esc → :q! 退出）
- commit 说明用了中文引号，终端卡在 dquote（Ctrl+C 脱身，引号要用英文半角）

明天 Day 2：流式输出 + function calling
    

## 2026-06-13 Day 2

学了：
- 流式输出（stream=True）：遍历 chunk 取 delta.content 逐字打印，理解首字延迟、为什么 LLM 产品都用流式
- 把流式接回多轮对话：循环里把每块 content 拼成 full_answer，循环后整条以 assistant 角色 append 回 messages，才能保住多轮记忆
- function calling 完整五步闭环：user 提问 → 模型返回 tool_calls（调用意图，不是执行）→ 本地代码执行函数 → 结果以 tool 角色回传 → 第二趟请求拿最终人话回答
- 拆透了 assistant_message 结构：tool_calls 是列表（可多个）、tool_call.id 用于配对、function.arguments 是 JSON 字符串需 json.loads 解析、content 在调工具时可能为空
- 多工具并行：一条 taskcalls 里可能多个调用，执行+回传必须都在 for 循环内
- 工具报错处理：失败信息也照常以 tool 角色回传，让模型翻译成对用户友好的话，而不是直接抛异常崩溃

踩的坑：
- content 又拼成 cotent —— 在 tool 消息里这次是 API 强制字段，直接报错（不再像变量名那样无害）
- "content": "result" 误加引号，变成字面文本而非变量值，模型收到的是 "result" 五个字母
- for 循环缩进错误：执行函数和回传结果跑到循环外面，单工具碰巧能跑，多工具时只处理最后一个 —— 缩进决定代码结构
- JSON Schema 里 required 缩进进了 properties 内部，应与 properties 平级（对照正确的工具逐行比缩进）
- 测"火星天气"时屏幕没输出：模型没调工具、直接文字回答，而代码只处理了调工具的情况 —— 补 else 处理"不调工具"分支

核心认知：
- 模型不执行函数，只返回"调用意图（工单）"，执行的是我的代码
- 模型本身没有实时数据，第一趟只能要工具，拿到结果第二趟才能回答
- function calling 是 Agent 的地基：Agent 就是把"开工单→执行→回传"这个循环自动化、多轮化

明天 Day 3：FastAPI 入门（路由、Pydantic）—— 开始从脚本转向后端服务

## 2026-06-14 Day 3

学了：
- 从"写脚本"转向"写后端服务"：脚本是跑一次就结束，服务是启动后一直挂着、等别人发请求来
- FastAPI 核心：用 @app.get / @app.post 装饰器把函数绑定到网络地址（路由），fastapi dev 启动服务
- 三种接收数据的方式：路径参数（/users/{id}）、查询参数（?keyword=x）、请求体（POST 的 JSON）
- /docs 自动文档（Swagger UI）：根据代码自动生成、能直接 Try it out 测接口，不用写客户端
- Pydantic「类型即校验」：用 BaseModel 声明数据该长什么样，框架自动校验，不用手写 if
- Field 约束（min_length / max_length）、Literal 限制取值范围（role 只能 system/user/assistant）、嵌套模型（ChatRequest 里套 List[Message]）
- 写了 POST /v1/echo 接口：仿 OpenAI 格式接收 messages 列表，校验 role，返回最后一条 content

搞懂的关键概念：
- 装饰器：不改函数代码，给它加"网络地址"身份；一个 @ 只管正下方的函数，但同一个装饰器能反复用在多个函数上
- FastAPI 在干什么：站在我函数门口的"门卫+翻译"——监听网络、查路由、用 Pydantic 校验、JSON↔Python对象双向转换、发回响应，这五件脏活它全包，我只写第④步业务逻辑
- 校验是"声明"出来的不是"手写"出来的：role 限制写在 Message 模型里，不在函数里。数据能进函数 = 已经合法，所以函数体很干净
- 422 在哪一层做的：Pydantic 在「请求进函数之前」校验，不合格直接返回 422，函数体根本不执行（用 print 实验亲眼验证过）

踩的坑/笔误：
- 想在 def 函数签名里手动校验 role —— 方向错了，校验该声明在模型里，是 Day 1/2 写脚本的惯性
- Literal 第一个值写成 'role'（把字段名当成值了），应是 'system'
- 访问 Pydantic 对象用点号 req.messages[-1].content，不是字典的 ["key"]

看文档的判断：
- 带"(可选)"标记、或要注册登录第三方服务（如 FastAPI Cloud 部署、entrypoint 配置）的章节，学习阶段一律跳过，不影响核心
- 文档当字典查（带着问题找答案），不当教科书从头读

明天 Day 4：FastAPI 进阶 —— 异步、依赖注入、中间件