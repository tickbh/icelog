
from iceslog import models
from iceslog.utils.cache_table import CacheTable

perm_cache_table = CacheTable(models.Perms, attribs=["id", "route"])
def get_perm(id):
    return perm_cache_table.get_value(id)

group_perm_cache_table = CacheTable(models.GroupPerms, attribs=["id"])
def get_group_perm(id):
    return group_perm_cache_table.get_value(id)

menus_cache_table = CacheTable(models.Menus, attribs=["id"])
def get_menu(id):
    return menus_cache_table.get_value(id)
