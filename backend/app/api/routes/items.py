import os
from typing import Any

from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.core.db import engine, init_db
from sqlmodel import Session, select

from app.models import User
from app.models.user import UserPublic
router = APIRouter()

@router.get("/")
def read_items() -> Any:
    return {"Hello": "World", "name": os.getenv("PROJECT_NAME")}

@router.get("/a")
def read_items() -> Any:
    with Session(engine) as session:
        init_db(session)
        value = session.exec(select(User)).first()
        return {"value": value}
    return {"Hello": "World", "config": settings, "aaa": settings.model_config}


@router.get("/id", response_model=list[UserPublic])
def read_items() -> Any:
    with Session(engine) as session:
        init_db(session)
        value = session.exec(select(User)).all()
        return value