import time
import elasticsearch
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException
import pandas
from sqlalchemy import text

from iceslog.api.deps import PageNumType, PageSizeType
from iceslog.utils import base_utils

exist_caches = {}
cache_clients = {}
async def get_cache_client(url):
    if url in cache_clients:
        vals: list = cache_clients[url]
        while len(vals) > 0:
            client: AsyncElasticsearch = vals.pop()
            try:
                await client.ping()
            except Exception as e:
                continue
            return client
    return AsyncElasticsearch(hosts=url, timeout=60.0)

async def do_cache_client(url, client: AsyncElasticsearch, has_exception=False):
    if not client:
        return
    if has_exception:
        try:
            await client.health_report()
        except Exception as e:
            return
    cache_clients[url] = cache_clients.get(url, [])
    cache_clients[url].append(client)

async def ensure_exist(client: AsyncElasticsearch, db: str):
    if db in exist_caches:
        return True
    if client.indices.exists(index=db):
        exist_caches[db] = True
        return True
    succ = await client.indices.create(index=db)
    if succ:
        exist_caches[db] = True
        return True
    raise Exception(f"无法创建index:{db}")

async def bluk_insert(client: AsyncElasticsearch, db: str, datas: list[str]):
    await ensure_exist(client, db)
    actions = []
    for d in datas:
        tid = d.get("tid")
        d["sys1"] = d["sys"]
        if not tid:
            continue
        actions.append({"index": {"_id": d.get("tid")}})
        actions.append(d)
    ret = await client.bulk(index=db, body=actions)
    print(ret)
    return ret
     
cache_datas = []
async def insert_log_datas(url, db, datas):
    db = base_utils.get_db_name(db)
    global cache_datas
    has_exception = False
    client = None
    try:
        if len(cache_datas) == 0 and len(datas) < 1000:
            client = await get_cache_client(url)
            await bluk_insert(client, db, datas)
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
                await bluk_insert(client, db, datas)
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
    
    condition = {
    }
    
    if search.msg:
        condition["match"] = condition.get("match", {})
        condition["match"]["msg"] = search.msg
        
    if search.uid:
        condition["bool"] = condition.get("bool", {"must": [], "must_not": [], "should": []})
        if base_utils.safe_int(search.uid) > 0:
            condition["bool"]["must"].append({
                "term": {
                    "uid": base_utils.safe_int(search.uid)
                }
            })
        else:
            condition["bool"]["must"].append({
                "term": {
                    "uid": search.uid.lower()
                }
            })
        
    if search.sys:
        condition["bool"] = condition.get("bool", {"must": [], "must_not": [], "should": []})
        condition["bool"]["must"].append({
            "term": {
                "sys": search.sys.lower()
            }
        })
        
    if search.lv:
        condition["bool"] = condition.get("bool", {"must": [], "must_not": [], "should": []})
        condition["bool"]["must"].append({
            "term": {
                "lv": search.lv
            }
        })
        
        
    if search.startTime:
        from datetime import datetime
        condition["bool"] = condition.get("bool", {"must": [], "must_not": [], "should": []})
        condition["bool"]["must"].append({
            "range": {
                "create": {
                    "gte": datetime.fromisoformat(search.startTime),
                    "lte": datetime.fromisoformat(search.endTime)
                }
            }
        })
        
    has_exception = False
    client = None
    try:
        client = await get_cache_client(url)
        ret = await client.search(query= condition if len(condition) > 0 else None, size=search.get_limit(), from_=search.get_offset(), sort=[
            {"create": "desc"},
        ])
        hits = ret["hits"]
        count = hits["total"]["value"]
        rets = []
        for v in hits["hits"]:
            rets.append(v["_source"])
        return rets, count
    except  :
        base_utils.print_exec()
        has_exception = True
        raise HTTPException(400, "查询出错")
    finally:
        await do_cache_client(url, client, has_exception)
