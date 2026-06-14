import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime   # 文件顶部加这个 import

def get_time(city):
    # 简单起见先不管时区，直接返回当前时间
    return f"{city}现在的时间是 {datetime.now().strftime('%H:%M')}"
load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def get_weather(city):
    if city == "火星":   # 故意制造一个查不到的情况
        return "查询失败：该城市不存在或暂无天气数据"
    return f"{city}今天晴，气温25度"

# ② 工具定义（上面那段 tools，复制过来）
tools  = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type":"function",
        "function": {
            "name":"get_time",
            "description":"查询某个城市的时间",
            "parameters": {
                "type":"object",
                "properties": {
                    "city": {
                        "type":"string",
                        "description":"城市名称，例如：北京",
                    }
                
                },
                "required":["city"]
            }
        }
    }
]  # ← 填进去

# ③ 第一趟：把用户问题 + tools 发给模型
messages = [{"role": "user", "content": "火星今天天气怎么样？"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,        # ← 把工具清单告诉模型
)

# ④ 取出模型的回复（这条 assistant 消息里带着 tool_calls）
assistant_message = response.choices[0].message

# 关键：把这条 assistant 消息 append 进 messages（包含它的调用意图）
messages.append(assistant_message)

if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
    
        if func_name == "get_weather":
            result = get_weather(func_args["city"])
        
        elif func_name == "get_time":
            result = get_time(func_args["city"])

        messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":result,
        })
    final_response = client.chat.completions.create(
        
        model="deepseek-chat",
        messages=messages,
    )

    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
