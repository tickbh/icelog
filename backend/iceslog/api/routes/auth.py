
from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException, Request
from iceslog import cruds
from iceslog.api.deps import CurrentUser, RedisDep, SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, LoginoutRet, RetMsg, LoginRet, Token
from iceslog.utils import base_utils, log_utils
router = APIRouter()


@router.get("/captcha")
async def get_captcha(redis: RedisDep) -> AuthCaptcha:
    img, text = img_captcha(img_byte="base64")
    key_hex = base_utils.random_hex(16)
    key = f"captcha:{key_hex}"
    await redis.set(key, text, ex=120)
    return AuthCaptcha(captchaKey=key_hex, captchaBase64="data:image/png;base64," + img)
# .build_message()

@router.post("/login")
async def do_login(request: Request, session: SessionDep, redis: RedisDep, username: str = Form(), password: str = Form(), captchaKey: str = Form(), captchaCode: str = Form()) -> LoginRet:
    key = f"captcha:{captchaKey}"
    value = await redis.get(key)
    if not value:
        raise HTTPException(400, "验证码已过期")
    
    # if captchaCode.lower() != value.lower():
    #     raise HTTPException(400, "验证码错误")
    
    log_utils.do_record_syslog(request, "LOGIN", f"{username}请求登陆")
    user = cruds.user.authenticate(
        session=session, username=username, password=password
    )
    if not user:
      raise HTTPException(400, "用户名或者密码错误")
    elif user.status != 1:
      raise HTTPException(400, "用户尚未激活")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return LoginRet(
        accessToken=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.delete("/logout")
def do_logout(request: Request, curent_user: CurrentUser) -> LoginoutRet:
    log_utils.do_record_syslog(request, "LOGOUT", f"{curent_user.username}注销登陆")
    # if captchaCode.lower() != captchaKey.lower():
        # return RetMsg.err_msg("00003", "验证码错误")
    return LoginoutRet()