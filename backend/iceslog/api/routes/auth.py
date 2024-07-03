
from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException
from iceslog import cruds
from iceslog.api.deps import SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import MsgAuthCaptcha, RetMsg, MsgLoginRet, Token
router = APIRouter()


@router.get("/captcha")
def get_captcha() -> RetMsg:
    img, text = img_captcha(img_byte="base64")
    return MsgAuthCaptcha(captchaKey=text, captchaBase64="data:image/png;base64," + img).build_message()

@router.post("/login")
def do_login(session: SessionDep, username: str = Form(), password: str = Form(), captchaKey: str = Form(), captchaCode: str = Form()) -> RetMsg:
    # if captchaCode.lower() != captchaKey.lower():
    #     return Message(code="00001", msg="验证码出错", data=None)
    
    user = cruds.user.authenticate(
        session=session, username=username, password=password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return MsgLoginRet(
        accessToken=security.create_access_token(
            user.userId, expires_delta=access_token_expires
        )
    ).build_message()
