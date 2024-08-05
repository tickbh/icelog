from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, select

from iceslog.api.deps import (
    CurrentUser,
    PageNumType,
    PageSizeType,
    SessionDep,
    check_has_perm,
    get_current_active_superuser,
)
from iceslog.models import (
    RetMsg,
)
from iceslog.models.base import OptionType
from iceslog.models.perms import GroupPerms, OnePerm, Perms, PermsPublic
from iceslog.utils import base_utils
from iceslog.utils.utils import page_view_condition

router = APIRouter(
    dependencies=[Depends(check_has_perm)]
)


@router.get("/page", response_model=PermsPublic)
def get_perms(session: SessionDep, keywords: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    table_perms: dict[int, OnePerm] = {}
    condition = [Perms.status == True]
    if keywords:
        condition.append(Perms.name.like(f"%{keywords}%"))
    perms, count = page_view_condition(session, condition, Perms, pageNum, pageSize, [Perms.sort])
    for pem in perms:
        one = OnePerm.model_validate(pem)
        table_perms[one.id] = one
        
    for groups in session.exec(select(GroupPerms)).all():
        for id in base_utils.split_to_int_list(groups.permissions):
            if not id in table_perms:
                continue
            table_perms[id].groups = base_utils.append_split_to_str(table_perms[id].groups, groups.id)
            table_perms[id].groups_name = base_utils.append_split_to_str(table_perms[id].groups_name, groups.name)
    return PermsPublic(list=perms, total=count)

@router.get(
    "/group/options",
    response_model=List[OptionType],
)
def read_options(session: SessionDep, user: CurrentUser) -> Any:
    rets = []
    for group in session.exec(select(GroupPerms)).all():
        rets.append(OptionType(value=group.id, label=group.name))
    return rets


def build_option(perm: OnePerm) -> OptionType:
    value = OptionType(value=perm.id, label=perm.name)
    for child in perm.children:
        value.children.append(build_option(child))
    return value

@router.get(
    "/options",
    response_model=List[OptionType],
)
def read_options(session: SessionDep, user: CurrentUser) -> Any:
    ret_list = read_all_perms(session)
    rets = []
    for v in ret_list:
        rets.append(build_option(v))
    return rets


@router.get(
    "",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[OnePerm],
)
def read_all_perms(session: SessionDep, keywords: str = None) -> Any:

    statement = select(Perms).where(Perms.status==True)
    if keywords:
        statement = statement.where(Perms.name.like(f"%{keywords}%"))

    all_perms: list[OnePerm] = []
    perm_table : dict[int, OnePerm] = {}
    for perm in session.exec(select(Perms).order_by(Perms.sort)).all():
        one = OnePerm.model_validate(perm)
        all_perms.append(one)
        perm_table[one.id] = one
        
    for groups in session.exec(select(GroupPerms)).all():
        for id in base_utils.split_to_int_list(groups.permissions):
            if not id in perm_table:
                continue
            perm_table[id].groups = base_utils.append_split_to_str(perm_table[id].groups, groups.id)
            perm_table[id].groups_name = base_utils.append_split_to_str(perm_table[id].groups_name, groups.name)
    
    ret_list = []
    for menu in all_perms:
        if menu.pid == 0:
            ret_list.append(menu)
        else:
            if menu.pid in perm_table:
                parent = perm_table[menu.pid]
                parent.children.append(menu)
            else:
                ret_list.append(menu)
    return ret_list

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
    map.status = perm_map.status
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
def add_perm(session: SessionDep, one: OnePerm) -> Any:
    map = Perms.model_validate(one)
    del map.id
    session.add(map)
    session.commit()
    session.refresh(map)
    
    now_perms = base_utils.split_to_int_list(one.groups)
    if len(now_perms) > 0:
        for groups in session.exec(select(GroupPerms).where(col(GroupPerms.id).in_(now_perms))).all():
            perms = base_utils.split_to_int_list(groups.permissions)
            perms.append(map.id)
            groups.permissions = base_utils.join_list_to_str(perms)
            session.merge(groups)
            session.commit()
    
    return RetMsg()