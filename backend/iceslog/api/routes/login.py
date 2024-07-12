from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from iceslog import cruds
from iceslog.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash
from iceslog.models import RetMsg, NewPassword, Token, UserPublic
from iceslog.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    raise HTTPException(status_code=400, detail="Not support from this")
    # user = cruds.user.authenticate(
    #     session=session, email=form_data.username, password=form_data.password
    # )
    # if not user:
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")
    # elif not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # return Token(
    #     access_token=security.create_access_token(
    #         user.id, expires_delta=access_token_expires
    #     )
    # )

