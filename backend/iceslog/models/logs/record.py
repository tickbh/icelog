from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel, Column
from iceslog.models.base import PageModel

from iceslog.core.db import datetime_now

class LogFreqBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    module: str = Field(max_length=255, nullable=False, description="记录模块")
    log_time: int = Field(nullable=False, description="归属时间戳")
    times: int = Field(nullable=False, description="请求次数")
    
class LogFreq(LogFreqBase, table=True):
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")

    __table_args__ = (
        UniqueConstraint("module", "log_time"),
    )
    
class RecordLog(SQLModel):
    create: datetime = None
    lv: int
    tid: str
    uid: int
    msg: str
    sys: str = None
    exid: str = None
    extra: str = None

class RecordLogPublices(SQLModel):
    list: list[RecordLog]
    total: int
    
'''
创建sql, clickhouse
CREATE TABLE log_record (
	lv Int8,
	tid String,
	uid UInt64,
	msg String,
    sys String,
	exid String,
	extra String DEFAULT '{}',
	create DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(create)
ORDER BY (create, uid)
TTL create + toIntervalDay(5);
'''
    
class OneLogVisit(SQLModel):
    module: str
    log_date: datetime
    times: int
    
class LogVisitInfos(SQLModel):
    dates: list[datetime]
    times: list[int]
    module: str
    
class LogPageSearch(PageModel):
    read: int
    project: str = "default"
    msg: str = None
    sys: str = None
    uid: str = None
    lv: int = None
    startTime: str = None
    endTime: str = None
    
    def params(self) -> dict:
        return {
            "msg": self.msg,
            "sys": self.sys,
            "lv": self.lv,
            "uid": self.uid,
            "exid": self.uid,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "offset": (self.pageNum.real - 1) * self.pageSize.real,
            "limit": self.pageSize.real,
        }
    
    def get_offset(self):
        return (self.pageNum.real - 1) * self.pageSize.real
    
    def get_limit(self):
        return self.pageSize.real