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
    menu = Menus(id=1, belong="sys", type="MENU", name="系统管理", component="Layout", icon="system",
                 params="", pid=0, path="/system", redirect="/system/user", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=10, pid=1, belong="sys|admin", type="MENU", name="用户管理", component="system/user/index",
                 icon="el-icon-User", params="", path="user", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=11, pid=1, belong="sys", type="MENU", name="角色管理", component="system/role/index",
                 icon="role", params="", path="role", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=12, pid=1, belong="sys", type="MENU", name="菜单管理", component="system/menu/index",
                 icon="menu", params="", path="menu", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=13, pid=1, belong="sys", type="MENU", name="权限管理", component="system/perm/index",
                 icon="el-icon-Finished", params="", path="perm", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=14, pid=1, belong="sys", type="MENU", name="字典管理", component="system/dict/index",
                 icon="dict", params="", path="dict", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=15, pid=1, belong="sys", type="MENU", name="系统日志", component="system/log/index",
                 icon="document", params="", path="log", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    
    menu = Menus(id=2, belong="sys", type="MENU", name="日志管理", component="Layout", icon="el-icon-Document",
                 params="", pid=0, path="/log", redirect="/log/user", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=21, pid=2, belong="sys", type="MENU", name="日志落库", component="log/store/index",
                 icon="document", params="", path="store", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=22, pid=2, belong="sys", type="MENU", name="日志读取", component="log/read/index",
                 icon="document", params="", path="read", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    menu = Menus(id=23, pid=2, belong="sys", type="MENU", name="日志查询", component="log/search/index",
                 icon="document", params="", path="search", redirect="", sort=0, status=1, groups="1")
    session.add(menu)
    session.commit()


def init_perm(session: Session):
    from iceslog.models import Perms, GroupPerms
    perm = Perms(id=1, name="最高权限", route="*", codename="*", sort=0, )
    session.add(perm)
    perm = Perms(id=2, name="用户权限", route="~", codename="~", sort=0, )
    session.add(perm)
    perm = Perms(id=3, name="菜单权限", route="~", codename="~", sort=0, )
    session.add(perm)
    perm = Perms(id=4, name="角色权限", route="~", codename="~", sort=0, )
    session.add(perm)
    perm = Perms(id=5, name="管理权限", route="~", codename="~", sort=0, )
    session.add(perm)
    perm = Perms(pid=2, name="用户查询权限", route="",
                 codename="sys:user:query", sort=0, )
    session.add(perm)
    perm = Perms(pid=2, name="用户新增权限", route="",
                 codename="sys:user:add", sort=0, )
    session.add(perm)
    perm = Perms(pid=2, name="用户编辑", route="",
                 codename="sys:user:edit", sort=0, )
    session.add(perm)
    perm = Perms(pid=2, name="用户删除", route="",
                 codename="sys:user:delete", sort=0, )
    session.add(perm)
    perm = Perms(pid=2, name="重置密码", route="",
                 codename="sys:user:password:reset", sort=0, )
    session.add(perm)

    session.commit()

    gp = GroupPerms(
        id=1,
        name="管理员",
        code="ROOT",
        permissions="1|2|3|4|5|6",
        sort=0,
    )
    session.add(gp)
    session.commit()
    pass

def init_dict(session: Session):
    from iceslog.models import DictMap, DictMapItem
    dict_map = DictMap(id=1, name="性别", code="sys_gender", status=1, remark="性别字典")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=1, label="男", value="1", status=1, remark="性别字典")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=1, label="女", value="2", status=1, remark="性别字典")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=1, label="保密", value="0", status=1, remark="性别字典")
    session.add(dict_map)
    session.commit()
    
    
    dict_map = DictMap(id=2, name="归属", code="sys_belong", status=1, remark="菜单归属")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=2, label="系统", value="sys", status=1, remark="系统级别")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=2, label="管理员", value="admin", status=1, remark="管理员")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=2, label="用户", value="usr", status=1, remark="用户级别")
    session.add(dict_map)
    session.commit()
    
    dict_map = DictMap(id=3, name="存储", code="sys_store", status=1, remark="日志存储方式")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=3, label="ClickHouse", value="ClickHouse", status=1, remark="ClickHouse")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=3, label="MongoDb", value="MongoDb", status=1, remark="MongoDb")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=3, label="Es", value="Es", status=1, remark="Es")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=3, label="Kafka", value="Kafka", status=1, remark="Kafka")
    session.add(dict_map)
    
    dict_map = DictMap(id=4, name="日志等级", code="sys_level", status=1, remark="日志等级")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=4, label="Error", value="1", status=1, remark="错误信息")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=4, label="Warn", value="2", status=1, remark="警告")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=4, label="Info", value="3", status=1, remark="Info")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=4, label="Debug", value="4", status=1, remark="调试")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=4, label="Trace", value="4", status=1, remark="调试")
    session.add(dict_map)
    
    dict_map = DictMap(id=5, name="系统类型", code="sys_sys", status=1, remark="系统类型")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=5, label="IOS", value="IOS", status=1, remark="IOS")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=5, label="Android", value="Android", status=1, remark="安卓")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=5, label="Windows", value="Windows", status=1, remark="Windows")
    session.add(dict_map)
    
    dict_map = DictMap(id=11, name="项目代号", code="project", status=1, remark="项目代号")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=11, label="默认", value="default", status=1, remark="默认")
    session.add(dict_map)
    dict_map = DictMapItem(dict_id=11, label="ices日志", value="iceslog", status=1, remark="ices日志")
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
        status=1,
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
