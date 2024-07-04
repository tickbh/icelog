import time

from sqlmodel import SQLModel, Session, select

from iceslog.models.menu import Menus
from iceslog.utils import base_utils

class PidTable:
    model: SQLModel
    def __init__(self, model, use_cache=False, expire_time = 60 * 60, check_redis=True, redis_expire_time=30):
        self.default_type = "default"
        self.model = model
        self.cache_time = 0
        self.cache_values = {}
        self.cache_show_values = {}
        self.cache_id_values = {}
        self.count_values = {}
        self.use_cache = use_cache
        self.expire_time = expire_time
        
        self.redis_cache_time = 0
        self.check_redis = check_redis
        self.redis_expire_time = redis_expire_time

    def get_type(self, val):
        if hasattr(val, "type"):
            return val.type
        return self.default_type

    def update(self):
        if not self.is_expire():
            return

        self.cache_time = time.time()
        self.redis_cache_time = time.time()
        old_cache_values = self.cache_values
        old_cache_show_values = self.cache_show_values
        old_cache_id_values = self.cache_id_values
        old_count_values = self.count_values
        try:
            self.cache_values = {}
            self.cache_show_values = {}
            self.cache_id_values = {}
            self.count_values = {}

            value_table = {}

            def _sort_value_func(elem):
                return elem.get("sort", 0) or 0

            def _build_value(table, key):
                value = table.pop(key, None)
                if not value:
                    return None
                
                for m in value:
                    sub_value = _build_value(table, m["id"])
                    if not sub_value:
                        continue
                    m["children"] = sub_value
                return value

            def _filter_show(table):
                new_table = []
                if not table:
                    return new_table
                for m in table:
                    if not m.get("is_show"):
                        continue
                    new_m = m.copy()
                    if m.get("children"):
                        new_m["children"] = _filter_show(m.get("children", {}))
                    new_table.append(new_m)
                return new_table

            for val in self.get_iter():
                type = self.get_type(val)
                self.count_values[type] = self.count_values.get(type, 0) + 1
                
                pid = val.pid
                value_table[type] = value_table.get(type, {})
                value_table[type][pid] = value_table[type].get(pid, [])
                data = val.model_dump()
                value_table[type][pid].append(data)
                self.cache_id_values[val.id] = data
            
            for type, table in value_table.items():
                for _, list in table.items():
                    list.sort(key = _sort_value_func)
                
                main_value = _build_value(table, 0)
                self.cache_values[type] = main_value
                self.cache_show_values[type] = _filter_show(main_value)
        except :
            base_utils.print_exec()
            self.cache_time = 0
            self.redis_cache_time = 0
            self.cache_values = old_cache_values
            self.cache_show_values = old_cache_show_values
            self.cache_id_values = old_cache_id_values
            self.count_values = old_count_values

    def get_iter(self):
        from iceslog.core.db import engine
        with Session(engine) as session:
            # menus = session.execute(select(Menus)).scalars().all()
            menus = session.exec(select(Menus)).all()
            for val in menus:
                print("val", val)
                print("val.key", val.id)
                yield val

    def is_expire(self):
        if time.time() - self.cache_time > self.expire_time:
            return True
        if self.check_redis and time.time() - self.redis_cache_time > self.redis_expire_time:
            # redis = pool_utils.get_redis_cache()
            # key = base_utils.get_model_cache_key(self.model)
            # value = base_utils.safe_int(redis.get(key))
            # if value > self.redis_cache_time:
            #     return True
            # self.redis_cache_time = time.time()
            return False
        return False

    def get_values(self, type="default", default={}):
        self.update()
        return self.cache_values.get(type, default)

    def get_id_value(self, type="default", default={}):
        self.update()
        return self.cache_id_values.get(type, default)
        
    def get_show_values(self, type="default", default={}):
        self.update()
        return self.cache_show_values.get(type, default)
    
    def get_counts(self, type="default", default = 0):
        self.update()
        return self.count_values.get(type, default)

    def force_update(self):
        self.cache_time = 0
        self.update()
    
    def mark_dirty(self):
        self.cache_time = 0
        
