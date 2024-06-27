import time
from typing import Union

from fastapi import FastAPI, Request

from app.api.main import api_router
app = FastAPI()

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/a")
# def read_root(request: Request):
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

app.include_router(api_router, prefix="/v1")