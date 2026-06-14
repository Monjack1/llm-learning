import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    )


def ask(temperature,max_tokens =None):
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [
            {"role": "user", "content": "用两句话描写一下夏天的傍晚。"},
        ],
        temperature=temperature,
        max_tokens = max_tokens,
    )
    return response.choices[0].message.content


# 实验一：temperature=0，跑两次，看是否几乎相同
print("===== temperature=0，第一次 =====")
print(ask(0))
print("===== temperature=0，第二次 =====")
print(ask(0))

# 实验二：temperature=1.5，跑两次，看差异有多大
print("\n===== temperature=1.5，第一次 =====")
print(ask(1.5))
print("===== temperature=1.5，第二次 =====")
print(ask(1.5))

# 实验三：max_tokens=20，观察话说一半被截断
print("\n===== max_tokens=20（会被截断）=====")
print(ask(0.7, max_tokens=20))