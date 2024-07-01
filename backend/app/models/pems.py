from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column


class Perms(SQLModel):
    id = Field(primary_key=True,  verbose_name="ID")
    name: str = Field(max_length=50, null=False, verbose_name="名字")
    route: str = Field(max_length=255, null=False,
                       unique=True, verbose_name="路由")
    codename: str = Field(max_length=50, null=False, verbose_name="代码名字")
    sort: int = Field(null=False, default=0, verbose_name="排序")
    create_time: datetime | None = Field(default=None, description="创建时间")


class GroupPerms(SQLModel):
    id = Field(primary_key=True, verbose_name="ID")
    name: str = Field(max_length=50, null=False, verbose_name="名字")
    permissions: JSON = Field(
        max_length=10240, null=False, default="[]", verbose_name="拥有权限数,如[1, 2, 3, 4, 5]")
    create_time: datetime | None = Field(default=None, description="创建时间")
