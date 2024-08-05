import pandas
from iceslog.utils.scheduler_utils import scheduler

from sqlmodel import select
from iceslog.utils import base_utils, pool_utils

cache_logs = []
cache_dict_logs = {}

def append_logs(project, logs: list):
    if not project in cache_dict_logs:
        cache_dict_logs[project] = []
    cache_dict_logs[project].extend(logs)  
    
def get_logs_store(project):
    from iceslog.models.logs.store import LogsStore
    from iceslog.core.db import get_db
    session = next(get_db())
    statement = select(LogsStore).filter(LogsStore.status == 1).filter(LogsStore.project == project)
    stores = []
    for item in session.exec(statement).all():
        stores.append(item)
    return stores

async def write_to_db():
    if len(cache_dict_logs) == 0:
        return
    for project in cache_dict_logs:
        insert_logs = cache_dict_logs[project]
        del cache_dict_logs[project]
        
        from iceslog.models.logs.store import LogsStore
        stores = get_logs_store(project)
        
        for store in stores:
            store: LogsStore = store
            
            if store.store.lower() == "clickhouse":
                from iceslog.drivers import clickhouse_utils
                await clickhouse_utils.insert_log_datas(store.connect_url, store.table_name, insert_logs)
            elif store.store.lower() == "kafka":
                from iceslog.drivers import kafka_utils
                await kafka_utils.insert_log_datas(store.connect_url, store.table_name, insert_logs)
        
    pass

# 每分钟执行的定时任务
@scheduler.scheduled_job('interval', seconds=5)
async def write_log_to_store_job():
    await write_to_db()