
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
from iceslog.models.logs.record import LogFreq, LogVisitInfos, OneLogVisit
from iceslog.utils import base_utils, log_utils
router = APIRouter()

@router.get("/visit-trend", response_model=LogVisitInfos)
async def get_visit(session: SessionDep, startDate: datetime, endDate: datetime, minStep: int) -> Any:

    min_step = 1
    if minStep == 1:
        min_step = 10
    elif minStep == 2:
        min_step = 30
    start_time = base_utils.fix_step(base_utils.get_now_minute(startDate), min_step) 
    end_time = base_utils.fix_step(base_utils.get_now_minute(endDate), min_step) + min_step
    hash_tables = {}
    
    for val in range(start_time, end_time, min_step):
        hash_tables[val] = 0
        
    statement = select(LogFreq).where(LogFreq.log_time >= start_time).where(LogFreq.log_time<end_time)
    infos = LogVisitInfos(dates=[], times=[], module="log")
    for s in session.exec(statement).all():
        step = base_utils.calc_step_value(start_time, s.log_time, min_step)
        hash_tables[step] = hash_tables.get(step, 0) + s.times
    
    for val in range(start_time, end_time, min_step):
        infos.dates.append(base_utils.minute_to_datetime(val))
        infos.times.append(hash_tables.get(val, 0))
    return infos
# .build_message()
