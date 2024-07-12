from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Union
from fastapi import Request
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now
from iceslog.utils import http_utils


class SysLogBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    module: str = Field(max_length=20, nullable=False, description="日志模块")
    content: str = Field(max_length=10240, nullable=False, description="日志内容")
    request_uri: str = Field(
        max_length=255, nullable=False, description="请求路径")
    ip: str = Field(max_length=255, nullable=True,
                    default="", description="请求IP")
    province: str = Field(max_length=255, nullable=True,
                          default="", description="省份")
    city: str = Field(max_length=255, nullable=True,
                      default="", description="城市")
    execution_time: int = Field(nullable=True, default=0, description="执行时间ms")
    browser: str = Field(max_length=255, nullable=True,
                         default="", description="浏览器")
    browser_version: str = Field(
        max_length=255, nullable=True, default="", description="浏览器版本")
    os: str = Field(max_length=255, nullable=True,
                    default="", description="终端系统")
    create_by: int = Field(nullable=True, default=0, description="创建人ID")
    create_time: datetime = Field(
        nullable=False, default_factory=datetime_now, description="创建时间")


class SysLog(SysLogBase, table=True):
    pass

def do_record_log(request: Request, module: str, content: str, execution_time: int = 0, create_by: int = 0):
    from iceslog.core.db import get_db
    session = next(get_db())
    log = SysLog(module=module, content=content,
                 request_uri=str(request.url), ip=http_utils.get_client_ip(request), province="", city="",
                 execution_time=execution_time, create_by=create_by, browser=http_utils.get_browser(request))
    session.add(log)
    session.commit()


class LogsPublic(SQLModel):
    list: list[SysLogBase]
    total: int