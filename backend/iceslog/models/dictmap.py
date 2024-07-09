from datetime import datetime
from typing import Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now
from iceslog.models.base import RetMsg

# Database model, database table inferred from class name


class DictMap(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False, description="类型名称")
    code: str = Field(max_length=255, nullable=False, unique=True, description="类型编码")
    status: int = Field(default=0, description="状态(0:正常;1:禁用)")
    remark: str = Field(max_length=255, nullable=True, default="", description="备注")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    update_time: datetime = Field(nullable=False, default_factory=datetime_now, description="更新时间")
    is_deleted: int = Field(default=0, description="是否删除(1-删除，0-未删除)")
    
    
class DictMapItem(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int | None = Field(default=None, primary_key=True)
    dict_id: int | None = Field(default=None, index=True, description="字典id")
    label: str = Field(max_length=255, nullable=False, description="字典名称")
    value: str = Field(max_length=255, nullable=False, description="字典项值")
    status: int = Field(default=0, description="状态(0:正常;1:禁用)")
    sort: int = Field(default=0, description="排序")
    remark: str = Field(max_length=255, nullable=True, default="", description="备注")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    update_time: datetime = Field(nullable=False, default_factory=datetime_now, description="更新时间")
    
    
   
class OneDictItem(SQLModel):
    value: int
    label: str = ""
    
class MsgDictItemsPublic(RetMsg):
    list: list[OneDictItem]
    
class OneEditDictItem(SQLModel):
    id: Union[int, None]
    label: str
    value: str
    status: int
    sort: int
    
class OneEditDictMap(SQLModel):
    id: Union[int, None]
    name: str
    code: str
    status: int
    dictItems: list[OneEditDictItem]
    
class MsgEditDictMap(SQLModel):
    list: list[OneEditDictMap]
    total: int
    