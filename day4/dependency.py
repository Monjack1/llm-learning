from fastapi import FastAPI,Depends,Header,HTTPException,Request
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import time
app = FastAPI()
load_dotenv()

class BusinessError(Exception):
    def __init__(self,code:str,messages: str):
        self.code = code
        self.messages = messages

class RateLimitError(Exception):
    def __init__(self,code:str,messages: str):
        self.code = code
        self.messages = messages

@app.exception_handler(RateLimitError)
async def rate_limit_error_handler(request:Request,exc:RateLimitError):
    return JSONResponse(
        status_code=429,
        content={"error":{"code":exc.code,"messages":exc.messages}}
    )
@app.exception_handler(BusinessError)
async def business_error_handler(request:Request,exc:BusinessError):
    return JSONResponse(
        status_code=400,
        content={"error":{"code":exc.code,"messages":exc.messages}},

    )
@app.get("/test_error")
def test_error():
    raise BusinessError(code = "NO_DOCUMENT",messages="找不到指定文档")
@app.get("/ratelimit_test_error")
def ratelimit_test_error():
    raise RateLimitError(code = "UP_TO_RATE",messages="reach rate limit!")
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv("API_ACCESS_KEY"):
        raise HTTPException(status_code=401,detail="API key 无效或缺失")
    return x_api_key

@app.get("/protected")
def protected_route(api_key: str = Depends(verify_api_key)):
    print("🔒 依赖执行了，正在校验 key...") 
    return {"message":"你通过了验证！","your_key":api_key}

@app.middleware("http")
async def log_request_time(request:Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() -start 
    print(f"{request.method}{request.url.path}耗时 {duration:.3f}秒")
    print(response)
    return response