# 阶段一详细计划：AI 应用开发（6.12 – 7.12）

> 目标：4.5 周内从"会 Python"到"能独立交付一个企业级 RAG 系统"，并产出简历核心项目①。
> 每天按 6–8 小时有效学习设计。每天的结构都是：**学习目标 → 具体任务 → 资源 → 验收标准**。验收标准是关键——达不到就别往下走，宁可砍后面的可选内容。

---

## Week 1（6.12 周五 – 6.18 周四）：LLM API + FastAPI 工程基础

### Day 1（6.12）：环境搭建 + 第一次调用大模型
**目标**：开发环境就绪，成功调用一次 LLM API。
**任务**
1. 安装 uv（现代 Python 包管理器，比 pip/conda 更快，`pip install uv` 即可）；用 `uv init` 建项目、`uv add openai` 装依赖，理解 pyproject.toml 是什么（项目的"配置说明书"：一个写在项目根目录的文本文件，声明项目名、Python 版本要求和依赖了哪些库，相当于 Node.js 的 package.json；有了它别人拿到你的项目一条命令就能装齐环境，是现代 Python 项目的标准做法，替代了老式的 requirements.txt）
2. 配置 API key 到环境变量（你已经拿到 key 了，这步是安全地把它接入代码）：① `uv add python-dotenv`；② 在项目根目录建 `.env` 文件，写入 `DEEPSEEK_API_KEY=sk-你的key`（等号两边无空格、key 不加引号）；③ **在 `.gitignore` 里加一行 `.env`**（最关键，防止 key 被推到 GitHub 盗刷，用 `git status` 确认看不到 .env 才算成功）；④ 代码里用 `from dotenv import load_dotenv; load_dotenv()` 加载，再用 `os.getenv("DEEPSEEK_API_KEY")` 读取。**永远不要把 key 写进代码**
3. 用 openai SDK 发出第一个请求：理解 `base_url` 为什么能指向 DeepSeek（OpenAI 兼容协议）、messages 里 system/user/assistant 三种角色的作用
4. 实验参数：改 temperature（0 vs 1.5）观察输出差异、设 max_tokens 观察截断
5. 配好 Git：建 GitHub 仓库 `llm-learning`，今天的代码提交上去，写好 .gitignore（排除 .env）

**资源**：DeepSeek 开放平台文档「首次调用 API」；uv 官方文档 Getting Started
**验收**：能不看文档写出一个带 system prompt 的多轮对话脚本（用 list 维护历史，循环输入）。

### Day 2（6.13）：流式输出 + function calling
**目标**：掌握 LLM 应用最核心的两个 API 能力。
**任务**
1. 流式输出：`stream=True`，遍历 chunk 拼接 delta.content，做一个终端里逐字打印的对话脚本；理解为什么所有 ChatGPT 类产品都是流式的（首字延迟体验）
2. function calling：定义一个 `get_weather(city)` 工具的 JSON Schema → 发请求 → 解析返回的 tool_calls → 本地执行函数 → 把结果作为 tool 角色消息回传 → 拿到最终回答。**完整闭环必须自己手写一遍**，这是 Week 3 Agent 的原理基础
3. 加分实验：让模型一次返回多个工具调用；故意让工具报错，把错误信息回传看模型如何处理

**资源**：DeepSeek 文档「Function Calling」章节；OpenAI 官方 Function calling guide（结构讲得最清楚）
**验收**：能画出 function calling 的完整时序图（用户→模型→本地函数→模型→用户），并解释每步传的 messages 长什么样。

### Day 3（6.14）：FastAPI 入门——路由与 Pydantic
**目标**：跑通 FastAPI 基础，理解它为什么是 AI 后端首选。
**任务**
1. FastAPI 官方教程从头走：路径参数、查询参数、请求体；启动 `fastapi dev`，玩熟 /docs 自动生成的交互文档（Swagger UI）
2. Pydantic 重点学：BaseModel 定义请求/响应模型、字段校验（Field 约束）、嵌套模型；理解"类型即校验"的思想——这也是 LangChain 结构化输出的基础
3. 写练习接口：`POST /v1/echo` 接收 `{messages: [...]}` 结构（模仿 OpenAI 格式），校验角色只能是 system/user/assistant

