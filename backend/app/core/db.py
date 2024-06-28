from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models import UserBase, User

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == "super@qq.com")
    ).first()
    if not user:
        user = User(
            email="super@qq.com",
            is_active=True,
            is_superuser=True,
            hashed_password="aaaaaaaaaaaaa",
        )
        session.add(user)
        session.commit()
        session.refresh(user)
