import time
from typing import Union

from fastapi import FastAPI, Request
from iceslog.core.config import settings

from iceslog.api.main import api_router
import contextlib
from starlette.applications import Starlette
from iceslog.utils.scheduler_utils import scheduler
 
# 每分钟执行的定时任务
@scheduler.scheduled_job('interval', seconds=1)
async def cron_job():
    from datetime import datetime
    # 执行任务的内容，例如打印当前时间
    print(f"The current time is {datetime.now()}")
    
@contextlib.asynccontextmanager
async def lifespan(app):
    scheduler.start()

    print("Run at startup!")
    yield
    print("Run on shutdown!")
    scheduler.shutdown()
        
app = FastAPI(lifespan=lifespan)

app.celery = scheduler

# # 设置celery的代理路径与结果存储路径，此处均使用 Redis
# # 默认用户可省略：redis://:<You Passowrd>@localhost:6379/0
# celery.conf.update(broker_url=settings.REDIS_URL)  # 代理
# celery.conf.update(result_backend=settings.REDIS_URL)  # 结果存储

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time * 1000:.2f}ms"
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)

