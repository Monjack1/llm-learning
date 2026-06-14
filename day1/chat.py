import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个简洁的编程助手。"},
        {"role": "user", "content": "Python 怎么定义函数？"},
        {"role": "assistant", "content": "用 def 关键字，例如 def f(): ..."},  # 上一轮模型的回答
        {"role": "user", "content": "那它怎么返回值？"}
       
    ],
)

print(response.choices[0].message.content)