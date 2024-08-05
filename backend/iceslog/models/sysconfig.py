from datetime import datetime
from typing import Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now
from iceslog.models.base import RetMsg

# Database model, database table inferred from class name

class SysConfigBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False, description="类型名称")
    key: str = Field(max_length=255, nullable=False, unique=True, description="键值")
    value: str = Field(max_length=255, nullable=False, unique=True, description="键值")
    status: int = Field(default=1, description="状态(1:正常;0:禁用)")
    sort: int = Field(default=1, description="排序")
    remark: str = Field(max_length=255, nullable=True, default="", description="备注")
    
class SysConfig(SysConfigBase, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    update_time: datetime = Field(nullable=False, default_factory=datetime_now, description="更新时间")
    is_deleted: int = Field(default=0, description="是否删除(1-删除，0-未删除)")
    
    
class PageSysConfig(SQLModel):
    list: list[SysConfig]
    total: int