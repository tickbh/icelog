from datetime import datetime
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column

# Database model, database table inferred from class name


class Menus(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int | None = Field(default=None, primary_key=True)
    type: str = Field(max_length=20, nullable=False, description="菜单归属")
    name: str = Field(max_length=255, nullable=False, description="菜单名字")
    icon: str = Field(max_length=255, nullable=False, description="菜单ICON")
    params: str = Field(max_length=1024, nullable=False, description="菜单参数")
    pid: int = Field(default=0, description="归属ID")
    route: str = Field(max_length=1024, nullable=False, description="菜单路由")
    sort: int = Field(nullable=True, default=0, description="菜单排序")
    is_show: bool = Field(default=False, description="是否展示")
    # groups: JSON = Column(JSON,
    #     max_length=4096, nullable=False, default="[]", comment="权限ids [1, 2, 3, 4, 5]"
    # )
    create_time: datetime | None = Field(default=None, description="创建时间")
