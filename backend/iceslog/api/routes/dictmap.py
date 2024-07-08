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
from iceslog.models.dictmap import MsgDictItemsPublic
from iceslog.models.user import MsgUserMePublic, MsgUserPublic, MsgUsersPublic, UserMePublic
from iceslog.utils import cache_utils, generate_new_account_email, send_email
from iceslog.utils.cache_table import CacheTable

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