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

from iceslog.models.logs.store import LogsStore, LogsStoreBase, LogsStoreCreate, LogsStorePublices, LogsStoreUpdateUrl
from iceslog.models.perms import GroupPerms, GroupPermsBase, GroupPermsPublic, OnePerm, Perms, PermsPublic
from iceslog.models.syslog import LogsPublic, SysLog
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition

router = APIRouter(
    dependencies=[Depends(check_has_perm)])

@router.get("/page", response_model=LogsStorePublices)
def get_logs_store(session: SessionDep, keywords: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    condition = []
    if keywords:
        condition.append(or_(LogsStore.name.like(f"%{keywords}%"), LogsStore.store.like(f"%{keywords}%")))
    logs, count = page_view_condition(session, condition, LogsStore, pageNum, pageSize, [col(LogsStore.sort).desc()])
    return LogsStorePublices(list=logs, total=count)

@router.post(
    "/create", response_model=LogsStoreBase
)
def create_user(*, session: SessionDep, store_in: LogsStoreCreate) -> Any:
    """
    Create new user.
    """
    store = LogsStore.model_validate(store_in)
    session.add(store)
    session.commit()
    session.refresh(store)
    return store


@router.get(
    "/form", 
    response_model=LogsStoreBase
)
def read_store_form(*, session: SessionDep, store_id: int) -> Any:
    
    store = session.get(LogsStore, store_id)
    if not store:
        return RetMsg("00001", "账号不存在")
    
    return store

@router.patch(
    "/url/{store_id}", 
    response_model=LogsStoreBase
)
def set_store_connect_url(*, session: SessionDep, store_id: int, body: LogsStoreUpdateUrl) -> Any:
    store = session.get(LogsStore, store_id)
    if not store:
        return RetMsg("00001", "账号不存在")
    store.connect_url = body.connect_url
    session.merge(store)
    session.commit()
    return store


@router.put(
    "/{store_id}",
    response_model=LogsStoreBase,
)
def update_store(
    *,
    session: SessionDep,
    store_id: int,
    user_in: LogsStoreBase,
) -> Any:
    """
    Update a user.
    """

    store = session.get(LogsStore, store_id)
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
    store_ids = base_utils.split_to_int_list(stores, ",")
    for store_id in store_ids:
        store = session.get(LogsStore, store_id)
        if not store:
            raise HTTPException(status_code=404, detail="未找到存储配置")
        session.delete(store)
        session.commit()
    return RetMsg(msg="User deleted successfully")
