from datetime import datetime, timezone
from pydantic import ConfigDict, EmailStr
from sqlalchemy import SMALLINT, BigInteger, DateTime, Integer, SmallInteger, func
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now
from iceslog.models.base import RetMsg

MIN_PASSWORD = 6
MAX_PASSWORD = 64

# Shared properties

class UserBase(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: EmailStr | None = Field(default=None, nullable=True, index=True, max_length=255)
    username: str = Field(unique=True, max_length=255)
    nickname: str | None = Field(default=None, nullable=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    gender: int | None = Field(sa_column=SmallInteger,
        default=0, description="性别(1-男，2-女 0-未知)")
    telephone: str | None = Field(
        default=None, max_length=15, unique=True, nullable=True, description="电话号码")
    user_type: str = Field(default=None, max_length=15,
                           description="用户类型, sys管理员")
    avatar: str | None = Field(
        default=None, max_length=255, description="用户头像")
    mobile: str | None = Field(
        default=None, max_length=255, description="联系方式")
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")
    create_by: int | None = Field(default=None, description="创建人id")
    # onupdate=func.now(), 
    update_time: datetime = Field(nullable=False, default_factory=datetime_now, description="更新时间")
    update_by: int | None = Field(default=None, description="更新人id")
    is_deleted: int = Field(default=0, description="逻辑删除标记")
    group_pem: int | None = Field(default=None, description="组权限id")


class UserCreate(UserBase):
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserRegister(SQLModel):
    username: EmailStr = Field(max_length=255)
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(
        default=None, max_length=255)  # type: ignore
    password: str | None = Field(
        default=None, min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(
        min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)
    new_password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    userId: int | None = Field(default=None, primary_key=True)
    real_name: str | None = Field(
        default=None, max_length=255, description="实际名称")
    hashed_password: str

# Properties to return via API, id is always required


class UserPublic(UserBase):
    userId: int

class MsgUserPublic(RetMsg):
    data: UserPublic

class UsersPublic(SQLModel):
    list: list[UserPublic]
    total: int

class MsgUsersPublic(RetMsg):
    data: UsersPublic
    
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