**资源**：FastAPI 官方文档中文版 Tutorial 前半（到 Request Body 部分）；Pydantic 官方文档 Models 章节
**验收**：传入非法字段时接口能自动返回 422 和清晰错误信息，并且你能解释这是 Pydantic 在哪一层做的。

### Day 4（6.15）：FastAPI 进阶——异步、依赖注入、中间件
**目标**：理解 async 在 IO 密集型 LLM 服务中的意义。
**任务**
1. async/await 补课（半天）：协程 vs 线程、事件循环直觉、什么时候用 `async def`（IO 等待时）什么时候用 `def`（CPU 计算时 FastAPI 会丢线程池）；用 httpx 异步并发调 3 次 LLM API，对比串行耗时
2. 依赖注入 Depends：写一个校验请求头 API key 的依赖，挂到接口上
3. 中间件：写一个记录每次请求耗时的日志中间件
4. 错误处理：自定义异常 + exception_handler，统一错误响应格式

**资源**：FastAPI 文档 Concurrency and async/await（这篇把异步讲得极好，必读）、Dependencies、Middleware 章节
**验收**：能向别人解释"为什么 FastAPI 适合做 LLM 网关"（答案关键词：IO 密集、异步并发、等待上游 API 时不阻塞）。

### Day 5（6.16）：SSE 流式接口——本周核心难点
**目标**：把 Day 2 的流式输出搬到 HTTP 接口上。
**任务**
1. 学 SSE（Server-Sent Events）协议：`text/event-stream`、`data:` 行格式，和 WebSocket 的区别（单向 vs 双向，LLM 场景 SSE 足够）
2. 用 FastAPI 的 StreamingResponse + async generator 实现：接口收到 messages → 流式调用 LLM → 逐 chunk 以 SSE 格式吐给客户端
3. 写一个简单客户端验证（httpx stream 或直接 curl -N）
4. 处理细节:客户端断开时如何停止上游调用（节省 token 费用）

**资源**：FastAPI 文档 Custom Response → StreamingResponse；MDN 的 Server-sent events 介绍
**验收**：curl 你的接口能看到逐字输出，且格式与 OpenAI API 的 SSE 格式一致（`data: {...}\n\n`，结尾 `data: [DONE]`）。

### Day 6（6.17）：Docker + pytest
**目标**：学会打包和测试，这是"工程素养"在简历上的体现。
**任务**
1. Docker 半天速成:镜像/容器/Dockerfile 三个概念；为你的 FastAPI 项目写 Dockerfile（基于 python:3.12-slim，多阶段构建可选），`docker build` + `docker run -p` 跑起来；学会 `docker logs`、`docker exec` 调试
2. pytest 半天：用 FastAPI 的 TestClient 给你的接口写 5–8 个测试（正常路径 + 非法输入 + 鉴权失败）；理解 fixture 的基本用法
3. 学会 mock：测试时不真调 LLM API（monkeypatch 或 respx 拦截 httpx 请求）

**资源**：Docker 官方 Get Started Part 1–3；FastAPI 文档 Testing 章节
**验收**：`docker build && docker run` 一条龙能跑通服务；`pytest` 全绿且不消耗任何 API 费用。

### Day 7（6.18）：Week 1 产出——流式对话后端 v1
**目标**：整合本周所有内容，完成项目①的骨架。
**任务**：从零搭一个干净的项目（这会成为项目①的仓库）：
- `POST /v1/chat/completions`：兼容 OpenAI 格式，支持流式与非流式
- 多轮对话：用内存 dict 按 session_id 存历史（后续可换 Redis，先不引入）
- API key 鉴权依赖、请求日志中间件、统一错误处理
- Dockerfile + pytest 测试 + README（写清楚怎么跑、接口示例）
- 提交 GitHub，commit 信息规范（feat:/fix:/docs:）

**验收**：发给一个朋友 README，对方能在 10 分钟内用 Docker 跑起来并对话成功。

