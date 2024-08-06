
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, Query, Request
from iceslog import cruds
from iceslog.api.deps import CurrentUser, RedisDep, SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, LoginoutRet, RetMsg, LoginRet, Token
from iceslog.models.logs.record import RecordLog
from iceslog.utils import base_utils, log_utils
router = APIRouter()

ProjectType = Annotated[str, Query(title="Check Default Page Num")]
@router.post("")
async def record_log(background_tasks: BackgroundTasks, request: Request, log: RecordLog, project: ProjectType = "default") -> RetMsg:
    background_tasks.add_task(log_utils.do_record_apilog, project, log)
    # await log_utils.do_record_apilog(request, log)
    return RetMsg()

@router.post("/batch")
async def record_log(background_tasks: BackgroundTasks, request: Request, logs: list[RecordLog], project: ProjectType = "default") -> RetMsg:
    background_tasks.add_task(log_utils.do_record_apilogs, project, logs)
    # await log_utils.do_record_apilogs(request, logs)
    return RetMsg()