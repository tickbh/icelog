from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from iceslog import models
from iceslog.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash, verify_password
from iceslog.models import (
    RetMsg,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from iceslog.models.dictmap import DictMap, MsgDictItemsPublic, MsgEditDictMap, OneEditDictMap
from iceslog.models.user import MsgUserMePublic, MsgUserPublic, MsgUsersPublic, UserMePublic
from iceslog.utils import cache_utils, generate_new_account_email, send_email
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition

router = APIRouter()


dict_cache_table = CacheTable(models.DictMap, attribs=["id", "code"])
def get_dict(id):
    return dict_cache_table.get_value(id)

dict_item_cache_table = CacheTable(models.DictMapItem, attribs=["id"], groups=["dict_id"])
def get_dict_items(id):
    return dict_item_cache_table.get_group(id)


@router.get(
    "/options",
    response_model=MsgDictItemsPublic,
)
def read_options(session: SessionDep, user: CurrentUser, key: str) -> Any:
    group = get_dict(key)
    if not group:
        return
    items = get_dict_items(group["id"])
    return MsgDictItemsPublic(data=items)


@router.get(
    "/page",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def read_dicts(session: SessionDep, pageNum: int = 0, pageSize: int = 100, keywords: str = None) -> Any:
    condition = []
    if keywords:
        condition.append(DictMap.name.like(f"%{keywords}%"))

    dicts, count = page_view_condition(session, condition, DictMap, pageNum, pageSize)
    vals = []
    for val in dicts:
        items = get_dict_items(val.id)
        val = OneEditDictMap.model_validate(val, update={"dictItems": get_dict_items(val.id)})
        vals.append(val)
    
    return RetMsg(data = MsgEditDictMap(data=vals, total=count)) 