---

## Week 2（6.19 – 6.25）：RAG 原理 + 向量数据库

### Day 8（6.19）：Embedding——一切检索的基础
**目标**：直觉 + 实操层面理解文本向量化。
**任务**
1. 概念：embedding 是什么（语义→高维向量）、余弦相似度 vs 点积 vs 欧氏距离、为什么归一化后余弦≈点积
2. 实操：用 sentence-transformers 加载 **BGE-M3**（中文场景事实标准），对 20 个句子算向量，计算相似度矩阵，验证"语义近的句子分数高"；试一组反例（字面像但语义不同 vs 字面不同但语义同）
3. 了解维度概念：BGE-M3 是 1024 维；维度高低的 trade-off
4. 了解 API 型 embedding（OpenAI text-embedding-3 系列）与本地模型的选型差异（成本/隐私/效果）

**资源**：Hugging Face 上 BAAI/bge-m3 的 model card；sentence-transformers 官方 Quickstart
**验收**：能解释"为什么 RAG 不直接用关键词搜索"并举一个 embedding 检索赢、一个关键词检索赢的例子（这是面试题：为什么还需要混合检索）。

### Day 9（6.20）：文档解析与切分（chunking）
**目标**：掌握 RAG 效果差异最大的环节——数据预处理。
**任务**
1. 文档解析：用 pypdf/pdfplumber 解析 PDF、python-docx 解析 Word、直接读 Markdown；体会 PDF 解析的脏（表格错乱、页眉页脚混入），了解 MinerU/marker 这类专业解析工具的存在
2. 切分策略逐个实现并对比：固定长度切分（最笨）→ 递归字符切分（按 \n\n→\n→句号 递归，LangChain 的 RecursiveCharacterTextSplitter 思想，**自己先手写再看库**）→ 按 Markdown 标题的结构化切分
3. 理解关键参数:chunk_size（中文建议先试 256–512 字）、chunk_overlap 的作用（防止语义被切断）
4. 元数据设计：每个 chunk 要带 source 文件名、标题路径、页码——这是后面"带引用回答"的基础

**资源**：LangChain 文档 Text Splitters 概念页；Pinecone 的 chunking strategies 博客（经典文章，搜 "pinecone chunking strategies"）
**验收**：拿一份真实 PDF（比如某模型的技术报告），用两种策略切分，肉眼对比哪种的 chunk 更"自包含"，并能说出为什么。

### Day 10（6.21）：手写最小 RAG——不许用框架
**目标**：白盒理解 RAG 全流程，这天的代码是面试底气。
**任务**：只用 openai SDK + sentence-transformers + numpy（或 faiss），手写完整 pipeline：
1. 加载并切分一份文档（用 Day 9 的代码）
2. 全部 chunk 算 embedding，存进 numpy 数组（或 FAISS IndexFlatIP）
3. 用户提问 → 问题向量化 → top-k 相似度检索
4. 把检索到的 chunk 拼进 prompt 模板（"根据以下资料回答…资料：{chunks} 问题：{query}"）→ 调 LLM 生成
5. 实验：问一个文档里没有的问题，观察模型是否乱编 → 在 prompt 里加"资料中没有则说不知道"约束，对比效果（这就是幻觉缓解的最朴素手段）

**资源**：不需要新资源，就用你已有的积木。卡住时可参考 LangChain 的 "RAG from scratch" 系列第 1–4 讲思路（B 站有搬运）
**验收**：整个 RAG 在一个 150 行以内的 Python 文件里，每一行你都能解释。把它单独开个仓库或目录，README 写"RAG from scratch, no framework"。

### Day 11–12（6.22 – 6.23）：Milvus——生产级向量库
**目标**：从玩具检索升级到生产组件，覆盖招聘里"向量库使用"要求。
**任务**
Day 11：
1. 概念：为什么需要专门的向量数据库（百万级向量时暴力检索太慢）；ANN 近似检索思想
2. 索引类型直觉：FLAT（精确）、IVF_FLAT（聚类分桶）、**HNSW**（图索引，主流默认）——各自的精度/速度/内存 trade-off，面试常问
3. 实操：pip 装 pymilvus，用 **Milvus Lite**（本地文件模式，零部署）建 collection、定义 schema（id/向量/文本/元数据）、插入 Day 10 的数据、向量检索 + 元数据过滤（如只检索某个文件的内容）

