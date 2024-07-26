
from clickhouse_driver import Client
import pandas

from iceslog.api.deps import PageNumType, PageSizeType
from iceslog.utils import base_utils

def insert_log_datas(url, db, datas):
    client = Client.from_url(url)
    df = pandas.DataFrame.from_records(datas)
    ret = client.insert_dataframe(
        f'INSERT INTO {db} (time, log_level, trace_id, uid, content, exid, extra) VALUES',
        df,
        settings=dict(use_numpy=True),)
    print(ret)
    
def read_log_page(url, db, content: str = None, sys: str = None, level: int = None, startTime: str = None, endTime: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    client = Client.from_url(url)
    sql = f"select * from {db}"
    if content:
        pass
    
    rets = client.query_dataframe(sql)
    return base_utils.dataframe_tolist(rets)