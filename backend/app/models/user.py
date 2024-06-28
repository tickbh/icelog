from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

MIN_PASSWORD = 8
MAX_PASSWORD = 64

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    telephone: str | None = Field(default=None, max_length=15, unique=True, nullable=True, description="电话号码")
    user_type: str = Field(default=None, max_length=15, description="用户类型, sys管理员")
    avatar: str | None = Field(default=None, max_length=255, description="用户头像")

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)
    new_password: str = Field(min_length=MIN_PASSWORD, max_length=MAX_PASSWORD)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    real_name: str | None = Field(default=None, max_length=255, description="实际名称")
    hashed_password: str

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int