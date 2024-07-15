
from datetime import timedelta
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, Request
from iceslog import cruds
from iceslog.api.deps import CurrentUser, RedisDep, SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, LoginoutRet, RetMsg, LoginRet, Token
from iceslog.models.log_record import RecordLog
from iceslog.utils import base_utils, log_utils
router = APIRouter()

@router.post("")
async def record_log(background_tasks: BackgroundTasks, request: Request, log: RecordLog) -> RetMsg:
    background_tasks.add_task(log_utils.do_record_apilog, log)
    # await log_utils.do_record_apilog(request, log)
    return RetMsg()

@router.post("/batch")
async def record_log(background_tasks: BackgroundTasks, request: Request, logs: list[RecordLog]) -> RetMsg:
    background_tasks.add_task(log_utils.do_record_apilogs, logs)
    # await log_utils.do_record_apilogs(request, logs)
    return RetMsg()