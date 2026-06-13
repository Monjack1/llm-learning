import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key= os.getenv("DEEPSEEK_API_KEY"),
    base_url= "https://api.deepseek.com",
)

def ask(temperature=None,max_tokens=None):
    messages = []
    temperature = int(input("Please set the temperature"))
    while True:

        question = input("Please enter your question :")
        if question == "clear":
            messages = []
            print("cleared")
            continue
        elif question =="quit":
            print("OK")
            break

        messages.append({"role":"user","content":question})
        response = client.chat.completions.create(
            model = "deepseek-chat",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        ) 
        answer = response.choices[0].message.content
        usage = response.usage.completion_tokens
        print(answer)
        print("tokens used:",usage)
        messages.append(
            {"role":"assistant","content":answer}
        )

ask()
             
            

    