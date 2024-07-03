
from typing import Any
from .menu import *
from .user import *
from .pems import *

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Generic message
class Message(SQLModel):
    code: str
    msg: str
    data: Any

class CommonMessage(SQLModel):
    def build_message(self, code="00000", msg="ok") -> Message:
        return Message(data=self, code=code, msg=msg)
    
# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None

# Contents of JWT token
class AuthCaptchaMsg(CommonMessage):
    captchaKey: str
    captchaBase64: str
    
# Contents of JWT token
class AuthLogin(SQLModel):
    username: str
    password: str
    captchaKey: str
    captchaCode: str