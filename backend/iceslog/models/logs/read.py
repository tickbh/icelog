from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now

class LogsReadBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    store: str = Field(max_length=255, nullable=False, description="存储类型")
    name: str = Field(max_length=255, nullable=False, description="项目名字")
    project: str = Field(nullable=False, default="default", description="归属项目")
    status: int = Field(nullable=False, default=1, description="状态(1启用, 0禁用)")
    sort: int = Field(default=0, description="排序")
    table_name: str = Field(max_length=255, nullable=True, default="", description="表名或者topic")
    table_ext: str = Field(max_length=255, nullable=True, default="", description="表名附加信息")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    
class LogsRead(LogsReadBase, table=True):
    connect_url: str = Field(max_length=255, nullable=False, description="链接地址")
    
class LogsReadFull(LogsReadBase):
    connect_url: str
    
class LogsReadPublices(SQLModel):
    list: list[LogsReadFull]
    total: int
    
class LogsReadCreate(LogsReadBase):
    connect_url: str


class LogsReadUpdateUrl(SQLModel):
    connect_url: str
    
# class LogsReadPublic(SQLModel):
#     list: list[LogsReadBase]
#     total: int