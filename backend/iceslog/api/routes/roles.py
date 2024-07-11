from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, or_, select

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
)
from iceslog.models.base import OptionType
from iceslog.models.dictmap import DictMap, DictMapItem, MsgDictItemsPublic, MsgEditDictMap, OneDictItem, OneEditDictMap
from iceslog.models.perms import GroupPerms, GroupPermsBase, GroupPermsPublic, OnePerm, Perms, PermsPublic
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition

router = APIRouter()


@router.get("/page", response_model=GroupPermsPublic)
def get_perms(session: SessionDep, keywords: str = None, pageNum: int = 0, pageSize: int = 100):
    condition = []
    if keywords:
        condition.append(or_(GroupPerms.name.like(f"%{keywords}%"), GroupPerms.code.like(f"%{keywords}%")))
    perms, count = page_view_condition(session, condition, GroupPerms, pageNum, pageSize, [GroupPerms.sort])
    return GroupPermsPublic(list=perms, total=count)

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
def read_dicts(session: SessionDep, pageNum: int = 0, pageSize: int = 100, keywords: str = None) -> Any:
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
    response_model=OnePerm,
)
def get_form_dict(session: SessionDep, perm_id: int) -> Any:
    perm = session.exec(select(Perms).where(Perms.id==perm_id)).first()
    if not perm:
        raise HTTPException(status_code=400, detail="不存在该权限id")
    perm = OnePerm.model_validate(perm)
    
    for groups in session.exec(select(GroupPerms)).all():
        for perm_id in base_utils.split_to_int_list(groups.permissions):
            if perm_id != perm.id:
                continue
            perm.groups = base_utils.append_split_to_str(perm.groups, groups.id)
            perm.groups_name = base_utils.append_split_to_str(perm.groups_name, groups.name)
    
    return perm

@router.put(
    "/{perm_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def modify_perm(session: SessionDep, perm_id: int, perm_map: OnePerm) -> Any:
    map = session.exec(select(Perms).where(Perms.id == perm_id)).first()
    if not map:
        raise HTTPException(400, "不存在该权限选项")
    
    map.codename = perm_map.codename
    map.name = perm_map.name
    map.route = perm_map.route
    map.sort = perm_map.sort
    map.is_show = perm_map.is_show
    session.merge(map)
    session.commit()
    
    group_perms = base_utils.split_to_int_list(perm_map.groups) 
        
    for groups in session.exec(select(GroupPerms)).all():
        now_perms = base_utils.split_to_int_list(groups.permissions)
        if perm_id in now_perms and not groups.id in group_perms:
            now_perms.remove(perm_id)
            groups.permissions = base_utils.join_list_to_str(now_perms)
            session.merge(groups)
            session.commit()
        elif not perm_id in now_perms and groups.id in group_perms:
            now_perms.append(perm_id)
            groups.permissions = base_utils.join_list_to_str(now_perms)
            session.merge(groups)
            session.commit()
        
    return RetMsg()


@router.delete(
    "/{perms}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def delete_dict(session: SessionDep, perms: str) -> Any:
    del_ids = []
    for perm_id in base_utils.split_to_int_list(perms):
        map = session.exec(select(Perms).where(Perms.id == perm_id)).first()
        if not map:
            raise HTTPException(400, "不存在该字典选项")
        
        del_ids.append(perm_id)
        session.delete(map)
        session.commit()
        
    for groups in session.exec(select(GroupPerms)).all():
        now_perms = base_utils.split_to_int_list(groups.permissions)
        has_del = False
        for id in del_ids:
            if id in now_perms:
                now_perms.remove(id)
                has_del = True
        
        if has_del:
            groups.permissions = base_utils.join_list_to_str(now_perms)
            session.merge(groups)
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