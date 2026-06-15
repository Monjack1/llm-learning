from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from pydantic import BaseModel
from typing import Literal
app = FastAPI()   # 创建一个应用实例，所有接口都挂在它上面


@app.get("/")     # 装饰器：把下面的函数绑定到 "GET /" 这个窗口
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/users/{user_id}")     # {user_id} 是占位符
def get_user(user_id: int):       # 类型标注 int，FastAPI 自动转换+校验
    return {"user_id": user_id}

@app.get("/search")
def search(keyword: str, limit: int = 10):   # limit 有默认值，可不传
    return {"keyword": keyword, "limit": limit}

class Message(BaseModel):
    role: Literal['system', 'assistant', 'user']    # ... 表示必填
    content: str = Field(..., min_length=1, max_length=2000)   # 长度约束


class ChatRequest(BaseModel):
    messages: List[Message]    # 一个列表，每个元素都必须符合 Message 结构
    model: str = "deepseek-chat"   # 带默认值，可选


@app.post("/chat")
def chat(msg: Message):        # 参数类型标成 Message，FastAPI 就知道这是请求体
    return {"你发的角色": msg.role, "你发的内容": msg.content}

@app.get("/health")
def get_health():
    return {"status":"ok"}

@app.post("/v1/echo")
def request(req:ChatRequest):
    last_me = req.messages[-1]
    return {"content":last_me.content}

