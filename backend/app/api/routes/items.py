from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def read_items() -> Any:
    return {"Hello": "World"}

@router.get("/a")
def read_items() -> Any:
    return {"Hello": "World"}
