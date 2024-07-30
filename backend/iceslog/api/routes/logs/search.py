from typing import Any, List

from fastapi import APIRouter, Body, Depends, Form, HTTPException
from sqlmodel import col, delete, func, or_, select

from iceslog import models
from iceslog.api.deps import (
    CurrentUser,
    PageNumType,
    PageSizeType,
    SessionDep,
    check_has_perm,
    get_current_active_superuser,
)
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash, verify_password
from iceslog.models import (
    RetMsg,
)
from iceslog.models.base import OptionType
from iceslog.models.dictmap import DictMap, DictMapItem, MsgDictItemsPublic, MsgEditDictMap, OneDictItem, OneEditDictMap

from iceslog.models.logs.read import LogsRead, LogsReadBase, LogsReadCreate, LogsReadPublices, LogsReadUpdateUrl
from iceslog.models.logs.record import RecordLogPublices, LogPageSearch
from iceslog.models.perms import GroupPerms, GroupPermsBase, GroupPermsPublic, OnePerm, Perms, PermsPublic
from iceslog.models.syslog import LogsPublic, SysLog
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition
from yarl import URL

router = APIRouter(
    dependencies=[Depends(check_has_perm)])

@router.post("/page", response_model=RecordLogPublices)
async def get_logs_store(session: SessionDep, search: LogPageSearch):
    data = session.get(LogsRead, search.read)
    if not data:
        raise HTTPException(400, "未找到相关的数据")
    
    if data.store.lower() == "clickhouse":
        from iceslog.drivers import clickhouse_utils
        logs, total = await clickhouse_utils.read_log_page(data.connect_url, data.table_name, search)
        return RecordLogPublices(list=logs, total=total)
    raise HTTPException(400, "暂不支持")

@router.post(
    "/create", response_model=LogsReadBase
)
def create_user(*, session: SessionDep, store_in: LogsReadCreate) -> Any:
    url = URL(store_in.connect_url)
    if not url or not url.scheme:
        raise HTTPException(400, "无效的url")

    store = LogsRead.model_validate(store_in)
    session.add(store)
    session.commit()
    session.refresh(store)
    return store


@router.get(
    "/form", 
    response_model=LogsReadBase
)
def read_store_form(*, session: SessionDep, id: int) -> Any:
    
    store = session.get(LogsRead, id)
    if not store:
        return RetMsg("00001", "账号不存在")
    
    return store

@router.patch(
    "/url/{id}", 
    response_model=LogsReadBase
)
def set_store_connect_url(*, session: SessionDep, id: int, body: LogsReadUpdateUrl) -> Any:
    store = session.get(LogsRead, id)
    if not store:
        return RetMsg("00001", "账号不存在")
    url = URL(body.connect_url)
    if not url or not url.scheme:
        raise HTTPException(400, "无效的url")
    store.connect_url = body.connect_url
    session.merge(store)
    session.commit()
    return store


@router.put(
    "/{id}",
    response_model=LogsReadBase,
)
def update_store(
    *,
    session: SessionDep,
    id: int,
    user_in: LogsReadBase,
) -> Any:
    """
    Update a user.
    """

    store = session.get(LogsRead, id)
    if not store:
        raise HTTPException(
            status_code=404,
            detail="当前存储方式不存在",
        )
    store.sqlmodel_update(user_in)
    session.merge(store)
    session.commit()
    return store


@router.delete("/{stores}")
def delete_user(
    session: SessionDep, stores: str
) -> RetMsg:
    """
    Delete a user.
    """
    ids = base_utils.split_to_int_list(stores, ",")
    for id in ids:
        store = session.get(LogsRead, id)
        if not store:
            raise HTTPException(status_code=404, detail="未找到存储配置")
        session.delete(store)
        session.commit()
    return RetMsg(msg="User deleted successfully")
