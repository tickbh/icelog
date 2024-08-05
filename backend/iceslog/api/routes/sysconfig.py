from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import or_, select

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
from iceslog.models.sysconfig import PageSysConfig, SysConfig, SysConfigBase
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.utils import page_view_condition

router = APIRouter(
    dependencies=[Depends(check_has_perm)])


@router.get("/page", response_model=PageSysConfig)
def get_pages(session: SessionDep, pageNum: PageNumType = 1, pageSize: PageSizeType = 10, keywords: str = None):
    condition = []
    if keywords:
        condition.append(or_(SysConfig.name.like(
            f"%{keywords}%"), SysConfig.key.like(f"%{keywords}%")))
    datas, count = page_view_condition(
        session, condition, SysConfig, pageNum, pageSize, [SysConfig.sort])
    return PageSysConfig(list=datas, total=count)


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
    "/form/{data_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SysConfigBase,
)
def get_form_data(session: SessionDep, data_id: int) -> Any:
    data = session.exec(select(SysConfig).where(
        SysConfig.id == data_id)).first()
    if not data:
        raise HTTPException(status_code=400, detail="不存在该数据")
    return data


@router.put(
    "/{data_id}",
    response_model=RetMsg,
)
def modify_data(session: SessionDep, data_id: int, data: SysConfigBase) -> Any:
    map = session.exec(select(SysConfig).where(
        SysConfig.id == data_id)).first()
    if not map:
        raise HTTPException(400, "不存在该数据")

    map.name = data.name
    map.key = data.key
    map.value = data.value
    map.remark = data.remark
    map.sort = data.sort
    map.status = data.status
    session.merge(map)
    session.commit()

    return RetMsg()


@router.delete(
    "/{ids}",
    response_model=RetMsg,
)
def delete_role(session: SessionDep, ids: str) -> Any:
    for data_id in base_utils.split_to_int_list(ids):
        map = session.exec(select(SysConfig).where(
            SysConfig.id == data_id)).first()
        if not map:
            raise HTTPException(400, "不存在该数据")

        session.delete(map)
        session.commit()

    return RetMsg()


@router.post(
    "",
    response_model=RetMsg,
)
def add_data(session: SessionDep, one: SysConfigBase) -> Any:
    data = SysConfig.model_validate(one)
    del data.id
    session.add(data)
    session.commit()
    session.refresh(data)
    return RetMsg()


@router.patch(
    "",
    response_model=RetMsg,
)
def patch_data(session: SessionDep) -> Any:
    return RetMsg()
