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

