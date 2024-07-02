import time
from typing import Union

from fastapi import FastAPI, Request
from iceslog.core.config import settings

from iceslog.api.main import api_router
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time * 1000:.2f}ms"
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)