from collections.abc import Generator
import logging
from typing import Annotated, AsyncGenerator

from redis.asyncio import Redis
import jwt
from fastapi import Depends, HTTPException, Path, Query, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from iceslog.core import security
from iceslog.core.config import settings
from iceslog.core.db import engine, get_db
from iceslog.models.user import UserEx
from iceslog.models import TokenPayload, User
from iceslog.utils.pool_utils import get_redis_cache

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
RedisDep = Annotated[Redis, Depends(get_redis_cache)]

async def get_current_user(session: SessionDep, token: TokenDep, redis: RedisDep) -> AsyncGenerator[UserEx, None]:
    
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
        
    cache_key = f"user:{token_data.sub}"
    cache_user = await redis.get(cache_key)
    user_ex: UserEx = None
    if cache_user:
        from iceslog.utils import base_utils
        data = base_utils.safe_json(cache_user)
        try:
            user_ex = UserEx.model_validate({}, update=data)
        except Exception as e:
            base_utils.print_exec()
            print(e)
    
    if not user_ex:    
        user = session.get(User, token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.status != 1:
            raise HTTPException(status_code=400, detail="Inactive user")
        user_ex = UserEx.model_validate(user)
        await redis.set(cache_key, user_ex.model_dump_json(), ex=3600 * 3)
    yield user_ex
    if user_ex.is_changed:
        user_ex.is_changed = False
        await redis.set(cache_key, user_ex.model_dump_json(), ex=3600 * 3)


CurrentUser = Annotated[UserEx, Depends(get_current_user)]

PageNumType = Annotated[int, Query(title="Check Default Page Num", ge=1)]
PageSizeType = Annotated[int, Query(title="Check Default Page Size", ge=10, le=100)]

def get_current_active_superuser(current_user: CurrentUser) -> User:
    # if not current_user.is_superuser:
    #     raise HTTPException(
    #         status_code=403, detail="The user doesn't have enough privileges"
    #     )
    return current_user

def split_path_info(path_info):
    paths = path_info.split("/")
    arrays = ["*"]
    for i in range(len(paths)):
        arrays.append("/".join(paths[:len(paths) - i]))
    return arrays

def check_has_perm(request: Request, current_user: CurrentUser):
    from iceslog.utils import cache_utils
    perms = cache_utils.get_all_perms_ids(current_user.group_pem)
    
    for path in split_path_info(request.url.path):
        perm = cache_utils.get_perm(path)
        logging.info(f'chk perm: {perm} - {path}')
        if not perm:
            continue
        if perm["id"] in perms:
            return
        if path == "*":
            continue
        raise HTTPException(400, f"您不能访问:{request.url.path}, 缺少权限{path}")
    
    raise HTTPException(400, f"您不能访问:{request.url.path}, 未配置权限权限{request.url.path}")