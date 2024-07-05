import time, logging

from sqlmodel import SQLModel, Session, select

from iceslog.utils import base_utils

class CacheTable:
    model: SQLModel
    def __init__(self, model, use_cache=False, expire_time = 60 * 60, attribs=[], check_redis=True, redis_expire_time=30):
        self.model = model
        self.cache_time = 0
        self.expire_time = expire_time
        self.cache_table = {}
        self.attribs = attribs
        self.use_cache = use_cache
        
        self.redis_cache_time = 0
        self.check_redis = check_redis
        self.redis_expire_time = redis_expire_time

    def update(self):
        if not self.is_expire():
            return
        
        logging.info(f'chk perm expire reload data')
        temp_table = {}
        for val in self.get_iter():
            data = val.model_dump()
            if hasattr(val, "id"):
                temp_table[val.id] = data
            for attrib in self.attribs:
                if attrib in data and data[attrib]:
                    if "sub_" in attrib:
                        value = base_utils.safe_str(data[attrib])
                        for sub in value.split(","):
                            temp_table[sub] = data
                    else:
                        temp_table[data[attrib]] = data
                        
        self.cache_table = temp_table
        self.cache_time = time.time()
        self.redis_cache_time = time.time()
        logging.info(f'chk perm done')
    
    def get_iter(self):
        from iceslog.core.db import engine
        with Session(engine) as session:
            return session.exec(select(self.model)).all()

    def is_expire(self):
        logging.info(f'chk perm: {time.time()} - {self.cache_time} - {self.expire_time}')
        if time.time() - self.cache_time > self.expire_time:
            return True
        if self.check_redis and time.time() - self.redis_cache_time > self.redis_expire_time:
            # redis = pool_utils.get_redis_cache()
            # key = base_utils.get_model_cache_key(self.model)
            # value = base_utils.safe_int(redis.get(key))
            # if value > self.redis_cache_time:
            #     return True
            # return False
            pass
        return False

    def get_value(self, key=0):
        self.update()
        return self.cache_table.get(key, None)
    
    def cache_iter(self):
        for it in self.cache_table:
            yield self.cache_table[it]

