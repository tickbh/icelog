from iceslog.utils.scheduler_utils import scheduler

from sqlmodel import select
from iceslog.utils import pool_utils

cache_logs = []

def append_logs(logs: list):
    cache_logs.extend(logs)
    
def get_logs_store():
    from iceslog.models.logs.store import LogsStore
    from iceslog.core.db import get_db
    session = next(get_db())
    statement = select(LogsStore).filter(LogsStore.status == 1)
    stores = []
    for item in session.exec(statement).all():
        stores.append(item)
    return stores

async def write_to_db():
    from iceslog.models.logs.store import LogsStore
    stores = get_logs_store()
    
    for store in stores:
        store: LogsStore = store
        if store.store == "ClickHouse":
            from clickhouse_driver import Client
            client = Client.from_url(store.connect_url)
            ret = client.execute('SHOW TABLES')
            print(ret)
            pass
        pass
    pass

# 每分钟执行的定时任务
@scheduler.scheduled_job('interval', seconds=5)
async def write_log_to_store_job():
    await write_to_db()