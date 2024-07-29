import random
import time
from aiokafka  import AIOKafkaProducer
from fastapi import HTTPException
import pandas
from sqlalchemy import text

from iceslog.api.deps import PageNumType, PageSizeType
from iceslog.utils import base_utils

cache_clients = {}
async def get_cache_client(url: str):
    if url in cache_clients:
        vals: list = cache_clients[url]
        while len(vals) > 0:
            client: AIOKafkaProducer = vals.pop()
            if client._closed:
                continue
            return client
    if "kafka://" in url:
        url = url.replace("kafka://", "")
    product = AIOKafkaProducer(bootstrap_servers=url)
    await product.start()
    return product

async def do_cache_client(url, client: AIOKafkaProducer, has_exception=False):
    if not client:
        return
    if has_exception:
        if client._closed:
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
            batch = client.create_batch()
            partitions = await client.partitions_for(db)
            partition = random.choice(tuple(partitions))
            for d in datas:
                batch.append(key=None, value=base_utils.safe_str(d).encode(), timestamp=None)
            await client.send_batch(batch, db, partition=partition)
        else:
            cache_datas.extend(datas)
            start = time.time()
            client = await get_cache_client(url)      
            partitions = await client.partitions_for(db)
            partition = random.choice(tuple(partitions)) 
            while time.time() - start < 5 and len(cache_datas) != 0:
                datas = cache_datas[:1000]
                if len(cache_datas) < 1000:
                    cache_datas = []
                else:
                    cache_datas = cache_datas[1000:]
             
                batch = client.create_batch()
                for d in datas:
                    batch.append(key=None, value=base_utils.safe_str(d).encode(), timestamp=None)
                await client.send_batch(batch, db, partition=partition)
    except Exception as e:
        has_exception = True
        cache_datas.extend(datas)
        # 防止内存过大导致的程序崩溃
        if len(cache_datas) > 1000000:
            cache_datas = cache_datas[-1000000:]
        pass
    finally:
        await do_cache_client(url, client, has_exception)
    
async def read_log_page(url, db, content: str = None, sys: str = None, level: int = None, startTime: str = None, endTime: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    raise HTTPException(400, "kafka 不支持查询")
