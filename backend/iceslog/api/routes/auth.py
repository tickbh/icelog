
from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException
from iceslog import cruds
from iceslog.api.deps import SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, LoginoutRet, RetMsg, LoginRet, Token
router = APIRouter()


@router.get("/captcha")
def get_captcha() -> AuthCaptcha:
    img, text = img_captcha(img_byte="base64")
    return AuthCaptcha(captchaKey=text, captchaBase64="data:image/png;base64," + img)
# .build_message()

@router.post("/login")
def do_login(session: SessionDep, username: str = Form(), password: str = Form(), captchaKey: str = Form(), captchaCode: str = Form()) -> LoginRet:
    # if captchaCode.lower() != captchaKey.lower():
        # return RetMsg.err_msg("00003", "验证码错误")
    user = cruds.user.authenticate(
        session=session, username=username, password=password
    )
    if not user:
      raise HTTPException(400, "用户名或者密码错误")
    elif not user.is_active:
      raise HTTPException(400, "用户尚未激活")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return LoginRet(
        accessToken=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.delete("/logout")
def do_login(session: SessionDep) -> LoginoutRet:
    # if captchaCode.lower() != captchaKey.lower():
        # return RetMsg.err_msg("00003", "验证码错误")
    return LoginoutRet()