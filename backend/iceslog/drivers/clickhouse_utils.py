import time
import clickhouse_connect
from clickhouse_connect.driver import AsyncClient
from fastapi import HTTPException
import pandas
from sqlalchemy import text

from iceslog.api.deps import PageNumType, PageSizeType
from iceslog.utils import base_utils

cache_clients = {}
async def get_cache_client(url):
    if url in cache_clients:
        vals: list = cache_clients[url]
        while len(vals) > 0:
            client: AsyncClient = vals.pop()
            try:
                await client.ping()
            except Exception as e:
                continue
            return client
    return await clickhouse_connect.get_async_client(dsn=url, compress="gzip", connect_timeout=5.0)

async def do_cache_client(url, client: AsyncClient, has_exception=False):
    if not client:
        return
    if has_exception:
        try:
            await client.ping()
        except Exception as e:
            return
    cache_clients[url] = cache_clients.get(url, [])
    cache_clients[url].append(client)

cache_datas = []
async def insert_log_datas(url, db, datas):
    db = base_utils.get_db_name(db)
    global cache_datas
    has_exception = False
    client = None
    try:
        if len(cache_datas) == 0 and len(datas) < 1000:
            client = await get_cache_client(url)
            df = pandas.DataFrame.from_records(datas)
            ret = await client.insert_df(db, df)
            print(ret)
        else:
            cache_datas.extend(datas)
            start = time.time()
            client = await get_cache_client(url)       
            while time.time() - start < 5 and len(cache_datas) != 0:
                datas = cache_datas[:1000]
                if len(cache_datas) < 1000:
                    cache_datas = []
                else:
                    cache_datas = cache_datas[1000:]
             
                df = pandas.DataFrame.from_records(datas)
                ret = await client.insert_df(db, df)
                print(ret)
    except Exception as e:
        has_exception = True
        cache_datas.extend(datas)
        # 防止内存过大导致的程序崩溃
        if len(cache_datas) > 1000000:
            cache_datas = cache_datas[-1000000:]
        pass
        base_utils.print_exec()
    finally:
        await do_cache_client(url, client, has_exception)
    
    
async def read_log_page(url, db, search):
    from iceslog.models.logs.record import LogPageSearch
    search: LogPageSearch = search
    db = base_utils.get_db_name(db, search.startTime)
    sql = f"select * from {db}"
    count_sql = f"select count(*) from {db}"
    params = search.params()
    condition = []
    if search.msg:
        params["msg"] = f"%{search.msg}%" 
        condition.append(" msg like %(msg)s") 
        
    if search.uid:
        if base_utils.safe_int(search.uid) > 0:
            condition.append(" (uid = %(uid)s or exid = %(uid)s)")
        else:
            condition.append(" exid = %(uid)s")
        
    if search.sys:
        condition.append(" sys = %(sys)s")
        
    if search.lv:
        condition.append(" lv = %(lv)d")
        
    if search.startTime:
        condition.append(" create >= %(startTime)s")
        
    if search.endTime:
        condition.append(" create <= %(endTime)s")
        
    if len(condition) > 0:
        sql += " WHERE " + " AND ".join(condition)
        count_sql += " WHERE " + " AND ".join(condition)
    
    
    sql += " order by create desc"
    sql += " LIMIT %(limit)d OFFSET %(offset)d"
    client = await get_cache_client(url)      
    has_exception = False
    try:
        rets = await client.query_df(sql, params)
        count = await client.query(count_sql, params)
        return base_utils.dataframe_tolist(rets), count.first_row[0]
    except  :
        base_utils.print_exec()
        has_exception = True
        raise HTTPException(400, "查询出错")
    finally:
        await do_cache_client(url, client, has_exception)
