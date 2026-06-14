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