Day 12：
4. 混合检索：理解 dense（语义）+ sparse（BM25 字面）各自的强项；用 BGE-M3 同时输出 dense 和 sparse 向量，在 Milvus 里做 hybrid search + RRF 融合排序
5. 用 docker compose 起一个完整版 Milvus standalone，把数据迁过去（为项目①做准备），用 Attu（官方 GUI）看看里面的数据

**资源**：Milvus 官方文档中文版（milvus.io/docs/zh）：Quickstart → Hybrid Search 章节；BGE-M3 model card 里的 hybrid 用法示例
**验收**：能回答"HNSW 和 IVF 的区别""什么 query 类型下 BM25 比向量检索好"（答案示例：专有名词、型号、代码标识符）。

### Day 13（6.24）：Rerank 与检索增强技巧
**目标**：掌握把 RAG 从"能用"提到"好用"的关键手段。
**任务**
1. Rerank：理解 bi-encoder（检索用，快）vs cross-encoder（重排用，准）的结构差异——这是高频面试题；实操用 **BGE-reranker-v2-m3** 对粗排 top-20 重排取 top-5，构造几个 case 对比重排前后的命中质量
2. Query 改写：用 LLM 把口语化/指代不清的问题改写成检索友好的问题（多轮对话里的"它呢？"必须结合历史改写）
3. 了解即可（各 30 分钟）：HyDE（先让 LLM 生成假设答案再去检索）、父子块检索（小块检索、大块送 LLM）、多路召回
4. 把 rerank 和 query 改写接入你 Day 10–12 的 pipeline

**资源**：BAAI/bge-reranker-v2-m3 model card；LangChain "RAG from scratch" 系列的 query translation 部分
**验收**：能讲清"为什么不直接用 cross-encoder 检索全库"（答案：要和每个文档拼接算一遍，O(n) 次模型前向，太慢）。

### Day 14（6.25）：RAG 评估（RAGAS）+ 本周复盘
**目标**：建立"用指标说话"的习惯——这是你项目区别于大路货的核心。
**任务**
1. 学 RAGAS 四个核心指标的含义和计算思想：faithfulness（答案是否忠于检索内容）、answer relevancy（答案是否切题）、context precision / context recall（检索质量）
2. 构建一个 20 条的小测试集（问题 + 标准答案 + 来源），对你本周的 pipeline 跑一次 RAGAS 评估，记下基线分数
3. 做一次对照实验：关掉 rerank 再跑一次，对比指标差异——把结果记进 README 的表格里
4. 复盘：把本周内容画成一张 RAG 架构图（手画拍照或 draw.io），存进仓库

**资源**：RAGAS 官方文档（docs.ragas.io）Get Started + Metrics 章节
**验收**：README 里有一张"优化项 vs 指标变化"的表格，哪怕只有两行。

---

## Week 3（6.26 – 7.2）：LangChain / LangGraph + Agent

### Day 15（6.26）：LangChain 核心抽象
**目标**：把你手写过的东西映射到框架抽象上（这个顺序让你不会被框架魔法迷惑）。
**任务**
1. 核心概念：ChatModel、PromptTemplate、OutputParser、**Runnable 与 LCEL**（`prompt | model | parser` 管道语法）、流式 `.stream()` 与异步 `.ainvoke()`
2. 结构化输出：`with_structured_output(PydanticModel)`——让 LLM 稳定吐 JSON，工程里极常用
3. 用 LCEL 重写你 Day 10 的手写 RAG：Milvus 接 VectorStore 接口 → as_retriever() → 组装链。对比手写版，明确框架帮你省了什么、隐藏了什么
4. 注意：LangChain 版本迭代快，**以官方最新文档为准**，遇到网上教程和文档冲突一律信文档

