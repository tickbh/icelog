from datetime import datetime
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, DateTime, func
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now

class Perms(SQLModel, table=True):
    id: int = Field(primary_key=True, description="id值")
    name: str = Field(max_length=50, nullable=False, description="名字")
    route: str = Field(max_length=255, nullable=False, description="路由")
    codename: str = Field(max_length=50, nullable=False, description="代码名字")
    is_show: bool = Field(default=True, description="是否展示")
    sort: int = Field(nullable=False, default=0, description="排序")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")

class GroupPerms(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int = Field(primary_key=True, description="ID")
    name: str = Field(max_length=50, nullable=False, description="名字")
    permissions: str = Field(max_length=10240, nullable=False, default="", description="拥有权限数,如 1, 2, 3, 4, 5")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")

class OnePerm(Perms):
    groups: str = None