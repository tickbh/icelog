
from datetime import timedelta
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
        "perm": data.perm,
        "meta": {
            "title": data.name,
            "icon": data.icon,
            "hidden": not data.is_show or len(data.perm or "") > 0,
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
def get_menus(session: SessionDep):
    all_menus: list[OneEditMenu] = []
    menu_table = {}
    for menu in session.exec(select(Menus).where(Menus.is_show == True)).all():
        one = OneEditMenu.model_validate(menu)
        all_menus.append(one)
        menu_table[one.id] = one
    
    ret_list = []
    for menu in all_menus:
        if menu.pid == 0:
            ret_list.append(menu)
        else:
            parent = menu_table[menu.pid]
            parent.children.append(menu)
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
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu

# @router.get(
#     "/page",
#     dependencies=[Depends(get_current_active_superuser)],
#     response_model=MsgEditDictMap,
# )
# def read_users(session: SessionDep, pageNum: int = 0, pageSize: int = 100, keywords: str = None) -> Any:
#     """
#     Retrieve users.
#     """
#     condition = []
#     if keywords:
#         condition.append(DictMap.name.like(f"%{keywords}%"))

#     dicts, count = page_view_condition(session, condition, DictMap, pageNum, pageSize)
    
#     for val in dicts:
#         val.dictItems = 
    
#     return MsgUsersPublic(data = UsersPublic(list=users, total=count)) 
