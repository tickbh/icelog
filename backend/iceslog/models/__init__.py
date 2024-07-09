
from .base import *
from .menu import *
from .user import *
from .pems import *
from .dictmap import *

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

    
# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None

# Contents of JWT token
class AuthCaptcha(SQLModel):
    captchaKey: str
    captchaBase64: str
    
# Contents of JWT token
class LoginRet(SQLModel):
    accessToken: str
    tokenType: str = "Bearer"
    refreshToken: str|None = None
    expires: str|None = None
    
class LoginoutRet(RetMsg):
    pass