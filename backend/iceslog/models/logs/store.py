from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now

class LogsStoreBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    store: str = Field(max_length=255, nullable=False, description="存储类型")
    name: str = Field(max_length=255, nullable=False, description="项目名字")
    status: int = Field(nullable=False, default=1, description="状态(1启用, 0禁用)")
    sort: int = Field(default=0, description="排序")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    
class LogsStore(LogsStoreBase, table=True):
    connect_url: str = Field(max_length=255, nullable=False, description="链接地址")
    
class LogsStorePublices(SQLModel):
    list: list[LogsStoreBase]
    total: int
    
class LogsStoreCreate(LogsStoreBase):
    connect_url: str


class LogsStoreUpdateUrl(SQLModel):
    connect_url: str
    
# class LogsStorePublic(SQLModel):
#     list: list[LogsStoreBase]
#     total: int