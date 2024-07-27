
from clickhouse_driver import Client
import pandas
from sqlalchemy import text

from iceslog.api.deps import PageNumType, PageSizeType
from iceslog.utils import base_utils

def insert_log_datas(url, db, datas):
    client = Client.from_url(url)
    df = pandas.DataFrame.from_records(datas)
    ret = client.insert_dataframe(
        f'INSERT INTO {db} (time, log_level, sys, trace_id, uid, content, exid, extra) VALUES',
        df,
        settings=dict(use_numpy=True),)
    print(ret)
    
def read_log_page(url, db, content: str = None, sys: str = None, level: int = None, startTime: str = None, endTime: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    client = Client.from_url(url)
    sql = f"select * from {db}"
    count_sql = f"select count(*) from {db}"
    params = {
        "content": content,
        "sys": sys,
        "level": level,
        "startTime": startTime,
        "endTime": endTime,
        "offset": (pageNum.real - 1) * pageSize.real,
        "limit": pageSize.real,
    }
    condition = []
    if content:
        params["content"] = f"%{content}%" 
        condition.append(" content like %(content)s") 
        
    if sys:
        condition.append(" sys = %(sys)s")
        
    if level:
        condition.append(" log_level = %(level)d")
        
    if startTime:
        condition.append(" startTime >= %(startTime)s")
        
    if endTime:
        condition.append(" endTime >= %(endTime)s")
        
    if len(condition) > 0:
        sql += " WHERE " + " AND ".join(condition)
        count_sql += " WHERE " + " AND ".join(condition)
    
    sql += " order by time desc"
    sql += " LIMIT %(limit)d OFFSET %(offset)d"
    rets = client.query_dataframe(sql, params)
    count = client.execute(count_sql, params)[0][0]
    return base_utils.dataframe_tolist(rets), count