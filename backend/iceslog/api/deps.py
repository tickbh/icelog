from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from iceslog.core import security
from iceslog.core.config import settings
from iceslog.core.db import engine, get_db
from iceslog.models import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户验证失败,请重新登陆",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

PageNumType = Annotated[int, Path(title="The ID of the item to get", ge=1)]
PageSizeType = Annotated[int, Path(title="The ID of the item to get", ge=10, le=100)]

def get_current_active_superuser(current_user: CurrentUser) -> User:
    # if not current_user.is_superuser:
    #     raise HTTPException(
    #         status_code=403, detail="The user doesn't have enough privileges"
    #     )
    return current_user
