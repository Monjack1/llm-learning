import time
from fastapi import FastAPI,Request
import asyncio
app = FastAPI()

@app.middleware("http")
async def log_request_time(request:Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() -start 
    print(f"{request.method}{request.url.path}耗时 {duration:.3f}秒")

    return response