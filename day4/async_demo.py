import asyncio
import time

async def fake_llm_call(name):
    print(f"{name} 开始调用...")
    await asyncio.sleep(2)   # 模拟等待网络2秒（await：等的时候让出控制权）
    print(f"{name} 拿到结果")
    return f"{name}的回答"

async def run_serial():
    start = time.time()
    await fake_llm_call("请求1")
    await fake_llm_call("请求2")
    await fake_llm_call("请求3")
    print(f"串行总耗时：{time.time() - start:.1f}秒\n")


async def run_concurrent():
    start = time.time()
    await asyncio.gather(
        fake_llm_call("请求A"),
        fake_llm_call("请求B"),
        fake_llm_call("请求C"),
        fake_llm_call("请求D"),
        fake_llm_call("请求E")
    )
    print(f"并发总耗时：{time.time() - start:.1f}秒\n")


async def main():
    print("===== 串行 =====")
    await run_serial()
    print("===== 并发 =====")
    await run_concurrent()


asyncio.run(main())

'''
import asyncio
import os
import time
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(   # 注意是 AsyncOpenAI，不是 OpenAI
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


async def call_llm(question):
    response = await client.chat.completions.create(   # 注意有 await
        model="deepseek-chat",
        messages=[{"role": "user", "content": question}],
    )

    return response.choices[0].message.content


async def main():
    start = time.time()
    results = await asyncio.gather(
        call_llm("用一句话介绍北京"),
        call_llm("用一句话介绍上海"),
        call_llm("用一句话介绍广州"),
    )
    for r in results:
        print(r)
    print(f"并发3次调用总耗时：{time.time() - start:.1f}秒")


asyncio.run(main())

'''






'''

import asyncio
import time 
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os 
load_dotenv()

client = AsyncOpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url= "https://api.deepseek.com",
)
async def call_llm(question):
    response = await client.chat.completions.create(
        model = "deepseek-chat",
        messages =[ {"role":"user","content":question}],
    )
    return response.choices[0].message.content




async def run_concurrent():
    start  = time.time()
    results = await asyncio.gather(
        call_llm("用一句话介绍北京"),
        call_llm("用一句话介绍上海"),
        call_llm("用一句话介绍广州"),
    )
    for ans in results:
        print(ans)
    print(f"并发三次总耗时{time.time()-start:.1f}seconds")

async def main():
    
    print("并行调用开始\n")
    await run_concurrent()

asyncio.run(main())

'''
