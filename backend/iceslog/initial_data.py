import logging

from sqlalchemy import select
from sqlmodel import Session

from iceslog.core.db import engine
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_menu(session: Session):
    from iceslog.models import Menus
    menu = Menus(id=1, belong="sys", type="MENU", name="系统管理", component="Layout", icon="aaa",
                 params="", pid=0, path="/system", redirect="/system/user", sort=0, is_show=True, groups="1")
    session.add(menu)
    menu = Menus(id=10, pid=1, belong="sys|admin", type="MENU", name="用户管理", component="system/user/index",
                 icon="aaa", params="", path="user", redirect="", sort=0, is_show=True, groups="1")
    session.add(menu)
    # menu = Menus(id=101, pid=0, belong="sys|admin", type="BUTTON", name="用户查询权限", perm="sys:user:query", is_show=True, component="", icon="", params="", path="", redirect="", sort=0, groups="1")
    # session.add(menu)
    # menu = Menus(id=102, pid=0, belong="sys|admin", type="BUTTON", name="用户新增权限", perm="sys:user:add", is_show=True, component="", icon="", params="", path="", redirect="", sort=0, groups="1")
    # session.add(menu)
    # menu = Menus(id=103, pid=0, belong="sys|admin", type="BUTTON", name="用户编辑", perm="sys:user:edit", is_show=True, component="", icon="", params="", path="", redirect="", sort=0, groups="1")
    # session.add(menu)
    # menu = Menus(id=104, pid=0, belong="sys|admin", type="BUTTON", name="用户删除", perm="sys:user:delete", is_show=True, component="", icon="", params="", path="", redirect="", sort=0, groups="1")
    # session.add(menu)
    # menu = Menus(id=105, pid=0, belong="sys|admin", type="BUTTON", name="重置密码", perm="sys:user:password:reset", is_show=True, component="", icon="", params="", path="", redirect="", sort=0, groups="1")
    # session.add(menu)
    menu = Menus(id=11, pid=1, belong="sys", type="MENU", name="角色管理", component="system/role/index",
                 icon="dict", params="", path="role", redirect="", sort=0, is_show=True, groups="1")
    session.add(menu)
    menu = Menus(id=12, pid=1, belong="sys", type="MENU", name="菜单管理", component="system/menu/index",
                 icon="dict", params="", path="menu", redirect="", sort=0, is_show=True, groups="1")
    session.add(menu)
    menu = Menus(id=13, pid=1, belong="sys", type="MENU", name="权限管理", component="system/perm/index",
                 icon="dict", params="", path="perm", redirect="", sort=0, is_show=True, groups="1")
    session.add(menu)
    menu = Menus(id=14, pid=1, belong="sys", type="MENU", name="字典管理", component="system/dict/index",
                 icon="dict", params="", path="dict", redirect="", sort=0, is_show=True, groups="1")
    session.add(menu)
    session.commit()


def init_perm(session: Session):
    from iceslog.models import Perms, GroupPerms
    perm = Perms(id=1, name="最高权限", route="*", codename="*", sort=0, )
    session.add(perm)
    perm = Perms(id=2, name="用户查询权限", route="",
                 codename="sys:user:query", sort=0, )
    session.add(perm)
    perm = Perms(id=3, name="用户新增权限", route="",
                 codename="sys:user:add", sort=0, )
    session.add(perm)
    perm = Perms(id=4, name="用户编辑", route="",
                 codename="sys:user:edit", sort=0, )
    session.add(perm)
    perm = Perms(id=5, name="用户删除", route="",
                 codename="sys:user:delete", sort=0, )
    session.add(perm)
    perm = Perms(id=6, name="重置密码", route="",
                 codename="sys:user:password:reset", sort=0, )
    session.add(perm)

    session.commit()

    gp = GroupPerms(
        id=1,
        name="管理员",
        permissions="1,2,3,4,5,6",
        sort=0,
    )
    session.add(gp)
    session.commit()
    pass

def init_dict(session: Session):
    from iceslog.models import DictMap, DictMapItem
    dict_map = DictMap(id=1, name="性别", code="gender", status=0, remark="性别字典")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=1, label="男", value="1", status=0, remark="性别字典")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=1, label="女", value="2", status=0, remark="性别字典")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=1, label="保密", value="0", status=0, remark="性别字典")
    session.add(dict_map)
    session.commit()
    
    
    dict_map = DictMap(id=2, name="归属", code="belong", status=0, remark="菜单归属")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=2, label="系统", value="sys", status=0, remark="系统级别")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=2, label="用户", value="usr", status=0, remark="用户级别")
    session.add(dict_map)
    session.commit()

def init_user(session: Session) -> None:
    from iceslog.models import UserBase, User
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = User(
        username=settings.FIRST_SUPER_USER,
        nickname="系统管理员",
        gender=0,
        mobile="13800000000",
        is_active=True,
        is_superuser=True,
        user_type="sys",
        hashed_password=get_password_hash(settings.FIRST_SUPER_PASS),
        group_pem=1,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    # user = session.exec(
    #     select(User).where(User.username == settings.FIRST_SUPER_USER)
    # ).first()
    # if not user:
    #     user = User(
    #         username=settings.FIRST_SUPER_USER,
    #         is_active=True,
    #         is_superuser=True,
    #         user_type="sys",
    #         hashed_password=get_password_hash(settings.FIRST_SUPER_PASS),
    #         group_pem=1,
    #     )
    #     session.add(user)
    #     session.commit()
    #     session.refresh(user)


def init() -> None:
    logger.info("Creating initial data")
    with Session(engine) as session:
        init_dict(session)
        init_perm(session)
        init_menu(session)
        init_user(session)
    logger.info("Initial data created")


def main() -> None:
    init()


if __name__ == "__main__":
    main()
