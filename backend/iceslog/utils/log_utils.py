from fastapi import Request

from iceslog.utils import http_utils


def do_record_log(request: Request, module: str, content: str):
    from iceslog.models.syslog import SysLog
    from iceslog.core.db import get_db
    session = next(get_db())
    log = SysLog(module=module, content=content,
                 request_uri=str(request.url), ip=http_utils.get_client_ip(request), province="", city="",
                 execution_time=0, browser=http_utils.get_browser(request))
    session.add(log)
    session.commit()
