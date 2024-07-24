from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

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
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from iceslog.models.dictmap import DictMap, DictMapItem, MsgDictItemsPublic, MsgEditDictMap, OneDictItem, OneEditDictMap
from iceslog.utils import base_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition

router = APIRouter(
    dependencies=[Depends(check_has_perm)])


dict_cache_table = CacheTable(models.DictMap, attribs=["id", "code"])
def get_dict(id):
    return dict_cache_table.get_value(id)

dict_item_cache_table = CacheTable(models.DictMapItem, attribs=["id"], groups=["dict_id"])
def get_dict_items(id):
    return dict_item_cache_table.get_group(id)

@router.get(
    "/options",
    response_model=List[OneDictItem],
)
def read_options(session: SessionDep, user: CurrentUser, key: str) -> Any:
    group = get_dict(key)
    if not group:
        return []
    items = get_dict_items(group["id"])
    if not items:
        return []
    return items

@router.get(
    "/page",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MsgEditDictMap,
)
def read_dicts(session: SessionDep, pageNum: PageNumType = 1, pageSize: PageSizeType = 100, keywords: str = None) -> Any:
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
    "/form/{dict_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=OneEditDictMap,
)
def get_form_dict(session: SessionDep, dict_id: int) -> Any:
    dict_map = session.exec(select(DictMap).where(DictMap.id==dict_id)).first()
    if not dict_map:
        raise HTTPException(status_code=400, detail="不存在该字典id")
    
    if dict_map.code.startswith("sys_"):
        raise HTTPException(status_code=400, detail="系统字段无法修改")
    items = []
    for sub in session.exec(select(DictMapItem).where(DictMapItem.dict_id == dict_id)).all():
        items.append(sub)
    val = OneEditDictMap.model_validate(dict_map, update={"dictItems": items})
    return val

@router.put(
    "/{dict_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def modify_dict(session: SessionDep, dict_id: int, dict_map: OneEditDictMap) -> Any:
    map = session.exec(select(DictMap).where(DictMap.id == dict_id)).first()
    if not map:
        raise HTTPException(400, "不存在该字典选项")
    
    if map.code.startswith("sys_"):
        raise HTTPException(status_code=400, detail="系统字段无法修改")
    
    if map.name != dict_map.name or map.code != dict_map.code or map.status != dict_map.status:
        map.name = dict_map.name
        map.code = dict_map.code
        map.status = dict_map.status
        session.add(map)
        session.commit()
        
    for sub in session.exec(select(DictMapItem).where(DictMapItem.dict_id == dict_id)).all():
        find = None
        for child in dict_map.dictItems:
            if sub.id == child.id:
                find = child
                break
        if not find:
            session.delete(sub)
            session.commit()
        elif find.label != sub.label or find.value != sub.value or find.status != sub.status or find.sort != sub.sort:
            sub.label = find.label
            sub.value = find.value
            sub.status = find.status
            sub.sort = find.sort
            session.add(map)
            session.commit()
            
    for child in dict_map.dictItems:
        if 0 == child.id:
            del child.id
            item = DictMapItem.model_validate(child)
            item.dict_id = dict_id
            session.add(item)
            session.commit()
    return RetMsg()


@router.delete(
    "/{dicts}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def delete_dict(session: SessionDep, dicts: str) -> Any:
    for dict_id in base_utils.split_to_int_list(dicts, ","):
        map = session.exec(select(DictMap).where(DictMap.id == dict_id)).first()
        if not map:
            raise HTTPException(400, "不存在该字典选项")
        
        if map.code.startswith("sys_"):
            raise HTTPException(status_code=400, detail="系统字段无法删除")
        
        session.delete(map)
        session.exec(delete(DictMapItem).where(DictMapItem.dict_id == dict_id))
        session.commit()
    return RetMsg()


@router.post(
    "",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RetMsg,
)
def add_dict(session: SessionDep, dict_map: OneEditDictMap) -> Any:
    del dict_map.id
    map = DictMap.model_validate(dict_map)
    if map.code.startswith("sys_"):
        raise HTTPException(status_code=400, detail="无法新增系统字典")
    session.add(map)
    session.commit()
    session.refresh(map)
    
    for child in dict_map.dictItems:
        del child.id
        item = DictMapItem.model_validate(child)
        item.dict_id = map.id
        session.add(item)
        session.commit()
    return RetMsg()