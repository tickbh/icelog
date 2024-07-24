from fastapi import APIRouter
from iceslog.api.routes import users, login, auth, menus, roles, dictmap, perm, syslog, stats
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="", tags=["login"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(dictmap.router, prefix="/dict", tags=["dict"])
api_router.include_router(perm.router, prefix="/perm", tags=["perm"])
api_router.include_router(syslog.router, prefix="/syslog", tags=["syslog"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])

from iceslog.api.routes.logs import store, read
api_router.include_router(store.router, prefix="/logs/store", tags=["store"])
api_router.include_router(read.router, prefix="/logs/read", tags=["read"])

from iceslog.api.public_routes import log
api_router.include_router(log.router, prefix="/pub/log", tags=["log"])