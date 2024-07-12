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
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition

router = APIRouter()

@router.get("/page", response_model=GroupPermsPublic)
def get_roles(session: SessionDep, pageNum: PageNumType = 1, pageSize: PageSizeType = 10, keywords: str = None):
    condition = []
    if keywords:
        condition.append(or_(GroupPerms.name.like(f"%{keywords}%"), GroupPerms.code.like(f"%{keywords}%")))
    roles, count = page_view_condition(session, condition, GroupPerms, pageNum, pageSize, [GroupPerms.sort])
    return GroupPermsPublic(list=roles, total=count)

@router.get(
    "/options",
    response_model=List[OptionType],
)
def read_options(session: SessionDep, user: CurrentUser) -> Any:
    rets = []
    for group in cache_utils.group_perm_cache_table.cache_iter():
        rets.append(OptionType(value=group["id"], label=group["name"]))
    return rets

@router.get(
    "/page",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MsgEditDictMap,
)
def read_roles(session: SessionDep, pageNum: int = 0, pageSize: int = 100, keywords: str = None) -> Any:
    condition = []
    if keywords:
        condition.append(DictMap.name.like(f"%{keywords}%"))

    dicts, count = page_view_condition(session, condition, DictMap, pageNum, pageSize)
    vals = []
    for val in dicts:
        items = []
        for sub in session.exec(select(DictMapItem).where(DictMapItem.dict_id == val.id)).all():
            items.append(sub)
        val = OneEditDictMap.model_validate(val, update={"dictItems": items})
        vals.append(val)
    
    return MsgEditDictMap(list=vals, total=count) 


@router.get(
    "/form/{perm_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=GroupPermsBase,
)
def get_form_role(session: SessionDep, perm_id: int) -> Any:
    perm = session.exec(select(GroupPerms).where(GroupPerms.id==perm_id)).first()
    if not perm:
        raise HTTPException(status_code=400, detail="不存在该权限id")
    return perm

@router.put(
    "/{perm_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def modify_perm(session: SessionDep, perm_id: int, perm_map: GroupPermsBase) -> Any:
    map = session.exec(select(GroupPerms).where(GroupPerms.id == perm_id)).first()
    if not map:
        raise HTTPException(400, "不存在该权限选项")
    
    map.code = perm_map.code
    map.name = perm_map.name
    map.sort = perm_map.sort
    map.status = perm_map.status
    session.merge(map)
    session.commit()
        
    return RetMsg()


@router.delete(
    "/{perms}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def delete_role(session: SessionDep, perms: str) -> Any:
    for perm_id in base_utils.split_to_int_list(perms):
        map = session.exec(select(GroupPerms).where(GroupPerms.id == perm_id)).first()
        if not map:
            raise HTTPException(400, "不存在该字典选项")
        
        session.delete(map)
        session.commit()
        
    return RetMsg()


@router.post(
    "",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def add_perm(session: SessionDep, one: GroupPermsBase) -> Any:
    map = GroupPerms.model_validate(one)
    del map.id
    session.add(map)
    session.commit()
    session.refresh(map)
    return RetMsg()



@router.get(
    "/perms/{group_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[int],
)
def get_perms(session: SessionDep, group_id: int) -> Any:
    group = session.exec(select(GroupPerms).where(GroupPerms.id == group_id)).first()
    if not group:
        raise HTTPException(400, "不存在id")
    return base_utils.split_to_int_list(group.permissions)



@router.put(
    "/perms/{group_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[int],
)
def put_perms(session: SessionDep, group_id: int, perms: list[int]) -> Any:
    group = session.exec(select(GroupPerms).where(GroupPerms.id == group_id)).first()
    if not group:
        raise HTTPException(400, "不存在id")
    group.permissions = base_utils.join_list_to_str(perms)
    session.merge(group)
    session.commit()
    return perms