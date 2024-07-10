from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now

# Database model, database table inferred from class name


class MenusBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    belong: str = Field(max_length=20, nullable=False, description="菜单归属")
    type: str = Field(max_length=20, nullable=False, description="菜单类型")
    name: str = Field(max_length=255, nullable=False, description="菜单名字")
    icon: str = Field(max_length=255, nullable=True, default="", description="菜单ICON")
    params: str = Field(max_length=1024, nullable=True, default="", description="菜单参数")
    component: str = Field(max_length=1024, nullable=True, default="", description="组件名称")
    pid: int = Field(default=0, description="归属ID")
    path: str = Field(max_length=1024, nullable=False, description="激活菜单名称")
    redirect: str = Field(max_length=1024, nullable=True, default="", description="菜单路由")
    sort: int = Field(nullable=True, default=0, description="菜单排序")
    is_show: bool = Field(default=True, description="是否展示")
    groups: str = Field(max_length=4096, nullable=False, default="", description="权限ids 1|2|3|4|5]")

class Menus(MenusBase, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")


class OneEditMenu(MenusBase):
    children: list[Self] | None = []

class OneLabelMenu(SQLModel):
    value: int
    label: str
    children: list[Self] | None = []

    @staticmethod
    def build_from(menu: OneEditMenu) -> Self:
        value = OneLabelMenu(value=menu.id, label=menu.name)
        for child in menu.children:
            value.children.append(OneLabelMenu.build_from(child))
        return value