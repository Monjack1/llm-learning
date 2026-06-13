## 2026-06-12 Day 1

学了：
- uv 建项目、pyproject.toml 是干嘛的
- 环境变量管理 API key（.env + python-dotenv + .gitignore）
- 第一次调通 DeepSeek API，理解了 base_url 和 system/user/assistant 三种角色
- temperature 实验：temp=0 可复现，temp=1.5 发散；max_tokens 是硬截断不是精简

踩的坑：
- 401 报错，原来是把 cmbUnionPay 那串订单号当成 key 了，去 API keys 页面重建才对
- key 一旦贴到聊天里就要立刻删掉重建

明天（Day 2）：流式输出 + function calling