**资源**：LangChain 官方文档（python.langchain.com）Tutorials 的 Basics 部分 + RAG tutorial
**验收**：同一个 RAG 你现在有手写版和 LangChain 版，能各用三句话说出对方的优劣。

### Day 16–17（6.27 – 6.28）：LangGraph——重头戏
**目标**：掌握当前 Agent 编排的主流框架，项目①的编排层就用它。
**任务**
Day 16：
1. 核心概念：StateGraph、State（TypedDict + reducer）、节点（函数）、边与条件边、START/END；理解它和 LCEL 链的本质区别（图可以循环，链不能——Agent 需要循环）
2. 官方 Quickstart 走完：搭一个最简单的 chatbot 图，加上 checkpointer（MemorySaver）实现多轮记忆，理解 thread_id 概念

Day 17：
3. 工具调用循环：bind_tools + ToolNode + tools_condition，搭出经典 ReAct 循环（模型决定调工具→执行→结果回喂→直到给出答案），对照 Day 2 你手写的 function calling 闭环——本质一样，LangGraph 帮你管理了循环和状态
4. 条件路由实战：搭一个"先判断问题类型→闲聊直接答 / 知识问题走 RAG"的分支图
5. human-in-the-loop：interrupt 机制了解 + 跑一个官方示例（概念知道即可）

**资源**：LangGraph 官方文档 Quickstart + Concepts；LangChain Academy 的 "Introduction to LangGraph" 免费课程（academy.langchain.com，质量很高，挑 Module 1–2 看）
**验收**：能不看文档画出 ReAct Agent 的状态图（节点、条件边），并搭建出来跑通。

### Day 18（6.29）：Agent 进阶 + MCP
**目标**：补齐 Agent 生态认知，覆盖招聘新热词。
**任务**
1. 给你的 Agent 接 3 个真实工具：网络搜索（Tavily 免费额度）、计算器、你 Week 2 的 Milvus 检索——一个能查资料、能算数、能搜本地知识库的多工具 Agent
2. MCP（Model Context Protocol）：理解它解决什么问题（工具接入的标准化协议，类比"AI 的 USB-C"）；用官方 Python SDK 跑一个最小 MCP server（暴露一个工具）+ client 调用
3. 了解概念：multi-agent 模式（supervisor/swarm）、Agent 的失败模式（死循环、工具滥用）和应对（max iterations、工具结果截断）

**资源**：MCP 官方文档（modelcontextprotocol.io）Quickstart；LangGraph 文档 Agent 架构概念页
**验收**：你的多工具 Agent 对"帮我查一下今天 LA 天气，再算 23*47，再从我的文档里找 XX"这种复合问题能正确分步调用三个工具。

### Day 19（6.30）：LlamaIndex 半天 + LangSmith 半天
**任务**
1. 上午 LlamaIndex：过官方 Quickstart，重点理解它的定位差异——以"数据接入与索引"为中心（Document/Node/Index 抽象，内置大量 loader 和 index 结构），而 LangChain 以"编排"为中心；跑一个它的 5 行 RAG demo。目的：面试被问"两者区别"时有一手体验
2. 下午 LangSmith（或开源替代 Langfuse）：给你的 LangGraph 应用接上 tracing，看每一步的 prompt/耗时/token 消耗——调试 Agent 没有 tracing 寸步难行，这也是工程亮点
**资源**：LlamaIndex 官方 Starter Tutorial；LangSmith 文档 Quickstart（免费个人额度够用）
**验收**：能用自己的话说清两个框架的选型场景；能在 trace 界面里指出 Agent 某次回答检索了哪些 chunk。

### Day 20–21（7.1 – 7.2）：Week 3 整合产出 + 缓冲
**任务**
1. 产出一个完整小项目：**多工具研究助手 Agent**（LangGraph 编排：query 分析 → 按需调用 搜索/RAG/计算 → 汇总带引用的回答），FastAPI 包成 SSE 流式接口（复用 Week 1 骨架），接 LangSmith tracing，写 README 推 GitHub
2. 缓冲半天：补前三周欠的账（每个人卡的点不同，正常）
3. 半天做项目①的方案设计：画架构图、定 API 契约、列功能清单和里程碑——Day 22 开工就不迷茫

