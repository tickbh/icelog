import time

from fastapi import FastAPI, Request
from iceslog.core.config import settings

from iceslog.api.main import api_router
import contextlib
from iceslog.middleware.cors import LogCORSMiddleware
from iceslog.utils.scheduler_utils import scheduler
from loguru import logger

# 每分钟执行的定时任务
@scheduler.scheduled_job('interval', seconds=60)
async def cron_job():
    from datetime import datetime
    # 执行任务的内容，例如打印当前时间
    logger.info(f"The current time is {datetime.now()}")
    
@contextlib.asynccontextmanager
async def lifespan(app):
    scheduler.start()

    logger.info("Run at startup!")
    yield
    logger.info("Run on shutdown!")
    scheduler.shutdown()
        
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    LogCORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_regex_paths = ["/api/v1/pub/(.*)"],
    allow_credentials = True,
)
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

# logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
logger.add("logs/iceslog_{time:YY-MM-DD_HH_mm}.log", rotation="500 MB")