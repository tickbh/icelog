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
    menu = Menus(id=1, type="sys", name="系统管理", component="Layout", icon="aaa", params="", pid=0, path="/", redirect="/", sort=0, is_show=True, groups="1")
    session.add(menu)
    menu = Menus(id=10, type="sys", name="用户管理", component="Layout", icon="aaa", params="", pid=1, path="/user", redirect="/user", sort=0, is_show=True, groups="1")
    session.add(menu)
    pass

def init_perm(session: Session):
    from iceslog.models import Perms, GroupPerms
    perm = Perms(
        id=1,
        name="最高权限",
        route="*",
        codename="super",
        sort=0,
    )
    session.add(perm)
    session.commit()
    
    gp = GroupPerms(
        id=1,
        name="管理员",
        permissions="1",
        sort=0,
    )
    session.add(gp)
    session.commit()
    pass


def init_user(session: Session) -> None:
    from iceslog.models import UserBase, User
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.username == settings.FIRST_SUPER_USER)
    ).first()
    if not user:
        user = User(
            username=settings.FIRST_SUPER_USER,
            is_active=True,
            is_superuser=True,
            user_type="sys",
            hashed_password=get_password_hash(settings.FIRST_SUPER_PASS),
            group_pem=1,
        )
        session.add(user)
        session.commit()
        session.refresh(user)


def init() -> None:
    logger.info("Creating initial data")
    with Session(engine) as session:
        init_perm(session)
        init_menu(session)
        init_user(session)
    logger.info("Initial data created")


def main() -> None:
    init()

if __name__ == "__main__":
    main()
