

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
