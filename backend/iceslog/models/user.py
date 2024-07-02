from datetime import datetime
from pydantic import ConfigDict, EmailStr
from sqlalchemy import SMALLINT, BigInteger, DateTime, Integer, SmallInteger, func
from sqlmodel import Field, Relationship, SQLModel, Column

MIN_PASSWORD = 8
MAX_PASSWORD = 64

# Shared properties


class UserBase(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    account: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    gender: int | None = Column(SmallInteger,
        default=None, comment="性别(1-男，2-女 0-未知)", doc="aaaaaaaaaaaaaa")
    telephone: str | None = Field(
        default=None, max_length=15, unique=True, nullable=True, description="电话号码")
    user_type: str = Field(default=None, max_length=15,
                           description="用户类型, sys管理员")
    avatar: str | None = Field(
        default=None, max_length=255, description="用户头像")
    mobile: str | None = Field(
        default=None, max_length=255, description="联系方式")
    create_time: datetime = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    create_by: int | None = Field(default=None, description="创建人id")
    update_time: datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    update_by: int | None = Field(default=None, description="更新人id")
    is_deleted: int = Column(Integer, default=0, comment="逻辑删除标记")
    group_pem: int | None = Field(default=None, description="组权限id")


class UserCreate(UserBase):
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
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
    id: int | None = Field(default=None, primary_key=True)
    real_name: str | None = Field(
        default=None, max_length=255, description="实际名称")
    hashed_password: str

# Properties to return via API, id is always required


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(
        default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: int | None = Field(
        default=None, foreign_key="user.id", nullable=False)

# Properties to return via API, id is always required


class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