**验收**：架构图能回答三个问题——数据怎么进来、一次提问经过哪些节点、引用来源怎么传回前端。

---

## Week 4–4.5（7.3 – 7.12）：项目①——企业级 RAG 知识库问答系统

> 10 天工期。前 6 天功能开发，后 4 天评估优化与交付。每天结束必须 commit。

### Day 22–23（7.3 – 7.4）：数据入库 pipeline
- 文档上传接口（PDF/Word/Markdown）→ 解析 → 递归切分（带标题路径元数据）→ BGE-M3 算 dense+sparse 向量 → 写入 Milvus
- 知识库管理：文档列表、删除文档（按元数据删 chunk）、重复上传去重（文件 hash）
- 注意：解析和向量化耗时,用 FastAPI 的 BackgroundTasks 异步处理,接口先返回任务受理

### Day 24–25（7.5 – 7.6）：检索链路
- 混合检索（dense + sparse + RRF 融合）→ BGE-reranker 重排 → top-k 输出
- 多轮场景的 query 改写节点（结合对话历史消解指代）
- 单独留一个 `POST /v1/retrieve` 调试接口，直接看检索结果——评估阶段会反复用

### Day 26–27（7.7 – 7.8）：LangGraph 编排 + 接口与前端
- 图结构：query 改写 → 检索 → 相关性自检（检索结果与问题不相关则改写重试一次或直接说不知道）→ 生成（强约束：基于资料回答 + 标注引用编号）
- 引用溯源：响应里返回每条引用的原文片段、文件名、页码
- FastAPI SSE 流式接口（复用 Week 1 骨架与鉴权/日志）；Streamlit 或 Gradio 糊一个界面：上传文档、对话、侧栏显示引用来源
- 接 LangSmith tracing

### Day 28–29（7.9 – 7.10）：评估驱动优化（项目灵魂）
- 构建 50–100 条评估集：拿 3–5 份真实文档（建议用几篇中文技术报告或某领域的公开规章），人工+LLM 辅助出题
- RAGAS 跑基线 → 做 3 组对照实验并记录指标表：
  1. 纯向量检索 vs 混合检索
  2. 有无 rerank
  3. chunk_size 两档对比（如 256 vs 512）
- 根据结果定最终配置，把实验表写进 README——**这两天的产出决定你面试时能聊 5 分钟还是 30 分钟**

### Day 30（7.11）：部署与交付
- docker-compose.yml 一键起全套（FastAPI + Milvus + 前端），环境变量模板 .env.example
- README 终稿：架构图、快速开始（10 分钟内可跑）、API 文档、评估实验表、效果截图/GIF
- 自测：换一台环境（或删掉本地镜像）从零按 README 跑一遍

### Day 31（7.12）：阶段复盘 + 简历落笔
- 把项目①写成简历条目（2–4 行，按"做了什么→技术→量化结果"）
- 自问自答 10 个面试题并写下答案：为什么混合检索、rerank 原理、chunk 怎么选、幻觉怎么缓解、faithfulness 怎么算、Agent 死循环怎么防、SSE vs WebSocket、async 为什么适合这场景、Milvus 索引选型、如果文档量到千万级怎么办
- 预习阶段二：把 Karpathy 的《Let's build GPT》加进收藏夹

---

## 本阶段时间分配原则
- 每天最后 30 分钟写学习日志（学了什么/卡在哪/明天补什么），就记在仓库的 LOG.md 里——这本身就是面试谈资
- 卡住超过 1 小时：先问 LLM、再搜 GitHub issues，还不行就标记跳过，周内缓冲时段回补
- 可砍内容（进度落后时）：Day 18 的 MCP 实操（保留概念）、Day 19 的 LlamaIndex（压缩到 1 小时）、项目①的前端（用 Swagger UI 演示也行）
- 不可砍：Day 10 手写 RAG、Day 16–17 LangGraph、Day 28–29 评估实验
