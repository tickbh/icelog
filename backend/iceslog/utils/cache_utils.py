
from iceslog import models
from iceslog.utils import base_utils
from iceslog.utils.cache_table import CacheTable

perm_cache_table = CacheTable(models.Perms, attribs=["id", "route"])
def get_perm(id):
    return perm_cache_table.get_value(id)

group_perm_cache_table = CacheTable(models.GroupPerms, attribs=["id"])
def get_group_perm(id):
    return group_perm_cache_table.get_value(id)

def get_all_perms(group_id: int) -> list[str]:
    group = get_group_perm(group_id)
    vals = []
    if group and "permissions" in group:
        for id in group["permissions"].split("|"):
            perm = get_perm(base_utils.safe_int(id) )
            if perm and len(perm["codename"]) > 0:
                vals.append(perm["codename"])
    
    return vals    

menus_cache_table = CacheTable(models.Menus, attribs=["id"])
def get_menu(id):
    return menus_cache_table.get_value(id)
