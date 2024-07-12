
from datetime import datetime, timedelta
import json
from typing import Any, List
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import ORJSONResponse
from sqlmodel import select
from iceslog import cruds
from iceslog.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, RetMsg, LoginRet, Token
from iceslog.models.dictmap import DictMap, MsgEditDictMap
from iceslog.models.menu import Menus, OneEditMenu, OneLabelMenu
from iceslog.utils import PidTable
from iceslog.utils.utils import page_view_condition
router = APIRouter()

def deal_func(data: Menus):
    new_data = {
        "id": data.id,
        "path": data.path,
        "component": data.component,
        "redirect": data.redirect,
        "name": data.name,
        "perm": "",
        "meta": {
            "title": data.name,
            "icon": data.icon,
            "hidden": not data.is_show ,
            "alwaysShow": False,
            "params": data.params,
        }
    }
    return new_data

pid_cls = PidTable(Menus, deal_func=deal_func)

@router.get("/routes", response_class=ORJSONResponse)
def get_routes(current_user: CurrentUser):
    menus = pid_cls.get_values(current_user.user_type)
    return ORJSONResponse(menus)


@router.get("", response_model=list[OneEditMenu])
def get_menus(session: SessionDep, keywords: str = None):
    all_menus: list[OneEditMenu] = []
    menu_table = {}
    statement = select(Menus).where(Menus.is_show == True)
    if keywords:
        statement = statement.where(Menus.name.like(f"%{keywords}%"))
    for menu in session.exec(statement).all():
        one = OneEditMenu.model_validate(menu)
        all_menus.append(one)
        menu_table[one.id] = one
    
    ret_list = []
    for menu in all_menus:
        if menu.pid == 0:
            ret_list.append(menu)
        else:
            if menu.pid in menu_table:
                parent = menu_table[menu.pid]
                parent.children.append(menu)
            else:
                ret_list.append(menu)
    return ret_list

def get_onelabel(session: SessionDep) -> OneLabelMenu:
    rets = get_menus(session)
    return rets


@router.get(
    "/options",
    response_model=List[OneLabelMenu],
)
def read_options(session: SessionDep, user: CurrentUser) -> Any:
    menus = get_menus(session)
    rets = []
    for menu in menus:
        rets.append(OneLabelMenu.build_from(menu))
    return rets

@router.post(
    "",
    response_model=Menus,
)
def add_menu(session: SessionDep, user: CurrentUser, menu: Menus) -> Any:
    menu.create_time = datetime.now()
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu

@router.get(
    "/form/{menu_id}",
    response_model=Menus,
)
def get_form_menu(session: SessionDep, user: CurrentUser, menu_id: int) -> Any:
    
    menu = session.exec(select(Menus).where(Menus.id == menu_id)).first()
    if not menu:
        raise HTTPException(400, "不存在该菜单id")
        
    return menu

@router.put(
    "/{menu_id}",
    response_model=Menus,
)
def add_menu(session: SessionDep, user: CurrentUser, menu_id: int, menu: Menus) -> Any:
    db_menu = session.exec(select(Menus).where(Menus.id == menu_id)).first()
    if not db_menu:
        raise HTTPException(400, "不存在菜单id")
    menu.create_time = db_menu.create_time
    db_menu.sqlmodel_update(menu)
    session.merge(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu

@router.delete(
    "/{menu_id}",
    response_model=Menus,
)
def delete_menu(session: SessionDep, user: CurrentUser, menu_id: int) -> Any:
    db_menu = session.exec(select(Menus).where(Menus.id == menu_id)).first()
    if not db_menu:
        raise HTTPException(400, "不存在菜单id")
    
    if session.exec(select(Menus).where(Menus.pid == menu_id)).first():
        raise HTTPException(400, "字菜单为空, 不能删除")
    
    session.delete(db_menu)
    session.commit()
    return db_menu

