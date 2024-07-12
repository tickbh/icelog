from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, or_, select

from iceslog import models
from iceslog.api.deps import (
    CurrentUser,
    PageNumType,
    PageSizeType,
    SessionDep,
    get_current_active_superuser,
)
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash, verify_password
from iceslog.models import (
    RetMsg,
)
from iceslog.models.base import OptionType
from iceslog.models.dictmap import DictMap, DictMapItem, MsgDictItemsPublic, MsgEditDictMap, OneDictItem, OneEditDictMap
from iceslog.models.perms import GroupPerms, GroupPermsBase, GroupPermsPublic, OnePerm, Perms, PermsPublic
from iceslog.models.syslog import LogsPublic, SysLog
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition

router = APIRouter()


@router.get("/page", response_model=LogsPublic)
def get_logs(session: SessionDep, keywords: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    condition = []
    if keywords:
        condition.append(or_(SysLog.content.like(f"%{keywords}%"), SysLog.module==keywords))
    select(SysLog).order_by()
    logs, count = page_view_condition(session, condition, SysLog, pageNum, pageSize, [col(SysLog.create_time).desc()])
    return LogsPublic(list=logs, total=count)
