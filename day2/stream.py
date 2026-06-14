from dotenv import load_dotenv
from openai import OpenAI
import os 

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url= "https://api.deepseek.com",
    )
messages = []
while True:
    full_answer = ""
    question = input("Please enter your question: ")
    if question == "quit":
        print("Byebye!")
        break
    elif question == "clear":
        messages = []
        continue
    messages.append(
        {"role":"user","content":question}
    )
    response = client.chat.completions.create(
    model= "deepseek-chat",
    messages=messages,
    stream= True)
    for chunk in response:
        content = chunk.choices[0].delta.content
        
        if content:
             print(content,end = '',flush =True)
             full_answer+=content
    messages.append(
        {"role":"assistant","content":full_answer}
    )
    print()
    
