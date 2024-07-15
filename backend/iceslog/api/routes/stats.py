
from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Form, HTTPException, Request
from sqlmodel import select
from iceslog import cruds
from iceslog.api.deps import CurrentUser, RedisDep, SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import AuthCaptcha, LoginoutRet, RetMsg, LoginRet, Token
from iceslog.models.log_record import LogFreq, LogVisitInfos, OneLogVisit
from iceslog.utils import base_utils, log_utils
router = APIRouter()

@router.get("/visit-trend", response_model=LogVisitInfos)
async def get_visit(session: SessionDep, startDate: datetime, endDate: datetime, minStep: int) -> Any:
    start_time = base_utils.get_now_minute(startDate) 
    end_time = base_utils.get_now_minute(endDate)
    statement = select(LogFreq).where(LogFreq.log_time >= start_time).where(LogFreq.log_time<end_time)
    infos = LogVisitInfos(dates=[], times=[], module="log")
    for s in session.exec(statement).all():
        infos.dates.append(base_utils.minute_to_datetime(s.log_time))
        infos.times.append(s.times)
    print("start:",startDate)
    return infos
# .build_message()
