import os
from typing import Any

from fastapi import APIRouter, HTTPException
from iceslog.core.config import settings
from iceslog.core.db import engine, init_db
from sqlmodel import Session, select

from iceslog.models import User
from iceslog.models.user import UserPublic
from iceslog.core.security import get_password_hash
router = APIRouter()

@router.get("/")
def read_items() -> Any:
    return {"Hello": "World", "name": os.getenv("PROJECT_NAME"), "pass": get_password_hash("123456")}

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