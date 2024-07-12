
from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException, Request
from iceslog import cruds
from iceslog.api.deps import CurrentUser, SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, LoginoutRet, RetMsg, LoginRet, Token
from iceslog.utils import log_utils
router = APIRouter()


@router.get("/captcha")
def get_captcha() -> AuthCaptcha:
    img, text = img_captcha(img_byte="base64")
    return AuthCaptcha(captchaKey=text, captchaBase64="data:image/png;base64," + img)
# .build_message()

@router.post("/login")
def do_login(request: Request, session: SessionDep, username: str = Form(), password: str = Form(), captchaKey: str = Form(), captchaCode: str = Form()) -> LoginRet:
    # if captchaCode.lower() != captchaKey.lower():
        # return RetMsg.err_msg("00003", "验证码错误")
    log_utils.do_record_log(request, "LOGIN", f"{username}请求登陆")
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
def do_logout(request: Request, curent_user: CurrentUser) -> LoginoutRet:
    log_utils.do_record_log(request, "LOGOUT", f"{curent_user.username}注销登陆")
    # if captchaCode.lower() != captchaKey.lower():
        # return RetMsg.err_msg("00003", "验证码错误")
    return LoginoutRet()